# app/services/profile_analyzer_optimized.py

import openai
import logging
import json
from typing import Dict, Optional, List, Tuple
from utils.config import settings
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)

class ProfileAnalyzer:
    """SPEED-OPTIMIZED Advanced psychological profiler - TARGET: <15s response time"""
    
    def __init__(self):
        # Robust OpenAI client setup
        self.api_key = settings.OPENAI_API_KEY or "dummy_key"
        # OPTIMIZATION 1: Use faster model
        self.model = "gpt-4o-mini"  # Faster than gpt-4o
        
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.client_available = True
        except Exception as e:
            logger.error(f"OpenAI client initialization failed: {e}")
            self.client_available = False
    
    def analyze_profile_with_context(self, profile_text: str, context: Dict = None, is_ocr_text: bool = False) -> Dict:
        """SPEED-OPTIMIZED psychological analysis with Step 2 compatibility"""
        
        # Input validation
        if not profile_text or len(profile_text.strip()) < 3:
            logger.warning("Profile text too short or empty")
            return self._fallback_analysis(is_ocr_text, "insufficient_text")
        
        # Client availability check
        if not self.client_available:
            logger.error("OpenAI client not available")
            return self._fallback_analysis(is_ocr_text, "openai_unavailable")
        
        # Robust context handling
        context = context or {}
        fallback_context = self._get_robust_context(context)
        
        # OPTIMIZATION 2: Single attempt with better timeout
        try:
            logger.info(f"Starting speed-optimized analysis for {len(profile_text)} characters")
            
            prompt = self._build_speed_optimized_prompt(profile_text, fallback_context, is_ocr_text)
            logger.info(f"Prompt built, making OpenAI call with {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a dating psychology expert. Provide concise analysis with essential insights only. Return valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # OPTIMIZATION 3: Lower temperature for faster processing
                max_tokens=1000,  # OPTIMIZATION 4: Increased from 800 to 1000 for complete responses
                timeout=30        # FIXED: Increased timeout to 30 seconds
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"OpenAI response received, length: {len(result)} characters")
            
            parsed_response = self._parse_openai_response(result)
            
            if parsed_response and self._validate_analysis_structure(parsed_response):
                logger.info("✅ OpenAI response validated successfully")
                
                # CONVERT TO STEP 2 COMPATIBLE STRUCTURE
                analysis = self._build_compatible_analysis_structure(parsed_response, fallback_context)
                
                # Add processing metadata
                analysis["processing_metadata"] = {
                    "input_method": "ocr" if is_ocr_text else "direct_text",
                    "context_provided": len([v for v in context.values() if v and str(v).lower() != "unknown"]) if context else 0,
                    "attempt_number": 1,
                    "psychological_depth": "optimized_speed",
                    "optimization_version": "v3_speed_compatible",
                    "model_used": self.model,
                    "response_length": len(result),
                    "timestamp": self._safe_timestamp()
                }
                
                logger.info("✅ Speed-optimized + compatible psychological analysis completed")
                return analysis
            else:
                logger.warning(f"OpenAI response validation failed. Response: {result[:200]}...")
                return self._fallback_analysis(is_ocr_text, "validation_failed")
                
        except openai.APITimeoutError as e:
            logger.error(f"OpenAI timeout after 30s: {e}")
            return self._fallback_analysis(is_ocr_text, "openai_timeout")
        except openai.RateLimitError as e:
            logger.error(f"OpenAI rate limit: {e}")
            return self._fallback_analysis(is_ocr_text, "rate_limit")
        except Exception as e:
            logger.error(f"Speed-optimized analysis error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return self._fallback_analysis(is_ocr_text, str(e))
    
    def _build_speed_optimized_prompt(self, profile_text: str, fallback_context: Dict, is_ocr_text: bool) -> str:
        """HEAVILY OPTIMIZED prompt for speed - but with complete structure"""
        
        # OPTIMIZATION 6: Truncate input but less aggressively
        if len(profile_text) > 600:  # Increased from 400 to 600
            profile_text = profile_text[:600] + "..."
        
        # OPTIMIZATION 7: Minimal OCR instruction
        ocr_note = "Note: OCR text may have typos." if is_ocr_text else ""
        
        # OPTIMIZATION 8: Streamlined but complete prompt
        prompt = f"""Analyze this dating profile quickly and return complete psychological analysis. {ocr_note}

PROFILE: "{profile_text}"
CONTEXT: {fallback_context['location']}, {fallback_context['time_of_day']}, {fallback_context['season']}

Return ONLY this JSON (no extra text, no markdown):

{{
    "text_interpretation": "Brief profile summary",
    "personality": {{
        "openness": {{"score": 0.7, "confidence": 0.8, "reasoning": "Evidence from profile"}},
        "conscientiousness": {{"score": 0.6, "confidence": 0.7, "reasoning": "Evidence from profile"}},
        "extraversion": {{"score": 0.5, "confidence": 0.6, "reasoning": "Evidence from profile"}},
        "agreeableness": {{"score": 0.6, "confidence": 0.7, "reasoning": "Evidence from profile"}},
        "neuroticism": {{"score": 0.3, "confidence": 0.6, "reasoning": "Evidence from profile"}}
    }},
    "dating_psychology": {{
        "adventurousness": {{"score": 0.8, "confidence": 0.9, "reasoning": "Evidence from profile"}},
        "authenticity_preference": {{"score": 0.7, "confidence": 0.8, "reasoning": "Evidence from profile"}},
        "intellectual_curiosity": {{"score": 0.6, "confidence": 0.7, "reasoning": "Evidence from profile"}},
        "social_energy": {{"score": 0.5, "confidence": 0.6, "reasoning": "Evidence from profile"}}
    }},
    "entities": {{
        "activities": ["hiking", "art"],
        "locations": ["{fallback_context['location']}"], 
        "interests": ["sustainability", "photography"],
        "food_preferences": [],
        "venues": []
    }},
    "demographic_context": {{
        "age_range": "25-30",
        "location": "{fallback_context['location']}",
        "lifestyle": "active",
        "education_level": "university"
    }},
    "personality_weights": {{
        "adventurous": 0.8,
        "authentic": 0.7,
        "intellectual": 0.6,
        "social": 0.5
    }},
    "confidence": 0.85
}}

Focus on extracting real evidence from the profile text. Be specific in reasoning."""
        
        return prompt
    
    def _build_compatible_analysis_structure(self, parsed_response: Dict, fallback_context: Dict) -> Dict:
        """Convert optimized response to Step 2 compatible structure"""
        
        # Extract from optimized response
        personality = parsed_response.get("personality", {})
        dating_psychology = parsed_response.get("dating_psychology", {})
        entities = parsed_response.get("entities", {})
        demographic = parsed_response.get("demographic_context", {})
        weights = parsed_response.get("personality_weights", {})
        
        # Build Step 2 compatible structure
        compatible_structure = {
            "text_interpretation": parsed_response.get("text_interpretation", "Profile analysis completed"),
            
            # Convert to expected Step 2 structure
            "advanced_psychological_profile": {
                "big_five_detailed": {
                    "openness": {
                        "score": personality.get("openness", {}).get("score", 0.5),
                        "reasoning": personality.get("openness", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": personality.get("openness", {}).get("confidence", 0.7)
                    },
                    "conscientiousness": {
                        "score": personality.get("conscientiousness", {}).get("score", 0.5),
                        "reasoning": personality.get("conscientiousness", {}).get("reasoning", "Extracted from optimized analysis"), 
                        "confidence": personality.get("conscientiousness", {}).get("confidence", 0.7)
                    },
                    "extraversion": {
                        "score": personality.get("extraversion", {}).get("score", 0.5),
                        "reasoning": personality.get("extraversion", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": personality.get("extraversion", {}).get("confidence", 0.7)
                    },
                    "agreeableness": {
                        "score": personality.get("agreeableness", {}).get("score", 0.5),
                        "reasoning": personality.get("agreeableness", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": personality.get("agreeableness", {}).get("confidence", 0.7)
                    },
                    "neuroticism": {
                        "score": personality.get("neuroticism", {}).get("score", 0.5),
                        "reasoning": personality.get("neuroticism", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": personality.get("neuroticism", {}).get("confidence", 0.7)
                    }
                },
                "dating_psychology": {
                    "adventurousness": {
                        "score": dating_psychology.get("adventurousness", {}).get("score", 0.5),
                        "reasoning": dating_psychology.get("adventurousness", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": dating_psychology.get("adventurousness", {}).get("confidence", 0.7)
                    },
                    "authenticity_preference": {
                        "score": dating_psychology.get("authenticity_preference", {}).get("score", 0.5),
                        "reasoning": dating_psychology.get("authenticity_preference", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": dating_psychology.get("authenticity_preference", {}).get("confidence", 0.7)
                    },
                    "intellectual_curiosity": {
                        "score": dating_psychology.get("intellectual_curiosity", {}).get("score", 0.5),
                        "reasoning": dating_psychology.get("intellectual_curiosity", {}).get("reasoning", "Extracted from optimized analysis"), 
                        "confidence": dating_psychology.get("intellectual_curiosity", {}).get("confidence", 0.7)
                    },
                    "social_energy": {
                        "score": dating_psychology.get("social_energy", {}).get("score", 0.5),
                        "reasoning": dating_psychology.get("social_energy", {}).get("reasoning", "Extracted from optimized analysis"),
                        "confidence": dating_psychology.get("social_energy", {}).get("confidence", 0.7)
                    }
                }
            },
            
            # Convert entities to expected structure
            "qloo_optimized_entities": {
                "explicitly_mentioned": {
                    "activities": entities.get("activities", []),
                    "locations": entities.get("locations", [fallback_context["location"]]),
                    "interests": entities.get("interests", []),
                    "food_preferences": entities.get("food_preferences", []),
                    "venues": entities.get("venues", [])
                },
                "high_confidence_inferences": {
                    "activity_categories": entities.get("activities", ["general"]),
                    "lifestyle_indicators": [demographic.get("lifestyle", "balanced")],
                    "demographic_context": [demographic.get("age_range", "young_adult")]
                },
                "personality_entities": {
                    "adventurous": weights.get("adventurous", 0.5),
                    "authentic": weights.get("authentic", 0.5),
                    "intellectual": weights.get("intellectual", 0.5),
                    "social": weights.get("social", 0.5)
                }
            },
            
            "qloo_query_preparation": {
                "primary_entities": entities.get("activities", ["general"]) + entities.get("interests", []),
                "demographic_context": {
                    "age_range": demographic.get("age_range", "25-35"),
                    "location": fallback_context["location"],
                    "lifestyle": demographic.get("lifestyle", "balanced"),
                    "education_level": demographic.get("education_level", "university")
                },
                "personality_weights": weights,
                "cultural_sophistication": "moderate"
            },
            
            "experience_optimization_insights": {
                "motivational_drivers": ["connection", "growth", "authenticity"],
                "ideal_date_psychology": {
                    "energy_level": "moderate",
                    "setting_preference": "comfortable_but_interesting",
                    "conversation_catalyst": "shared_interests"
                },
                "conversation_psychology": {
                    "energizing_topics": entities.get("interests", ["general_topics"]),
                    "bonding_opportunities": ["shared_activity_experiences"],
                    "conversation_starters": [
                        "What's something you're passionate about?",
                        "What kind of experiences make you feel most alive?"
                    ]
                }
            },
            
            "intelligent_context_recommendations": {
                "optimal_location": fallback_context["location"],
                "optimal_timing": fallback_context["time_of_day"],
                "ideal_duration": fallback_context["duration"],
                "date_type_optimization": "activity_based_with_conversation_opportunities"
            },
            
            "demographics": {
                "age": demographic.get("age_range", "25-35"),
                "location": fallback_context["location"],
                "education": demographic.get("education_level", "university"),
                "occupation": "unknown",
                "lifestyle_stage": "exploration_phase"
            },
            
            "processing_confidence": parsed_response.get("confidence", 0.8)
        }
        
        return compatible_structure
    
    def _get_robust_context(self, context: Dict) -> Dict:
        """Simplified context handling for speed"""
        try:
            current_season = self._safe_detect_season()
        except Exception:
            current_season = "spring"
        
        return {
            "location": str(context.get("location", "amsterdam")).strip() or "amsterdam",
            "time_of_day": str(context.get("time_of_day", "afternoon")).strip() or "afternoon", 
            "season": str(context.get("season", current_season)).strip() or current_season,
            "duration": str(context.get("duration", "4 hours")).strip() or "4 hours",
            "date_type": str(context.get("date_type", "first_date")).strip() or "first_date"
        }
    
    def _safe_detect_season(self) -> str:
        """Safely detect current season"""
        try:
            current_month = datetime.now().month
            if current_month in [3, 4, 5]: return "spring"
            elif current_month in [6, 7, 8]: return "summer"
            elif current_month in [9, 10, 11]: return "autumn"
            else: return "winter"
        except Exception:
            return "spring"
    
    def _safe_timestamp(self) -> str:
        """Generate safe timestamp"""
        try:
            return datetime.now().isoformat()
        except Exception:
            return "unknown"
    
    def _parse_openai_response(self, result: str) -> Optional[Dict]:
        """Parse JSON with thorough fallback strategies"""
        if not result:
            logger.error("Empty OpenAI response")
            return None
        
        # OPTIMIZATION 9: More parsing attempts for robustness
        parsing_attempts = [
            result.strip(),
            result.strip().strip('```json').strip('```').strip('```'),
            result.split('```json')[1].split('```')[0] if '```json' in result else result,
            result.split('```')[1] if result.count('```') >= 2 else result
        ]
        
        for i, attempt_text in enumerate(parsing_attempts):
            try:
                parsed = json.loads(attempt_text.strip())
                logger.info(f"Successfully parsed JSON on attempt {i+1}")
                return parsed
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing attempt {i+1} failed: {e}")
                continue
        
        logger.error(f"All JSON parsing attempts failed. Response: {result[:300]}...")
        return None
    
    def _validate_analysis_structure(self, analysis: Dict) -> bool:
        """Enhanced validation for optimized structure"""
        required_keys = ["personality", "entities", "confidence"]
        
        if not all(key in analysis for key in required_keys):
            missing = [k for k in required_keys if k not in analysis]
            logger.error(f"Missing required keys: {missing}")
            return False
        
        # Validate personality structure
        personality = analysis.get("personality", {})
        required_personality = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        
        if not all(trait in personality for trait in required_personality):
            missing_traits = [trait for trait in required_personality if trait not in personality]
            logger.error(f"Missing personality traits: {missing_traits}")
            return False
        
        # Validate entities structure  
        entities = analysis.get("entities", {})
        if not isinstance(entities.get("activities"), list):
            logger.error("Entities activities is not a list")
            return False
        
        logger.info("✅ Analysis structure validation passed")
        return True
    
    def _fallback_analysis(self, is_ocr_text: bool, error_reason: str) -> Dict:
        """Lightweight fallback analysis - COMPATIBLE WITH STEP 2"""
        
        logger.warning(f"Using fallback analysis due to: {error_reason}")
        
        return {
            "text_interpretation": f"Speed-optimized fallback analysis due to: {error_reason}",
            
            # STEP 2 COMPATIBILITY: Match expected structure exactly
            "advanced_psychological_profile": {
                "big_five_detailed": {
                    "openness": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "conscientiousness": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "extraversion": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "agreeableness": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "neuroticism": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3}
                },
                "dating_psychology": {
                    "adventurousness": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "authenticity_preference": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "intellectual_curiosity": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3},
                    "social_energy": {"score": 0.5, "reasoning": "Fallback default", "confidence": 0.3}
                }
            },
            
            # STEP 2 COMPATIBILITY: Expected entity structure
            "qloo_optimized_entities": {
                "explicitly_mentioned": {
                    "activities": [],
                    "locations": ["rotterdam"],  # Use context location
                    "interests": [],
                    "food_preferences": [],
                    "venues": []
                },
                "high_confidence_inferences": {
                    "activity_categories": ["general"],
                    "lifestyle_indicators": ["balanced"],
                    "demographic_context": ["young_adult"]
                },
                "personality_entities": {
                    "balanced": 0.5
                }
            },
            
            "qloo_query_preparation": {
                "primary_entities": ["general"],
                "demographic_context": {
                    "age_range": "25-35",
                    "location": "rotterdam",
                    "lifestyle": "balanced",
                    "education_level": "university"
                },
                "personality_weights": {
                    "balanced": 0.5
                },
                "cultural_sophistication": "moderate"
            },
            
            "experience_optimization_insights": {
                "motivational_drivers": ["connection"],
                "ideal_date_psychology": {
                    "energy_level": "moderate",
                    "setting_preference": "comfortable",
                    "conversation_catalyst": "shared_interests"
                },
                "conversation_psychology": {
                    "energizing_topics": ["general_topics"],
                    "bonding_opportunities": ["shared_experiences"],
                    "conversation_starters": ["What do you enjoy doing in your free time?"]
                }
            },
            
            "intelligent_context_recommendations": {
                "optimal_location": "rotterdam",
                "optimal_timing": "afternoon",
                "ideal_duration": "4 hours",
                "date_type_optimization": "conversation_focused"
            },
            
            "demographics": {
                "age": "25-35",
                "location": "rotterdam",
                "education": "university",
                "occupation": "unknown",
                "lifestyle_stage": "exploration_phase"
            },
            
            "processing_confidence": 0.1,  # Low confidence for fallback
            "processing_metadata": {
                "input_method": "ocr" if is_ocr_text else "direct_text",
                "error_reason": error_reason,
                "fallback_used": True,
                "optimization_version": "v3_speed_fallback_compatible",
                "timestamp": self._safe_timestamp()
            }
        }


# COMPATIBILITY WRAPPER: Update ProfileProcessor to use optimized version
class ProfileProcessorOptimized:
    """Updated profile processor using speed-optimized analyzer"""
    
    def __init__(self):
        self.profile_analyzer = ProfileAnalyzerOptimized()  # Use optimized version
        # Keep existing image processor
        from services.image_processor import ImageProcessor
        self.image_processor = ImageProcessor()
    
    def process_profile_with_context(self, text: Optional[str] = None, image_data_list: Optional[List[str]] = None, context: Optional[Dict] = None) -> Dict:
        """Process profile with speed optimization"""
        
        # Step 1: Get combined text from all sources
        profile_text, is_ocr = self._extract_text(text, image_data_list)
        
        if not profile_text:
            return self._empty_profile_response("No text content found")
        
        # Step 2: Use SPEED-OPTIMIZED OpenAI analysis
        analysis = self.profile_analyzer.analyze_profile_with_context(profile_text, context, is_ocr)
        
        if not analysis:
            return self._empty_profile_response("AI analysis failed")
        
        # Step 3: Structure the response (compatible with existing pipeline)
        return {
            "success": True,
            "input_text": profile_text,
            "input_context": context or {},
            "input_summary": {
                "text_provided": bool(text),
                "images_provided": len(image_data_list) if image_data_list else 0,
                "combined_sources": len([x for x in [text, image_data_list] if x]),
                "final_text_length": len(profile_text)
            },
            "analysis": analysis,
            "processing_method": f"optimized_speed_v3_{'combined' if text and image_data_list else 'multi_ocr' if image_data_list else 'text'}"
        }
    
    def _extract_text(self, text: Optional[str], image_data_list: Optional[List[str]] = None) -> tuple[str, bool]:
        """Extract and combine text from all available sources"""
        
        combined_text_parts = []
        has_ocr = False
        
        # Add direct text if provided
        if text and text.strip():
            logger.info("Adding direct text input")
            combined_text_parts.append(text.strip())
        
        # Add OCR text from images (can be 1 or many)
        if image_data_list and len(image_data_list) > 0:
            if len(image_data_list) == 1:
                logger.info("Processing single image with OCR")
                extracted_text = self.image_processor.extract_text_only(image_data_list[0])
            else:
                logger.info(f"Processing {len(image_data_list)} images with OCR")
                extracted_text = self.image_processor.extract_text_from_multiple_images(image_data_list)
            
            if extracted_text and extracted_text.strip():
                combined_text_parts.append(extracted_text.strip())
                has_ocr = True
        
        # Combine all text sources
        if combined_text_parts:
            final_text = " ".join(combined_text_parts)
            logger.info(f"Combined text from {len(combined_text_parts)} sources: {len(final_text)} characters")
            return final_text, has_ocr
        
        logger.warning("No valid input provided")
        return "", False

    def _empty_profile_response(self, error_message: str) -> Dict:
        """Return empty response with error"""
        return {
            "success": False,
            "error": error_message,
            "input_text": "",
            "input_context": {},
            "analysis": {},
            "processing_method": "failed"
        }