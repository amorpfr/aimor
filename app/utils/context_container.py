# app/utils/context_container.py

from typing import Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ContextContainer:
    """
    Context preservation container for the 6-step cultural intelligence pipeline.
    
    Ensures original request context flows through all steps without loss.
    """
    
    def __init__(self, original_context: Optional[Dict] = None):
        """Initialize with original context from user request"""
        self.original_context = self._normalize_context(original_context or {})
        self.step_outputs = {}
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "steps_completed": [],
            "context_preserved": True
        }
        
    def _normalize_context(self, context: Dict) -> Dict:
        """Normalize and validate context with intelligent defaults"""
        normalized = {
            "location": str(context.get("location", "amsterdam")).lower().strip(),
            "time_of_day": str(context.get("time_of_day", "afternoon")).lower().strip(),
            "season": str(context.get("season", self._detect_current_season())).lower().strip(),
            "duration": str(context.get("duration", "4 hours")).strip(),
            "date_type": str(context.get("date_type", "first_date")).lower().strip()
        }
        
        # Validate critical fields
        if normalized["location"] in ["", "unknown", "none"]:
            logger.warning("No location provided, using 'amsterdam' as default")
            normalized["location"] = "amsterdam"
            
        logger.info(f"Context normalized: {normalized}")
        return normalized
    
    def _detect_current_season(self) -> str:
        """Detect current season as fallback"""
        try:
            current_month = datetime.now().month
            if current_month in [3, 4, 5]: return "spring"
            elif current_month in [6, 7, 8]: return "summer"
            elif current_month in [9, 10, 11]: return "autumn"
            else: return "winter"
        except Exception:
            return "spring"
    
    def get_context_for_step(self, step_number: int) -> Dict:
        """Get context for a specific step with step-specific enhancements"""
        
        base_context = self.original_context.copy()
        
        # Add step-specific context enhancements
        base_context["step_number"] = step_number
        base_context["pipeline_stage"] = f"step_{step_number}"
        
        return base_context
    
    def store_step_output(self, step_number: int, output: Dict) -> None:
        """Store step output and mark step as completed"""
        
        # Inject original context into step output
        if isinstance(output, dict):
            output["original_context"] = self.original_context.copy()
            
            # Also store in processing_metadata for backward compatibility
            if "processing_metadata" not in output:
                output["processing_metadata"] = {}
            output["processing_metadata"]["input_context"] = self.original_context.copy()
            output["processing_metadata"]["context_preserved"] = True
        
        self.step_outputs[f"step_{step_number}"] = output
        self.metadata["steps_completed"].append(step_number)
        
        logger.info(f"Step {step_number} output stored with preserved context")
    
    def get_step_output(self, step_number: int) -> Optional[Dict]:
        """Get output from a specific step"""
        return self.step_outputs.get(f"step_{step_number}")
    
    def get_enhanced_output_for_next_step(self, current_step: int) -> Dict:
        """Get enhanced output for the next step with guaranteed context"""
        
        current_output = self.get_step_output(current_step)
        if not current_output:
            raise ValueError(f"Step {current_step} output not found")
        
        # Ensure context is present and accessible
        enhanced_output = current_output.copy()
        
        # Multiple ways to access context for robustness
        enhanced_output["original_context"] = self.original_context.copy()
        enhanced_output["preserved_context"] = self.original_context.copy()
        
        if "processing_metadata" not in enhanced_output:
            enhanced_output["processing_metadata"] = {}
        enhanced_output["processing_metadata"]["input_context"] = self.original_context.copy()
        enhanced_output["processing_metadata"]["context_container_used"] = True
        
        return enhanced_output
    
    def validate_context_preservation(self) -> Dict:
        """Validate that context has been preserved throughout pipeline"""
        
        issues = []
        
        # Check each step output for context preservation
        for step_key, output in self.step_outputs.items():
            if not isinstance(output, dict):
                continue
                
            # Check if original_context exists
            if "original_context" not in output:
                issues.append(f"{step_key}: missing original_context")
                continue
            
            # Check if context matches original
            preserved_context = output["original_context"]
            for key, original_value in self.original_context.items():
                if preserved_context.get(key) != original_value:
                    issues.append(f"{step_key}: context mismatch for {key}")
        
        return {
            "context_preserved": len(issues) == 0,
            "issues": issues,
            "steps_completed": len(self.step_outputs),
            "original_context": self.original_context
        }
    
    def get_final_context_for_step6(self) -> Dict:
        """Get complete context specifically formatted for Step 6 consumption"""
        
        # Get the latest step output (should be Step 5)
        latest_step = max(self.metadata["steps_completed"]) if self.metadata["steps_completed"] else 0
        latest_output = self.get_step_output(latest_step) if latest_step > 0 else {}
        
        # Build comprehensive context for Step 6
        final_context = {
            # Original user context (GUARANTEED to be present)
            "original_context": self.original_context.copy(),
            
            # Enhanced context for Step 6
            "location": self.original_context["location"],
            "time_of_day": self.original_context["time_of_day"], 
            "season": self.original_context["season"],
            "duration": self.original_context["duration"],
            "date_type": self.original_context["date_type"],
            
            # Pipeline metadata
            "pipeline_metadata": {
                "steps_completed": self.metadata["steps_completed"],
                "context_container_used": True,
                "context_preservation_validated": True
            },
            
            # Latest step output for cultural intelligence
            "latest_step_output": latest_output
        }
        
        logger.info(f"Final context prepared for Step 6: location={final_context['location']}, time={final_context['time_of_day']}, season={final_context['season']}")
        
        return final_context

# Convenience function for creating context containers
def create_context_container(request_context: Optional[Dict] = None) -> ContextContainer:
    """Create a context container for the pipeline"""
    return ContextContainer(request_context)