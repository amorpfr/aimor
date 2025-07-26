# app/services/date_intelligence_engine.py

import openai
import logging
import json
from typing import Dict, Optional, List
from utils.config import settings
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)

class DateIntelligenceEngine:
    """
    STEP 3-4: Date Intelligence Engine - Optimized for OpenAI Intelligence
    
    Creates culturally intelligent date plans with QLOO-READY parameters
    letting OpenAI handle the sophisticated reasoning.
    """
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY or "dummy_key"
        self.model = settings.OPENAI_MODEL or "gpt-4o-mini"
        
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.client_available = True
        except Exception as e:
            logger.error(f"OpenAI client initialization failed: {e}")
            self.client_available = False
    
    def create_intelligent_date_plan(self, enriched_profile_a: Dict, enriched_profile_b: Dict, context: Dict = None) -> Dict:
        """
        Create culturally intelligent date plan with QLOO-READY venue parameters
        """
        
        if not self.client_available:
            logger.error("OpenAI client not available")
            return self._fallback_date_plan("openai_unavailable")
        
        # Robust context handling
        context = self._enhance_context(context or {})
        
        # Create the QLOO-optimized prompt
        for attempt in range(3):
            try:
                prompt = self._build_qloo_ready_prompt(
                    enriched_profile_a, enriched_profile_b, context
                )
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are the world's most sophisticated dating AI that creates date plans with precise Qloo API parameters for instant venue discovery. Your output must be perfectly formatted for Qloo Insights API calls."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2500,
                    timeout=45
                )
                
                result = response.choices[0].message.content.strip()
                analysis = self._parse_date_intelligence_response(result)
                
                if analysis and self._validate_qloo_ready_structure(analysis):
                    # Add processing metadata
                    analysis["processing_metadata"] = {
                        "input_profiles": 2,
                        "cultural_discoveries_analyzed": (
                            len(enriched_profile_a.get("cross_domain_discoveries", {}).get("music_artists", [])) +
                            len(enriched_profile_b.get("cross_domain_discoveries", {}).get("music_artists", []))
                        ),
                        "context_factors": len([v for v in context.values() if v]),
                        "qloo_queries_generated": len(analysis.get("qloo_ready_queries", [])),
                        "attempt_number": attempt + 1,
                        "intelligence_level": "qloo_optimized_cultural_psychology",
                        "timestamp": self._safe_timestamp()
                    }
                    analysis["original_context"] = context
                    analysis["processing_metadata"]["input_context"] = context
                    
                    logger.info(f"Successfully created Qloo-ready date plan on attempt {attempt + 1}")
                    return analysis
                
            except openai.RateLimitError:
                logger.warning(f"Rate limit hit on attempt {attempt + 1}")
                if attempt < 2:
                    import time
                    time.sleep(2 ** attempt)
                continue
                
            except Exception as e:
                logger.error(f"Date intelligence error on attempt {attempt + 1}: {e}")
                if attempt < 2:
                    continue
        
        # All attempts failed
        logger.error("All Qloo-ready date intelligence attempts failed")
        return self._fallback_date_plan("openai_failed")
    
    def _enhance_context(self, context: Dict) -> Dict:
        """Enhance context with intelligent defaults"""
        
        enhanced = {
            "location": context.get("location", "amsterdam").lower(),
            "duration": context.get("duration", "4 hours"),
            "time_of_day": context.get("time_of_day", "afternoon"),
            "season": context.get("season", self._detect_current_season()),
            "date_type": context.get("date_type", "first_date"),
            "weather_context": self._get_weather_context(context.get("season")),
            "cultural_setting": self._get_cultural_setting(context.get("location", "amsterdam")),
            "qloo_location_query": self._format_qloo_location(context.get("location", "amsterdam"))
        }
        
        return enhanced
    
    def _format_qloo_location(self, location: str) -> str:
        """Format location for Qloo filter.location.query parameter"""
        location_mappings = {
            "amsterdam": "Amsterdam, Netherlands",
            "rotterdam": "Rotterdam, Netherlands", 
            "paris": "Paris, France",
            "london": "London, United Kingdom",
            "new_york": "New York City, New York",
            "nyc": "New York City, New York"
        }
        
        return location_mappings.get(location.lower(), location.title())
    
    def _detect_current_season(self) -> str:
        """Detect current season intelligently"""
        try:
            current_month = datetime.now().month
            if current_month in [3, 4, 5]: return "spring"
            elif current_month in [6, 7, 8]: return "summer" 
            elif current_month in [9, 10, 11]: return "autumn"
            else: return "winter"
        except Exception:
            return "spring"
    
    def _get_weather_context(self, season: str) -> Dict:
        """Get weather-aware recommendations"""
        weather_contexts = {
            "spring": {"conditions": "mild, occasional rain", "indoor_outdoor_balance": "60% outdoor preferred"},
            "summer": {"conditions": "warm, longer daylight", "indoor_outdoor_balance": "80% outdoor preferred"},
            "autumn": {"conditions": "crisp, cozy atmosphere", "indoor_outdoor_balance": "40% outdoor preferred"},
            "winter": {"conditions": "cold, shorter daylight", "indoor_outdoor_balance": "20% outdoor preferred"}
        }
        return weather_contexts.get(season, weather_contexts["spring"])
    
    def _get_cultural_setting(self, location: str) -> Dict:
        """Get location-specific cultural context"""
        cultural_settings = {
            "amsterdam": {
                "culture": "Direct, authentic, work-life balance focused",
                "conversation_topics": ["travel", "sustainability", "art", "local discoveries"]
            }
        }
        
        return cultural_settings.get(location.lower(), {
            "culture": "Local authentic culture with international influences",
            "conversation_topics": ["local culture", "travel", "personal interests", "discoveries"]
        })
    
    def _build_qloo_ready_prompt(self, profile_a: Dict, profile_b: Dict, context: Dict) -> str:
        """Build prompt that leverages OpenAI intelligence for Qloo optimization"""
        
        # Extract discovery data for OpenAI to analyze intelligently
        def get_discovery_sample(profile, max_per_category=3):
            discoveries = profile.get("cross_domain_discoveries", {})
            sample = {}
            for category, items in discoveries.items():
                if isinstance(items, list) and items and category != "discovery_confidence":
                    sample[category] = []
                    for item in items[:max_per_category]:
                        if isinstance(item, dict):
                            sample[category].append({
                                "id": item.get('id', 'unknown'),
                                "name": item.get('name', 'unknown'),
                                "description": item.get('description', ''),
                                "cultural_context": item.get('cultural_context', '')
                            })
            return sample
        
        profile_a_data = {
            "explicit_interests": profile_a.get("input_explicit_interests", {}),
            "discoveries": get_discovery_sample(profile_a),
            "cultural_sophistication": profile_a.get("enriched_cultural_profile", {}).get("cultural_intelligence", {}).get("sophistication_level", 0.5)
        }
        
        profile_b_data = {
            "explicit_interests": profile_b.get("input_explicit_interests", {}),
            "discoveries": get_discovery_sample(profile_b),
            "cultural_sophistication": profile_b.get("enriched_cultural_profile", {}).get("cultural_intelligence", {}).get("sophistication_level", 0.5)
        }
        
        prompt = f"""You are the world's most sophisticated dating AI. Create an intelligent date plan with PERFECT QLOO API PARAMETERS.

PERSON A PROFILE:
{json.dumps(profile_a_data, indent=2)}

PERSON B PROFILE:
{json.dumps(profile_b_data, indent=2)}

CONTEXT:
Location: {context['qloo_location_query']}
Duration: {context['duration']}
Season: {context['season']} ({context['weather_context']['conditions']})
Weather Balance: {context['weather_context']['indoor_outdoor_balance']}

YOUR INTELLIGENCE TASKS:
1. Extract entity IDs from their discoveries for Qloo signals
2. Choose venue tags based on their personalities (coffee, art, restaurant, etc.)
3. Set price levels (1-4) based on cultural sophistication
4. Create 2-3 activities with natural progression

QLOO REQUIREMENTS:
- filter.type: "urn:entity:place" (required)
- filter.location.query: "{context['qloo_location_query']}" (required)
- signal.interests.entities: comma-separated entity IDs from discoveries
- filter.tags: venue type tags like "coffee,cozy" or "art,gallery"
- filter.price_level.min/max: 1-4 based on sophistication
- take: 5

Return ONLY valid JSON:
{{
    "compatibility_insights": {{
        "overall_compatibility": <0.0-1.0>,
        "shared_cultural_patterns": ["pattern1", "pattern2"],
        "connection_bridges": ["bridge1", "bridge2"]
    }},
    
    "intelligent_date_plan": {{
        "theme": "<creative theme>",
        "total_duration": "{context['duration']}",
        
        "activities": [
            {{
                "sequence": 1,
                "name": "<activity name>",
                "type": "<venue type>",
                "duration": "<time>",
                "cultural_reasoning": "<why this creates connection>",
                "conversation_catalysts": ["topic1", "topic2"],
                
                "qloo_parameters": {{
                    "filter.type": "urn:entity:place",
                    "filter.location.query": "{context['qloo_location_query']}",
                    "signal.interests.entities": "<entity IDs from discoveries>",
                    "filter.tags": "<venue tags>",
                    "filter.price_level.min": <1-4>,
                    "filter.price_level.max": <1-4>,
                    "filter.popularity.min": <0.0-1.0>,
                    "take": 5
                }}
            }},
            {{
                "sequence": 2,
                "name": "<second activity>",
                "type": "<different venue type>",
                "duration": "<time>",
                "cultural_reasoning": "<progression reasoning>",
                "conversation_catalysts": ["topic1", "topic2"],
                
                "qloo_parameters": {{
                    "filter.type": "urn:entity:place",
                    "filter.location.query": "{context['qloo_location_query']}",
                    "signal.interests.entities": "<entity IDs>",
                    "filter.tags": "<different tags>",
                    "filter.price_level.min": <number>,
                    "filter.price_level.max": <number>,
                    "filter.popularity.min": <float>,
                    "take": 5
                }}
            }}
        ]
    }},
    
    "qloo_ready_queries": [
        {{
            "activity_name": "<activity 1>",
            "parameters": {{
                "filter.type": "urn:entity:place",
                "filter.location.query": "{context['qloo_location_query']}",
                "signal.interests.entities": "<entities>",
                "filter.tags": "<tags>",
                "filter.price_level.min": <number>,
                "filter.price_level.max": <number>,
                "filter.popularity.min": <float>,
                "take": 5
            }}
        }},
        {{
            "activity_name": "<activity 2>",
            "parameters": {{
                "filter.type": "urn:entity:place",
                "filter.location.query": "{context['qloo_location_query']}",
                "signal.interests.entities": "<entities>",
                "filter.tags": "<tags>",
                "filter.price_level.min": <number>,
                "filter.price_level.max": <number>,
                "filter.popularity.min": <float>,
                "take": 5
            }}
        }}
    ],
    
    "cultural_intelligence_reasoning": {{
        "entity_selection_logic": "<why these entities>",
        "venue_psychology_optimization": "<why these venues work>"
    }}
}}

Be intelligent about entity selection and venue matching."""
        
        return prompt
    
    def _parse_date_intelligence_response(self, result: str) -> Optional[Dict]:
        """Parse JSON response with fallbacks"""
        if not result:
            return None
        
        parsing_attempts = [
            result,
            result.strip(),
            result.strip().strip('```json').strip('```'),
            result.split('```json')[1].split('```')[0] if '```json' in result else result,
        ]
        
        for attempt_text in parsing_attempts:
            try:
                return json.loads(attempt_text)
            except json.JSONDecodeError:
                continue
        
        logger.error(f"JSON parsing failed: {result[:200]}...")
        return None
    
    def _validate_qloo_ready_structure(self, analysis: Dict) -> bool:
        """Validate Qloo-ready structure"""
        required_keys = [
            "compatibility_insights",
            "intelligent_date_plan", 
            "qloo_ready_queries"
        ]
        
        if not all(key in analysis for key in required_keys):
            missing = [k for k in required_keys if k not in analysis]
            logger.error(f"Missing required keys: {missing}")
            return False
        
        activities = analysis.get("intelligent_date_plan", {}).get("activities", [])
        if not activities:
            logger.error("No activities in date plan")
            return False
        
        # Check Qloo parameters
        for i, activity in enumerate(activities):
            qloo_params = activity.get("qloo_parameters", {})
            if not qloo_params.get("filter.type") or not qloo_params.get("filter.location.query"):
                logger.error(f"Activity {i+1} missing essential Qloo parameters")
                return False
        
        queries = analysis.get("qloo_ready_queries", [])
        if not queries:
            logger.error("No Qloo queries generated")
            return False
        
        logger.info(f"✅ Validated: {len(activities)} activities, {len(queries)} queries")
        return True
    
    def _safe_timestamp(self) -> str:
        """Generate safe timestamp"""
        try:
            return datetime.now().isoformat()
        except Exception:
            return "unknown"
    
    def _fallback_date_plan(self, error_reason: str) -> Dict:
        """Intelligent fallback when OpenAI fails"""
        return {
            "success": False,
            "error": "date_intelligence_failed", 
            "error_reason": error_reason,
            "compatibility_insights": {
                "overall_compatibility": 0.6,
                "shared_cultural_patterns": ["General compatibility"],
                "connection_bridges": ["Common interests assumed"]
            },
            "intelligent_date_plan": {
                "theme": "Amsterdam Discovery",
                "total_duration": "4 hours",
                "activities": [
                    {
                        "sequence": 1,
                        "name": "Cozy Café",
                        "type": "cafe",
                        "duration": "2 hours",
                        "cultural_reasoning": "Intimate conversation starter",
                        "qloo_parameters": {
                            "filter.type": "urn:entity:place",
                            "filter.location.query": "Amsterdam, Netherlands",
                            "filter.tags": "coffee,cafe",
                            "filter.price_level.min": 2,
                            "filter.price_level.max": 3,
                            "take": 5
                        }
                    }
                ]
            },
            "qloo_ready_queries": [
                {
                    "activity_name": "Cozy Café",
                    "parameters": {
                        "filter.type": "urn:entity:place",
                        "filter.location.query": "Amsterdam, Netherlands",
                        "filter.tags": "coffee,cafe",
                        "filter.price_level.min": 2,
                        "filter.price_level.max": 3,
                        "take": 5
                    }
                }
            ],
            "processing_metadata": {
                "fallback_used": True,
                "error_reason": error_reason,
                "timestamp": self._safe_timestamp()
            }
        }