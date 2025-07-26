import openai
import logging
import json
from typing import Dict, Optional, List, Tuple
from utils.config import settings
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)

class ProfileAnalyzer:
    """Advanced psychological profiler optimized for Qloo cultural intelligence integration"""
    
    def __init__(self):
        # Robust OpenAI client setup
        self.api_key = settings.OPENAI_API_KEY or "dummy_key"
        self.model = settings.OPENAI_MODEL or "gpt-4o-mini"
        
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.client_available = True
        except Exception as e:
            logger.error(f"OpenAI client initialization failed: {e}")
            self.client_available = False
    
    def analyze_profile_with_context(self, profile_text: str, context: Dict = None, is_ocr_text: bool = False) -> Dict:
        """Advanced psychological analysis optimized for cultural intelligence systems"""
        
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
        
        # Make OpenAI call with retries
        for attempt in range(3):
            try:
                prompt = self._build_psychological_analysis_prompt(profile_text, fallback_context, is_ocr_text)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a world-class cultural psychologist and dating expert. Provide deep psychological insights while extracting clean entities for cultural intelligence systems. Focus on what makes this person unique psychologically."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,  # Balanced for insight and consistency
                    max_tokens=1800,
                    timeout=30
                )
                
                result = response.choices[0].message.content.strip()
                analysis = self._parse_openai_response(result)
                
                if analysis and self._validate_analysis_structure(analysis):
                    # Accuracy validation
                    is_accurate, accuracy_issues = self._validate_text_accuracy(profile_text, analysis)
                    
                    if not is_accurate and attempt < 2:
                        logger.warning(f"Accuracy issues detected: {accuracy_issues}. Retrying.")
                        continue
                    
                    # Add processing metadata
                    analysis["processing_metadata"] = {
                        "input_method": "ocr" if is_ocr_text else "direct_text",
                        "context_provided": len([v for v in context.values() if v and str(v).lower() != "unknown"]) if context else 0,
                        "attempt_number": attempt + 1,
                        "accuracy_issues": accuracy_issues if not is_accurate else [],
                        "psychological_depth": "advanced",
                        "timestamp": self._safe_timestamp()
                    }
                    
                    logger.info(f"Successfully completed advanced psychological analysis on attempt {attempt + 1}")
                    return analysis
                
            except openai.RateLimitError:
                logger.warning(f"Rate limit hit on attempt {attempt + 1}")
                if attempt < 2:
                    import time
                    time.sleep(2 ** attempt)
                continue
                
            except Exception as e:
                logger.error(f"Analysis error on attempt {attempt + 1}: {e}")
                if attempt < 2:
                    continue
        
        # All attempts failed
        logger.error("All analysis attempts failed")
        return self._fallback_analysis(is_ocr_text, "openai_failed")
    
    def _build_psychological_analysis_prompt(self, profile_text: str, fallback_context: Dict, is_ocr_text: bool) -> str:
        """Build sophisticated psychological analysis prompt for cultural intelligence"""
        
        # OCR handling
        ocr_instruction = ""
        if is_ocr_text:
            ocr_instruction = """
            IMPORTANT: This text was extracted via OCR and may contain typos. Focus on the meaning behind potentially garbled words.
            """
        
        # Truncate if needed
        if len(profile_text) > 1000:
            profile_text = profile_text[:1000] + "..."
        
        prompt = f"""
        You are a leading cultural psychologist specializing in personality analysis for personalized experiences. Analyze this dating profile with sophisticated psychological insight.

        {ocr_instruction}

        PROFILE TEXT: "{profile_text}"

        CONTEXT: Location: {fallback_context['location']}, Time: {fallback_context['time_of_day']}, Season: {fallback_context['season']}, Duration: {fallback_context['duration']}, Type: {fallback_context['date_type']}

        PROVIDE DEEP PSYCHOLOGICAL ANALYSIS:

        1. **ADVANCED PERSONALITY PSYCHOLOGY**: Go beyond surface traits
           - Big Five with nuanced scoring based on language patterns and stated interests
           - Dating-specific traits with confidence levels
           - Communication style analysis (direct vs subtle, playful vs serious, etc.)
           - Attachment style indicators (secure, anxious, avoidant)
           - Social energy patterns and group preferences
           - Intellectual curiosity level and learning style

        2. **CULTURAL ENTITY EXTRACTION**: Clean entities for cultural intelligence systems
           - Extract ONLY explicitly mentioned or clearly implied entities
           - Structure for cultural recommendation systems
           - Focus on accuracy - don't invent connections

        3. **PSYCHOLOGICAL CONTEXT INTELLIGENCE**: Deep insights for experience optimization
           - What motivates this person psychologically?
           - What environments bring out their best self?
           - What conversation topics create authentic connection?
           - What experiences would feel meaningful vs superficial to them?
           - How do they likely approach new relationships?

        4. **CULTURAL SOPHISTICATION ASSESSMENT**: For personalization depth
           - Level of cultural engagement and curiosity
           - Preference for mainstream vs niche experiences
           - Aesthetic sensibilities and style preferences
           - Openness to new cultural experiences

        Return sophisticated JSON analysis:
        {{
            "text_interpretation": "Sarah enjoys hiking and outdoor activities, lives in Rotterdam, currently studying marketing",
            
            "advanced_psychological_profile": {{
                "big_five_detailed": {{
                    "openness": {{"score": 0.7, "reasoning": "Hiking suggests openness to outdoor experiences", "confidence": 0.8}},
                    "conscientiousness": {{"score": 0.6, "reasoning": "Marketing studies suggest goal-oriented behavior", "confidence": 0.7}},
                    "extraversion": {{"score": 0.5, "reasoning": "Insufficient data for strong assessment", "confidence": 0.4}},
                    "agreeableness": {{"score": 0.6, "reasoning": "Generally positive self-presentation", "confidence": 0.5}},
                    "neuroticism": {{"score": 0.3, "reasoning": "Active lifestyle suggests emotional stability", "confidence": 0.6}}
                }},
                "dating_psychology": {{
                    "adventurousness": {{"score": 0.8, "reasoning": "Hiking indicates comfort with adventure", "confidence": 0.9}},
                    "authenticity_preference": {{"score": 0.7, "reasoning": "Direct self-expression in profile", "confidence": 0.7}},
                    "intellectual_curiosity": {{"score": 0.6, "reasoning": "University education, but no strong indicators", "confidence": 0.5}},
                    "social_energy": {{"score": 0.5, "reasoning": "No clear social indicators", "confidence": 0.4}},
                    "cultural_sophistication": {{"score": 0.5, "reasoning": "No specific cultural markers", "confidence": 0.4}}
                }},
                "communication_style": {{
                    "directness": "moderate_to_high",
                    "humor_style": "natural_and_unpretentious", 
                    "conversation_depth": "prefers_genuine_over_polished",
                    "attachment_indicators": "appears_secure_and_straightforward"
                }},
                "relationship_approach": {{
                    "dating_goals": "likely_seeking_genuine_connection",
                    "pace_preference": "natural_progression",
                    "value_alignment": "authenticity_and_shared_experiences",
                    "deal_breakers": "likely_dislikes_pretension_and_superficiality"
                }}
            }},

            "qloo_optimized_entities": {{
                "explicitly_mentioned": {{
                    "activities": ["hiking"],
                    "locations": ["rotterdam"],
                    "education": ["marketing"],
                    "interests": []
                }},
                "high_confidence_inferences": {{
                    "activity_categories": ["outdoor", "active"],
                    "lifestyle_indicators": ["health_conscious", "nature_appreciating"],
                    "demographic_context": ["university_student", "young_adult"]
                }},
                "personality_entities": {{
                    "adventure_seeking": 0.8,
                    "authenticity_valuing": 0.7,
                    "nature_loving": 0.8,
                    "goal_oriented": 0.6
                }}
            }},

            "qloo_query_preparation": {{
                "primary_entities": ["hiking", "outdoor_activities"],
                "demographic_context": {{
                    "age_range": "20-25",
                    "location": "rotterdam",
                    "education_level": "university",
                    "lifestyle": "active"
                }},
                "personality_weights": {{
                    "adventurous": 0.8,
                    "authentic": 0.7,
                    "health_conscious": 0.7,
                    "unpretentious": 0.7
                }},
                "cultural_sophistication": "moderate",
                "venue_preferences": {{
                    "atmosphere": "relaxed_and_genuine",
                    "formality": "casual_to_moderate",
                    "novelty": "open_to_new_but_not_required"
                }}
            }},

            "experience_optimization_insights": {{
                "motivational_drivers": ["authentic_connection", "shared_experiences", "personal_growth"],
                "ideal_date_psychology": {{
                    "energy_level": "moderate_to_active",
                    "setting_preference": "comfortable_but_interesting",
                    "conversation_catalyst": "shared_activities_or_experiences",
                    "connection_style": "genuine_and_unpressured"
                }},
                "conversation_psychology": {{
                    "energizing_topics": ["outdoor_experiences", "travel_stories", "life_goals", "local_discoveries"],
                    "bonding_opportunities": ["shared_activity_experiences", "future_adventure_planning", "personal_story_sharing"],
                    "conversation_starters": [
                        "What's the most beautiful hiking spot you've discovered?",
                        "How did you end up choosing marketing as your field?",
                        "What's something about Rotterdam that most people don't know?"
                    ],
                    "topics_to_avoid": ["overly_polished_small_talk", "status_focused_conversations"],
                    "depth_preference": "meaningful_but_accessible"
                }},
                "environmental_psychology": {{
                    "comfort_factors": ["natural_elements", "relaxed_atmosphere", "authentic_character"],
                    "energy_preferences": ["moderate_stimulation", "not_overwhelming", "space_for_conversation"],
                    "deal_breakers": ["overly_pretentious_venues", "extremely_loud_environments"]
                }}
            }},

            "intelligent_context_recommendations": {{
                "optimal_location": "amsterdam",
                "reasoning": "Urban cultural opportunities while maintaining access to nature",
                "optimal_timing": "afternoon_to_early_evening", 
                "timing_reasoning": "Natural energy pattern for outdoor-oriented person",
                "ideal_duration": "4-5_hours",
                "duration_reasoning": "Enough time for genuine connection without pressure",
                "seasonal_adaptations": {{
                    "winter": "indoor_venues_with_natural_elements",
                    "summer": "outdoor_or_semi_outdoor_options",
                    "spring/autumn": "flexible_indoor_outdoor_combinations"
                }},
                "date_type_optimization": "activity_based_with_conversation_opportunities"
            }},

            "demographics": {{
                "age": "approximately_20-25",
                "location": "Rotterdam",
                "education": "Marketing",
                "occupation": "Student",
                "lifestyle_stage": "university_exploration_phase"
            }},

            "processing_confidence": 0.87
        }}
        """
        
        return prompt
    
    def _validate_text_accuracy(self, input_text: str, analysis: Dict) -> Tuple[bool, List[str]]:
        """Validate psychological analysis accuracy"""
        issues = []
        input_lower = input_text.lower()
        
        # Check explicit entity extraction
        qloo_entities = analysis.get("qloo_optimized_entities", {})
        mentioned = qloo_entities.get("explicitly_mentioned", {})
        
        # Validate activity extraction
        if "hiking" in input_lower:
            activities = mentioned.get("activities", [])
            if "hiking" not in str(activities).lower():
                issues.append("Hiking mentioned but not captured in activities")
        
        # Validate location extraction  
        if "rotterdam" in input_lower:
            locations = mentioned.get("locations", [])
            if "rotterdam" not in str(locations).lower():
                issues.append("Rotterdam mentioned but not captured in locations")
        
        # Validate education extraction
        if "marketing" in input_lower:
            education = mentioned.get("education", [])
            demographics = analysis.get("demographics", {})
            if "marketing" not in str(education).lower() and "marketing" not in str(demographics.get("education", "")).lower():
                issues.append("Marketing mentioned but not captured correctly")
        
        return len(issues) == 0, issues
    
    def _get_robust_context(self, context: Dict) -> Dict:
        """Get context with intelligent defaults"""
        try:
            current_season = self._safe_detect_season()
        except Exception:
            current_season = "spring"
        
        return {
            "location": str(context.get("location", "unknown")).strip() or "unknown",
            "time_of_day": str(context.get("time_of_day", "unknown")).strip() or "unknown", 
            "season": str(context.get("season", current_season)).strip() or current_season,
            "duration": str(context.get("duration", "unknown")).strip() or "unknown",
            "date_type": str(context.get("date_type", "unknown")).strip() or "unknown"
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
        """Parse JSON with multiple fallback strategies"""
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
        
        logger.error(f"JSON parsing failed for: {result[:200]}...")
        return None
    
    def _validate_analysis_structure(self, analysis: Dict) -> bool:
        """Validate required structure for Qloo integration"""
        required_keys = [
            "advanced_psychological_profile",
            "qloo_optimized_entities", 
            "qloo_query_preparation",
            "experience_optimization_insights"
        ]
        return all(key in analysis for key in required_keys)
    
    def _fallback_analysis(self, is_ocr_text: bool, error_reason: str) -> Dict:
        """Comprehensive fallback with sophisticated structure"""
        return {
            "text_interpretation": "Fallback analysis due to processing error",
            "advanced_psychological_profile": {
                "big_five_detailed": {
                    "openness": {"score": 0.5, "reasoning": "Insufficient data", "confidence": 0.3},
                    "conscientiousness": {"score": 0.5, "reasoning": "Insufficient data", "confidence": 0.3},
                    "extraversion": {"score": 0.5, "reasoning": "Insufficient data", "confidence": 0.3},
                    "agreeableness": {"score": 0.5, "reasoning": "Insufficient data", "confidence": 0.3},
                    "neuroticism": {"score": 0.5, "reasoning": "Insufficient data", "confidence": 0.3}
                },
                "dating_psychology": {
                    "adventurousness": {"score": 0.5, "reasoning": "Default assumption", "confidence": 0.3},
                    "authenticity_preference": {"score": 0.5, "reasoning": "Default assumption", "confidence": 0.3},
                    "intellectual_curiosity": {"score": 0.5, "reasoning": "Default assumption", "confidence": 0.3},
                    "social_energy": {"score": 0.5, "reasoning": "Default assumption", "confidence": 0.3}
                },
                "communication_style": {
                    "directness": "moderate",
                    "humor_style": "balanced",
                    "conversation_depth": "moderate"
                }
            },
            "qloo_optimized_entities": {
                "explicitly_mentioned": {
                    "activities": [],
                    "locations": [],
                    "interests": []
                },
                "personality_entities": {
                    "balanced": 0.5
                }
            },
            "qloo_query_preparation": {
                "primary_entities": ["general_interests"],
                "demographic_context": {
                    "age_range": "25-35",
                    "location": "amsterdam",
                    "lifestyle": "balanced"
                },
                "personality_weights": {
                    "balanced": 0.5
                }
            },
            "experience_optimization_insights": {
                "motivational_drivers": ["connection", "comfort"],
                "conversation_psychology": {
                    "energizing_topics": ["shared_interests"],
                    "conversation_starters": ["What do you enjoy doing in your free time?"]
                }
            },
            "intelligent_context_recommendations": {
                "optimal_location": "amsterdam",
                "optimal_timing": "evening",
                "ideal_duration": "3-4_hours"
            },
            "demographics": {
                "age": "unknown",
                "location": "unknown", 
                "education": "unknown",
                "occupation": "unknown"
            },
            "processing_confidence": 0.1,
            "processing_metadata": {
                "input_method": "ocr" if is_ocr_text else "direct_text",
                "error_reason": error_reason,
                "fallback_used": True,
                "timestamp": self._safe_timestamp()
            }
        }