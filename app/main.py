from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from utils.config import settings
from services.profile_processor import ProfileProcessor
from models.schemas import AnalyzeRequest, DatePlanRequest
from typing import List, Optional, Dict
import traceback
from services.profile_enricher import ProfileEnricher
from utils.context_container import create_context_container
from services.date_intelligence_engine import DateIntelligenceEngine
from services.venue_discoverer import VenueDiscoverer
from services.final_intelligence_optimizer import FinalIntelligenceOptimizer
import time
import uuid
import asyncio
import json
import redis
from concurrent.futures import ThreadPoolExecutor

# Import error handlers
from utils.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    api_exception_handler,
    APIException
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ai-mor.me API - Cultural Intelligence Dating Engine",
    description="Redis-Powered Async Cultural Intelligence Dating Engine",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# ===== REDIS CONNECTION =====

def get_redis_client():
    """Get Redis client with fallback for different environments"""
    try:
        # Try Heroku Redis first (production)
        redis_url = os.getenv('REDIS_URL')
        if redis_url:
            logger.info("Connecting to Heroku Redis...")
            import ssl
            return redis.from_url(
                redis_url, 
                decode_responses=True,
                ssl_cert_reqs=ssl.CERT_NONE,
                ssl_check_hostname=False,
                ssl_ca_certs=None
            )
        
        # Try local Redis (development)
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_password = os.getenv('REDIS_PASSWORD')
        
        logger.info(f"Connecting to Redis at {redis_host}:{redis_port}...")
        return redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        return None

# Initialize Redis and processors
redis_client = get_redis_client()
profile_processor = ProfileProcessor()

# Thread pool for background processing
executor = ThreadPoolExecutor(max_workers=3)

# Redis key patterns
PROGRESS_KEY = "progress:{request_id}"
RESULT_KEY = "result:{request_id}"
REQUEST_KEY = "request:{request_id}"

# ===== REDIS HELPER FUNCTIONS =====

def redis_set_json(key: str, data: dict, expire_seconds: int = 3600):
    """Set JSON data in Redis with expiration"""
    try:
        if redis_client:
            redis_client.setex(key, expire_seconds, json.dumps(data, default=str))
            return True
    except Exception as e:
        logger.error(f"Redis set failed for {key}: {e}")
    return False

def redis_get_json(key: str) -> Optional[dict]:
    """Get JSON data from Redis"""
    try:
        if redis_client:
            data = redis_client.get(key)
            return json.loads(data) if data else None
    except Exception as e:
        logger.error(f"Redis get failed for {key}: {e}")
    return None

def redis_delete(key: str):
    """Delete key from Redis"""
    try:
        if redis_client:
            redis_client.delete(key)
    except Exception as e:
        logger.error(f"Redis delete failed for {key}: {e}")

def cleanup_expired_requests():
    """Clean up expired Redis keys (Redis handles TTL automatically, but we can do manual cleanup)"""
    try:
        if redis_client:
            # Get all progress keys older than 2 hours for manual cleanup
            pattern = "progress:*"
            keys = redis_client.keys(pattern)
            
            expired_count = 0
            for key in keys:
                try:
                    ttl = redis_client.ttl(key)
                    if ttl == -1:  # No expiration set (shouldn't happen, but safety)
                        redis_client.expire(key, 3600)  # Set 1 hour expiration
                        expired_count += 1
                except Exception:
                    continue
                    
            if expired_count > 0:
                logger.info(f"Set expiration for {expired_count} Redis keys")
                
    except Exception as e:
        logger.error(f"Redis cleanup failed: {e}")

def get_redis_status():
    """Get Redis connection status and stats"""
    try:
        if redis_client:
            # Test connection with ping
            redis_client.ping()
            
            info = redis_client.info()
            
            # Count active requests
            try:
                progress_keys = len(redis_client.keys("progress:*"))
                result_keys = len(redis_client.keys("result:*"))
            except Exception:
                progress_keys = 0
                result_keys = 0
            
            return {
                "connected": True,
                "redis_version": info.get("redis_version", "unknown"),
                "used_memory_human": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "active_progress_keys": progress_keys,
                "active_result_keys": result_keys
            }
    except Exception as e:
        logger.error(f"Redis status check failed: {e}")
    
    return {"connected": False, "error": "Redis not available"}

# ===== CORE ENDPOINTS =====

@app.get("/health")
async def health_check():
    """Enhanced health check with Redis status"""
    try:
        validation = settings.validate_required_keys()
        redis_status = get_redis_status()
        
        # Clean up if Redis is available
        if redis_status["connected"]:
            cleanup_expired_requests()
        
        return {
            "status": "healthy",
            "service": "ai-mor.me API v2.1 - Redis-Powered Cultural Intelligence",
            "version": "2.1.0",
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "api_keys_valid": validation["valid"],
            "missing_keys": validation["missing_keys"] if not validation["valid"] else [],
            "redis_status": redis_status,
            "processing_queue": {
                "active_requests": redis_status.get("active_progress_keys", 0),
                "completed_results": redis_status.get("active_result_keys", 0),
                "storage": "redis" if redis_status["connected"] else "fallback_memory"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ai-mor.me API v2.1 - Redis-Powered Cultural Intelligence",
        "features": [
            "Redis-powered real-time progress tracking",
            "6-step AI pipeline with live updates", 
            "Async processing for instant response",
            "OpenAI + Qloo cultural intelligence",
            "Production-ready scalable architecture"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "start_plan": "POST /start-cultural-date-plan",
            "progress": "GET /date-plan-progress/{request_id}",
            "result": "GET /date-plan-result/{request_id}",
            "cancel": "DELETE /cancel-date-plan/{request_id}"
        },
        "version": "2.1.0"
    }

# ===== MAIN ASYNC ENDPOINTS =====

@app.post("/start-cultural-date-plan")
async def start_cultural_date_plan(request: DatePlanRequest, background_tasks: BackgroundTasks):
    """
    START: Redis-Powered Async Cultural Intelligence Date Planning FOR TWO PROFILES
    
    Accepts two complete profiles with text/images and creates intelligent date plan.
    """
    try:
        # Validate that both profiles have content
        profile_a_valid = any([request.profile_a.text, request.profile_a.image_data])
        profile_b_valid = any([request.profile_b.text, request.profile_b.image_data])
        
        if not profile_a_valid or not profile_b_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Both profiles must provide either text or image data",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Store request data in Redis (expires in 2 hours)
        request_data = {
            "request_data": request.dict(),
            "created_at": datetime.now().isoformat(),
            "status": "queued"
        }
        
        if not redis_set_json(REQUEST_KEY.format(request_id=request_id), request_data, 7200):
            logger.warning("Redis storage failed, but continuing with processing")
        
        # Initialize progress tracking in Redis
        initial_progress = {
            "request_id": request_id,
            "status": "starting",
            "overall_progress": 0,
            "current_step": 0,
            "steps": {
                "1": {"name": "Profile Analysis (Both)", "status": "pending", "duration": None, "preview": "Preparing dual personality analysis..."},
                "2": {"name": "Cultural Discovery (Both)", "status": "pending", "duration": None, "preview": "Waiting for cultural exploration..."},
                "3": {"name": "Compatibility Calculation", "status": "pending", "duration": None, "preview": "Compatibility analysis pending..."},
                "4": {"name": "Activity Planning", "status": "pending", "duration": None, "preview": "Activity planning queued..."},
                "5": {"name": "Venue Discovery", "status": "pending", "duration": None, "preview": "Venue discovery awaiting..."},
                "6": {"name": "Final Optimization", "status": "pending", "duration": None, "preview": "Final optimization pending..."}
            },
            "cultural_previews": [],
            "eta_seconds": 120,
            "processing_start": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        if not redis_set_json(PROGRESS_KEY.format(request_id=request_id), initial_progress, 7200):
            logger.warning("Redis progress storage failed, but continuing")
        
        # Start background processing for TWO PROFILES
        logger.info(f"🎬 STARTING background task for {request_id} - SINGLE CALL")
        background_tasks.add_task(process_dual_profile_pipeline, request_id)
        logger.info(f"🎬 QUEUED background task for {request_id} - TASK ADDED")
        
        # Log request start
        logger.info(f"🚀 Started Redis-powered DUAL PROFILE cultural intelligence processing: {request_id}")
        
        # Return immediate response
        return {
            "success": True,
            "message": "Dual profile cultural intelligence analysis started with Redis state management",
            "request_id": request_id,
            "status": "processing",
            "estimated_time_seconds": 120,
            "progress_endpoint": f"/date-plan-progress/{request_id}",
            "result_endpoint": f"/date-plan-result/{request_id}",
            "storage": "redis" if redis_client else "memory_fallback",
            "profiles": "dual_profile_mode",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to start dual profile cultural intelligence processing: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Failed to start dual profile processing",
                "detail": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/date-plan-progress/{request_id}")
async def get_date_plan_progress(request_id: str):
    """
    PROGRESS: Redis-powered real-time progress updates
    
    ENHANCED: Returns complete results when status is "complete" to bypass corruption bug.
    """
    try:
        # Get progress from Redis
        progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        
        if not progress:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Request not found or expired",
                    "request_id": request_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Calculate elapsed time and update ETA
        start_time = datetime.fromisoformat(progress["processing_start"])
        elapsed_seconds = (datetime.now() - start_time).total_seconds()
        
        # Dynamic ETA calculation based on current step
        if progress["status"] == "processing":
            current_step = progress["current_step"]
            if current_step == 1:
                progress["eta_seconds"] = max(0, 120 - elapsed_seconds)
            elif current_step == 2:
                progress["eta_seconds"] = max(0, 100 - elapsed_seconds)
            elif current_step <= 4:
                progress["eta_seconds"] = max(0, 80 - elapsed_seconds)
            elif current_step == 5:
                progress["eta_seconds"] = max(0, 50 - elapsed_seconds)
            elif current_step == 6:
                progress["eta_seconds"] = max(0, 30 - elapsed_seconds)
            else:
                progress["eta_seconds"] = 0
        else:
            progress["eta_seconds"] = 0
        
        # Add elapsed time and last updated for frontend
        progress["elapsed_seconds"] = int(elapsed_seconds)
        progress["last_updated"] = datetime.now().isoformat()
        
        # ENHANCED: If processing is complete, add full results as new field
        if progress["status"] == "complete":
            # PRIORITY 1: Check for embedded results (corruption-proof)
            if progress.get("results_embedded") and progress.get("final_date_plan_embedded"):
                progress["final_results_available"] = True
                progress["complete_date_plan"] = progress["final_date_plan_embedded"]
                progress["results_message"] = "Complete date plan available (embedded results)"
                progress["results_source"] = "embedded_in_progress"
                logger.info(f"✅ DELIVERED EMBEDDED RESULTS via progress endpoint for {request_id}")
            else:
                # FALLBACK: Try to get results from Redis (may be corrupted)
                final_results = redis_get_json(RESULT_KEY.format(request_id=request_id))
                
                if final_results and final_results.get("success"):
                    progress["final_results_available"] = True
                    progress["complete_date_plan"] = final_results
                    progress["results_message"] = "Complete date plan available (from Redis)"
                    progress["results_source"] = "redis_fallback"
                    logger.info(f"✅ DELIVERED REDIS RESULTS via progress endpoint for {request_id}")
                else:
                    # Results not available or corrupted
                    progress["final_results_available"] = False
                    progress["results_message"] = "Results corrupted by duplicate task - please retry"
                    progress["results_source"] = "corrupted"
                    logger.warning(f"⚠️  All results corrupted or missing for {request_id}")
        else:
            # Still processing - no results yet
            progress["final_results_available"] = False
        # Update Redis with new timing info (quick update, 10 min expiry)
        redis_set_json(PROGRESS_KEY.format(request_id=request_id), progress, 600)
        
        return progress
        
    except Exception as e:
        logger.error(f"Failed to get progress for {request_id}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Failed to get progress",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/date-plan-result/{request_id}")
async def get_date_plan_result(request_id: str):
    """
    RESULT: Get final cultural intelligence date plan from Redis
    
    Returns complete results when processing is finished.
    """
    try:
        # Check progress first
        progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        
        if not progress:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Request not found or expired",
                    "request_id": request_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Check if processing is complete
        if progress["status"] not in ["complete", "error"]:
            return JSONResponse(
                status_code=202,
                content={
                    "success": False,
                    "error": "Processing not complete yet",
                    "status": progress["status"],
                    "current_step": progress["current_step"],
                    "request_id": request_id,
                    "message": "Please continue polling /date-plan-progress/{request_id}",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Get results from Redis
        result = redis_get_json(RESULT_KEY.format(request_id=request_id))
        
        if not result:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Results not found despite completion status",
                    "request_id": request_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Add request metadata
        result["request_metadata"] = {
            "request_id": request_id,
            "processing_time_seconds": progress.get("elapsed_seconds", 0),
            "completed_at": datetime.now().isoformat(),
            "steps_completed": progress["current_step"],
            "storage_backend": "redis"
        }
        
        logger.info(f"✅ Delivered Redis-stored results for {request_id}")
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get results for {request_id}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Failed to get results",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        )

# ===== UTILITY ENDPOINTS =====

@app.delete("/cancel-date-plan/{request_id}")
async def cancel_date_plan(request_id: str):
    """Cancel a running date plan request via Redis"""
    try:
        progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        
        if progress:
            # Mark as cancelled in Redis
            progress["status"] = "cancelled"
            progress["last_updated"] = datetime.now().isoformat()
            redis_set_json(PROGRESS_KEY.format(request_id=request_id), progress, 600)
            
            return {
                "success": True,
                "message": "Date plan processing cancelled",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": "Request not found or expired",
                    "request_id": request_id
                }
            )
    except Exception as e:
        logger.error(f"Failed to cancel {request_id}: {str(e)}")
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

@app.get("/demo")
async def demo_with_redis():
    """Demo endpoint showing Redis-powered async flow"""
    redis_status = get_redis_status()
    
    return {
        "demo": "Redis-Powered Async Cultural Intelligence Demo",
        "redis_backend": redis_status,
        "flow": {
            "step_1": "POST /start-cultural-date-plan with profiles → Immediate response + Redis storage",
            "step_2": "Poll GET /date-plan-progress/{request_id} every 2s → Live updates from Redis",
            "step_3": "GET /date-plan-result/{request_id} when complete → Final results from Redis"
        },
        "sample_progress_flow": [
            "Step 1/6: Analyzing Personalities... ✅ (12s)",
            "├─ Cultural Preview: Found core personality traits",
            "Step 2/6: Discovering Cultural Preferences... ✅ (28s)", 
            "├─ Cultural Preview: Discovered 12 cross-domain preferences",
            "Step 3/6: Calculating Compatibility... ✅ (16s)",
            "├─ Cultural Preview: Compatibility: 70% match",
            "Step 5/6: Finding Perfect Venues... ✅ (11s)",
            "├─ Cultural Preview: Selected 6 perfect venues",
            "Step 6/6: Creating Your Date Plan... ✅ (38s)",
            "├─ Cultural Preview: Your perfect Rotterdam date plan is ready!"
        ],
        "benefits": [
            "Redis-powered persistence and reliability",
            "Real-time cultural intelligence streaming",
            "Production-ready scalable architecture",
            "Automatic expiration and cleanup"
        ],
        "expected_duration": "~2 minutes with engaging real-time updates",
        "version": "2.1.0"
    }

# ===== REDIS-POWERED BACKGROUND PROCESSING =====

def process_dual_profile_pipeline(request_id: str):
    """
    Redis-powered background processing for TWO PROFILES with persistent state management
    """
    
    # CRITICAL: Global duplicate prevention
    completion_marker_key = f"completed:{request_id}"
    if redis_client and redis_client.exists(completion_marker_key):
        logger.warning(f"🚫 TASK ALREADY COMPLETED for {request_id} - blocking duplicate")
        return
    
    # CRITICAL: Check if already processing
    processing_lock_key = f"processing_lock:{request_id}"
    if redis_client:
        if redis_client.exists(processing_lock_key):
            logger.warning(f"🚫 DUPLICATE TASK BLOCKED for {request_id} - already processing")
            return
        
        # Set processing lock
        redis_client.setex(processing_lock_key, 300, "locked")  # 5 minute lock
        logger.info(f"🔒 Processing lock acquired for {request_id}")
    
    try:
        logger.info(f"🔄 Starting Redis-powered DUAL PROFILE background processing for {request_id}")
        
        # Get request data from Redis
        request_data_raw = redis_get_json(REQUEST_KEY.format(request_id=request_id))
        if not request_data_raw:
            logger.error(f"❌ Request data not found in Redis for {request_id}")
            return
        
        logger.info(f"📋 Retrieved request data for {request_id}: {type(request_data_raw)}")
        logger.info(f"📋 Request data keys: {list(request_data_raw.keys()) if isinstance(request_data_raw, dict) else 'Not a dict'}")
        
        # Parse request data for TWO PROFILES
        try:
            request_data = DatePlanRequest(**request_data_raw["request_data"])
            logger.info(f"📋 Parsed request data successfully for {request_id}")
            logger.info(f"📋 Profile A text length: {len(request_data.profile_a.text) if request_data.profile_a.text else 0}")
            logger.info(f"📋 Profile B text length: {len(request_data.profile_b.text) if request_data.profile_b.text else 0}")
        except Exception as e:
            logger.error(f"❌ Failed to parse request data for {request_id}: {e}")
            logger.error(f"❌ Raw request data: {request_data_raw}")
            handle_redis_processing_error(request_id, f"Data parsing failed: {str(e)}", 0)
            return
            
        context = request_data.context.dict() if request_data.context else {}
        
        # Validate profiles have content
        if not request_data.profile_a.text and not request_data.profile_b.text:
            logger.error(f"No text content in either profile for {request_id}")
            handle_redis_processing_error(request_id, "No text content found in profiles", 1)
            return
        
        # Update status to processing
        update_redis_progress(request_id, status="processing", current_step=1)
        
        # Initialize context container
        context_container = create_context_container(context)
        
        # Track total time
        pipeline_start = time.time()
        
        # ===== STEP 1: DUAL PROFILE ANALYSIS =====
        update_redis_progress(request_id, current_step=1, step_status="1", status_value="processing", 
                       preview="Analyzing both personalities and interests...")
        
        step1_start = time.time()
        
        step1_context = context_container.get_context_for_step(1)
        
        # Process Profile A
        profile_a_images = []
        if hasattr(request_data.profile_a, 'image_data') and request_data.profile_a.image_data:
            profile_a_images = [request_data.profile_a.image_data]
        
        result_a = profile_processor.process_profile_with_context(
            text=request_data.profile_a.text,
            image_data_list=profile_a_images,
            context=step1_context
        )
        
        # Process Profile B  
        profile_b_images = []
        if hasattr(request_data.profile_b, 'image_data') and request_data.profile_b.image_data:
            profile_b_images = [request_data.profile_b.image_data]
            
        result_b = profile_processor.process_profile_with_context(
            text=request_data.profile_b.text,
            image_data_list=profile_b_images,
            context=step1_context
        )
        
        step1_time = time.time() - step1_start
        
        if not result_a.get("success") or not result_b.get("success"):
            error_msg = f"Profile analysis failed - A: {result_a.get('success', False)}, B: {result_b.get('success', False)}"
            handle_redis_processing_error(request_id, error_msg, 1)
            return
        
        # Store both results
        context_container.store_step_output("1a", result_a)
        context_container.store_step_output("1b", result_b)
        
        # Extract confidence for preview
        confidence_a = result_a["analysis"].get("processing_confidence", 0)
        confidence_b = result_b["analysis"].get("processing_confidence", 0)
        avg_confidence = (confidence_a + confidence_b) / 2
        
        step1_preview = f"Both personalities analyzed (avg confidence: {avg_confidence:.0%})"
        
        update_redis_progress(request_id, step_status="1", status_value="complete", 
                       duration=step1_time, preview=step1_preview,
                       cultural_preview=f"✅ Two personality profiles analyzed (confidence: {avg_confidence:.0%})")
        
        # Check for cancellation
        if check_redis_cancellation(request_id):
            return
        
        # ===== STEP 2: DUAL CULTURAL ENHANCEMENT =====
        update_redis_progress(request_id, current_step=2, step_status="2", status_value="processing",
                       preview="Discovering cultural preferences for both profiles...")
        
        step2_start = time.time()
        
        step2_context = context_container.get_context_for_step(2)
        enricher = ProfileEnricher()
        
        # Enhance both profiles
        enhanced_profile_a = enricher.process_psychological_profile(
            result_a["analysis"], step2_context
        )
        enhanced_profile_b = enricher.process_psychological_profile(
            result_b["analysis"], step2_context
        )
        
        step2_time = time.time() - step2_start
        
        if not enhanced_profile_a.get("success") or not enhanced_profile_b.get("success"):
            error_msg = f"Cultural enhancement failed - A: {enhanced_profile_a.get('success', False)}, B: {enhanced_profile_b.get('success', False)}"
            handle_redis_processing_error(request_id, error_msg, 2)
            return
        
        context_container.store_step_output("2a", enhanced_profile_a)
        context_container.store_step_output("2b", enhanced_profile_b)
        
        # Extract discoveries for preview
        metadata_a = enhanced_profile_a.get("processing_metadata", {})
        metadata_b = enhanced_profile_b.get("processing_metadata", {})
        discoveries_a = metadata_a.get("total_new_discoveries", 0)
        discoveries_b = metadata_b.get("total_new_discoveries", 0)
        total_discoveries = discoveries_a + discoveries_b
        user_location = metadata_a.get("user_location", "unknown")
        
        step2_preview = f"Found {total_discoveries} total cultural discoveries in {user_location}"
        
        update_redis_progress(request_id, step_status="2", status_value="complete",
                       duration=step2_time, preview=step2_preview,
                       cultural_preview=f"🌍 Discovered {total_discoveries} cross-domain preferences for both profiles in {user_location}")
        
        # Check for cancellation
        if check_redis_cancellation(request_id):
            return
        
        # ===== STEPS 3-4: DATE INTELLIGENCE FOR TWO PEOPLE =====
        update_redis_progress(request_id, current_step=3, step_status="3", status_value="processing",
                       preview="Calculating real compatibility between two people...")
        
        step34_start = time.time()
        
        step34_context = context_container.get_context_for_step(3)
        engine = DateIntelligenceEngine()
        
        # NOW CREATE REAL DATE PLAN FOR TWO DIFFERENT PEOPLE
        date_plan = engine.create_intelligent_date_plan(
            enriched_profile_a=enhanced_profile_a,
            enriched_profile_b=enhanced_profile_b,  # ACTUAL TWO DIFFERENT PEOPLE!
            context=step34_context
        )
        
        step34_time = time.time() - step34_start
        
        if not date_plan or date_plan.get("error"):
            handle_redis_processing_error(request_id, f"Steps 3-4 failed: {date_plan.get('error', 'Date intelligence failed')}", 3)
            return
        
        context_container.store_step_output(3, date_plan)
        
        # Extract compatibility and theme for preview
        compatibility = date_plan.get("compatibility_insights", {})
        theme = date_plan.get("intelligent_date_plan", {}).get("theme", "Unknown")
        comp_score = compatibility.get("overall_compatibility", 0)
        
        step34_preview = f"Compatibility: {comp_score:.0%} - Theme: {theme}"
        
        update_redis_progress(request_id, step_status="3", status_value="complete",
                       duration=step34_time, preview=step34_preview,
                       cultural_preview=f"💝 Real compatibility calculated: {comp_score:.0%} match with theme '{theme}'")
        
        # Mark step 4 as included
        update_redis_progress(request_id, current_step=4, step_status="4", status_value="complete",
                       duration=0, preview="Activity planning included in compatibility analysis")
        
        # Check for cancellation
        if check_redis_cancellation(request_id):
            return
        
        # ===== STEP 5: VENUE DISCOVERY =====
        update_redis_progress(request_id, current_step=5, step_status="5", status_value="processing",
                       preview="Finding perfect venues with AI intelligence...")
        
        step5_start = time.time()
        
        step5_input = context_container.get_enhanced_output_for_next_step(3)
        discoverer = VenueDiscoverer()
        venue_enhanced_plan = discoverer.discover_venues_for_date_plan(step5_input)
        
        step5_time = time.time() - step5_start
        
        if not venue_enhanced_plan:
            handle_redis_processing_error(request_id, "Step 5 failed: Venue discovery failed", 5)
            return
        
        context_container.store_step_output(5, venue_enhanced_plan)
        
        # Extract venue info for preview
        venue_summary = venue_enhanced_plan.get("venue_discovery_summary", {})
        venues_selected = venue_summary.get("total_venues_selected", 0)
        success_rate = venue_summary.get("discovery_success_rate", 0)
        
        step5_preview = f"Found {venues_selected} perfect venues (success: {success_rate:.0%})"
        
        update_redis_progress(request_id, step_status="5", status_value="complete",
                       duration=step5_time, preview=step5_preview,
                       cultural_preview=f"🏢 Selected {venues_selected} perfect venues for your date in {user_location}")
        
        # Check for cancellation
        if check_redis_cancellation(request_id):
            return
        
        # ===== STEP 6: FINAL OPTIMIZATION =====
        update_redis_progress(request_id, current_step=6, step_status="6", status_value="processing",
                       preview="Creating your complete date plan with perfect timing...")
        
        step6_start = time.time()
        
        step6_input = context_container.get_enhanced_output_for_next_step(5)
        optimizer = FinalIntelligenceOptimizer()
        final_plan = optimizer.optimize_complete_date_plan(step6_input)
        
        step6_time = time.time() - step6_start
        
        if not final_plan:
            handle_redis_processing_error(request_id, "Step 6 failed: Final optimization failed", 6)
            return
        
        context_container.store_step_output(6, final_plan)
        
        # Extract final info for preview
        date_section = final_plan.get("date", {})
        activities_count = len(date_section.get("activities", []))
        location = date_section.get("location_city", user_location)
        total_duration = date_section.get("total_duration", "Unknown")
        
        step6_preview = f"Complete! {activities_count} activities in {location} ({total_duration})"
        
        update_redis_progress(request_id, step_status="6", status_value="complete",
                       duration=step6_time, preview=step6_preview,
                       cultural_preview=f"🎯 Your perfect {location} date plan is ready! {activities_count} activities over {total_duration}")
        
        # ===== PIPELINE COMPLETION =====
        total_time = time.time() - pipeline_start
        
        # Build final response
        final_response = {
            "success": True,
            "message": "Complete 6-step dual profile cultural intelligence pipeline executed successfully",
            "final_date_plan": final_plan,
            "pipeline_performance": {
                "total_time_seconds": round(total_time, 1),
                "step_1_time": round(step1_time, 1),
                "step_2_time": round(step2_time, 1),
                "step_34_time": round(step34_time, 1),
                "step_5_time": round(step5_time, 1),
                "step_6_time": round(step6_time, 1),
                "steps_completed": 6,
                "pipeline_complete": True
            },
            "cultural_intelligence_summary": {
                "total_discoveries_analyzed": total_discoveries,
                "compatibility_score": comp_score,
                "venues_selected": venues_selected,
                "final_activities": activities_count,
                "location": location,
                "dual_profile_mode": True,
                "demo_ready": True
            },
            "redis_backend": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store final results in Redis (expires in 24 hours)
        if not redis_set_json(RESULT_KEY.format(request_id=request_id), final_response, 86400):
            logger.warning(f"Failed to store final results for {request_id}")
        else:
            logger.info(f"📦 Final results stored successfully for {request_id}")
        
        # CRITICAL: ALSO store results directly in progress data to prevent corruption
        current_progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        if current_progress:
            current_progress["final_date_plan_embedded"] = final_response
            current_progress["results_embedded"] = True
            current_progress["embedded_timestamp"] = datetime.now().isoformat()
            redis_set_json(PROGRESS_KEY.format(request_id=request_id), current_progress, 7200)
            logger.info(f"📦 EMBEDDED final results in progress data for {request_id}")
        
        # Mark as complete with final status
        update_redis_progress(request_id, status="complete", overall_progress=100, current_step=6)
        
        # CRITICAL: Mark completion IMMEDIATELY to prevent duplicate
        if redis_client:
            redis_client.setex(f"completed:{request_id}", 7200, "true")  # 2 hour marker
            logger.info(f"🏁 COMPLETION MARKER SET for {request_id}")
        
        logger.info(f"✅ Redis-powered DUAL PROFILE pipeline completed for {request_id} in {total_time:.1f}s - RESULTS STORED")
        
    except Exception as e:
        logger.error(f"Redis-powered dual profile pipeline processing failed for {request_id}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        handle_redis_processing_error(request_id, str(e), get_current_step_from_redis(request_id))
    
    finally:
        # ALWAYS clear the processing lock
        if redis_client:
            redis_client.delete(f"processing_lock:{request_id}")
            logger.info(f"🔓 Processing lock released for {request_id}")

def update_redis_progress(request_id: str, status: str = None, current_step: int = None, 
                         overall_progress: int = None, step_status: str = None, 
                         status_value: str = None, duration: float = None, 
                         preview: str = None, cultural_preview: str = None):
    """Update progress tracking in Redis"""
    try:
        # Get current progress from Redis
        progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        
        if not progress:
            logger.warning(f"Progress data not found in Redis for {request_id}")
            return
        
        # Update fields
        if status:
            progress["status"] = status
        if current_step is not None:
            progress["current_step"] = current_step
        if overall_progress is not None:
            progress["overall_progress"] = overall_progress
        else:
            # Auto-calculate overall progress
            if current_step:
                progress["overall_progress"] = min(int((current_step / 6) * 100), 95)
        
        if step_status and status_value:
            if step_status in progress["steps"]:
                progress["steps"][step_status]["status"] = status_value
                if duration is not None:
                    progress["steps"][step_status]["duration"] = round(duration, 1)
                if preview:
                    progress["steps"][step_status]["preview"] = preview
        
        if cultural_preview:
            progress["cultural_previews"].append(cultural_preview)
            # Keep only last 8 previews for better UX
            progress["cultural_previews"] = progress["cultural_previews"][-8:]
        
        # Update last modified time
        progress["last_updated"] = datetime.now().isoformat()
        
        # Save back to Redis (expires in 2 hours)
        redis_set_json(PROGRESS_KEY.format(request_id=request_id), progress, 7200)
        
    except Exception as e:
        logger.error(f"Failed to update Redis progress for {request_id}: {e}")

def check_redis_cancellation(request_id: str) -> bool:
    """Check if request has been cancelled via Redis"""
    try:
        progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        if progress and progress.get("status") == "cancelled":
            logger.info(f"Processing cancelled for {request_id}")
            return True
    except Exception as e:
        logger.error(f"Failed to check cancellation for {request_id}: {e}")
    return False

def get_current_step_from_redis(request_id: str) -> int:
    """Get current step from Redis progress"""
    try:
        progress = redis_get_json(PROGRESS_KEY.format(request_id=request_id))
        return progress.get("current_step", 0) if progress else 0
    except Exception:
        return 0

def handle_redis_processing_error(request_id: str, error_message: str, failed_step: int):
    """Handle processing errors with Redis state management"""
    try:
        logger.error(f"💥 HANDLING ERROR for {request_id} at step {failed_step}: {error_message}")
        
        # Update progress to show error
        update_redis_progress(request_id, status="error", current_step=failed_step)
        
        # Store error result in Redis
        error_response = {
            "success": False,
            "error": "Cultural intelligence processing failed",
            "detail": error_message,
            "failed_at_step": failed_step,
            "partial_results": "Processing stopped due to error",
            "redis_backend": True,
            "timestamp": datetime.now().isoformat()
        }
        
        redis_set_json(RESULT_KEY.format(request_id=request_id), error_response, 3600)
        logger.error(f"💥 ERROR RESULT STORED for {request_id}")
        
    except Exception as e:
        logger.error(f"Failed to handle Redis error for {request_id}: {e}")

# ===== APPLICATION STARTUP =====

@app.on_event("startup")
async def startup_event():
    """Application startup - test Redis connection"""
    logger.info("🚀 Starting ai-mor.me API v2.1 with Redis backend")
    
    redis_status = get_redis_status()
    if redis_status["connected"]:
        logger.info(f"✅ Redis connected: {redis_status['redis_version']}")
        logger.info(f"📊 Memory usage: {redis_status['used_memory_human']}")
    else:
        logger.warning("⚠️  Redis not available - some features may be limited")
    
    # Test API keys
    validation = settings.validate_required_keys()
    if validation["valid"]:
        logger.info("✅ API keys validated")
    else:
        logger.warning(f"⚠️  Missing API keys: {validation['missing_keys']}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown - cleanup Redis connections"""
    logger.info("🔽 Shutting down ai-mor.me API v2.1")
    
    try:
        if redis_client:
            redis_client.close()
            logger.info("✅ Redis connection closed")
    except Exception as e:
        logger.error(f"Redis shutdown error: {e}")

# ===== DEPLOYMENT READY =====

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "true").lower() == "true"
    )