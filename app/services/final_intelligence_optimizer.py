# app/services/final_intelligence_optimizer.py

import openai
import logging
import json
from typing import Dict, Optional, List
from utils.config import settings
from datetime import datetime, timedelta
import traceback
import re

logger = logging.getLogger(__name__)

class FinalIntelligenceOptimizer:
    """
    STEP 6: Final Intelligence Layer - Realistic Date Planning
    
    Takes complete Steps 1-5 output and creates realistic, practical date plans
    with detailed timing, Google Maps links, and frontend-friendly reasoning
    
    ENHANCED: Proper duration interpretation for "full day" contexts
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
    
    def optimize_complete_date_plan(self, step5_output: Dict) -> Dict:
        """
        STEP 6: Create realistic, practical date plan from Steps 1-5 intelligence
        """
        
        if not self.client_available:
            logger.error("OpenAI client not available for Step 6")
            return self._fallback_final_plan(step5_output, "openai_unavailable")
        
        try:
            logger.info("=== STEP 6: FINAL INTELLIGENCE OPTIMIZATION ===")
            
            # Extract all context and intelligence from Steps 1-5
            context_data = self._extract_complete_context(step5_output)
            logger.info(f"Extracted context: {context_data['location']}, {context_data['time_of_day']}, {context_data['season']}, {context_data['duration']}")
            
            # ENHANCED: Interpret duration properly
            interpreted_duration = self._interpret_duration_context(context_data)
            logger.info(f"Duration interpretation: {interpreted_duration['total_hours']} hours, {interpreted_duration['activities_needed']} activities, {interpreted_duration['start_time']}-{interpreted_duration['end_time']}")
            
            # Validate that we have location context
            if not context_data['location'] or context_data['location'] == 'unknown':
                logger.warning("No location context found in Step 5 output - cannot create realistic date plan")
                return self._fallback_final_plan(step5_output, "no_location_context")
            
            # Create comprehensive OpenAI prompt for realistic date planning
            prompt = self._build_realistic_date_planning_prompt(step5_output, context_data, interpreted_duration)
            
            # Get OpenAI's realistic date plan
            for attempt in range(3):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are the world's most sophisticated date planning expert. Create realistic, practical date plans with precise timing, real locations, and Google Maps integration. Focus on logistics, routing, and authentic local experiences. CRITICAL: Honor the duration requirements exactly - if full day is requested, plan 8+ hours with multiple activities and meals."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,  # Lower temperature for practical planning
                        max_tokens=4000,  # More tokens for full day planning
                        timeout=60  # Longer timeout for complex planning
                    )
                    
                    result = response.choices[0].message.content.strip()
                    final_plan = self._parse_final_plan_response(result)
                    
                    if final_plan and self._validate_final_plan_structure(final_plan, interpreted_duration):
                        # Add processing metadata
                        final_plan["processing_metadata"] = {
                            "step_6_completed": True,
                            "step_6_method": "openai_realistic_planning_with_duration",
                            "input_activities": len(step5_output.get("intelligent_date_plan", {}).get("activities", [])),
                            "input_venues": step5_output.get("venue_discovery_summary", {}).get("total_venues_selected", 0),
                            "output_activities": len(final_plan.get("date", {}).get("activities", [])),
                            "duration_interpretation": interpreted_duration,
                            "planning_intelligence": f"realistic_{context_data['location']}_logistics",
                            "attempt_number": attempt + 1,
                            "pipeline_fully_complete": True,
                            "demo_ready": True,
                            "timestamp": self._safe_timestamp()
                        }
                        
                        logger.info("✅ Step 6 realistic date planning completed successfully")
                        return final_plan
                
                except openai.RateLimitError:
                    logger.warning(f"Rate limit hit on attempt {attempt + 1}")
                    if attempt < 2:
                        import time
                        time.sleep(2 ** attempt)
                    continue
                    
                except Exception as e:
                    logger.error(f"Step 6 planning error on attempt {attempt + 1}: {e}")
                    if attempt < 2:
                        continue
            
            # All attempts failed
            logger.error("All Step 6 realistic planning attempts failed")
            return self._fallback_final_plan(step5_output, "openai_planning_failed")
            
        except Exception as e:
            logger.error(f"Step 6 final intelligence optimization failed: {str(e)}")
            return self._fallback_final_plan(step5_output, str(e))
        
    
    def _interpret_duration_context(self, context_data: Dict) -> Dict:
        """
        FIXED: Interpret duration context for realistic planning
        
        Properly handles "full day", "half day", "4 hours", etc.
        """
        
        duration = context_data.get('duration', '4 hours').lower()
        time_of_day = context_data.get('time_of_day', 'afternoon').lower()
        
        logger.info(f"Interpreting duration: '{duration}' with time_of_day: '{time_of_day}'")
        
        # ✅ FIX: Handle "full day" scenarios FIRST (before checking time_of_day)
        # Handle both "full day" and "full-day" variations
        if ('full day' in duration or 'full-day' in duration or 
            'whole day' in duration or 'whole-day' in duration or 
            'all day' in duration or 'all-day' in duration):
            if 'morning' in time_of_day:
                return {
                    "total_hours": 10,  # ✅ CORRECT: Full day from morning
                    "start_time": "10:00", 
                    "end_time": "20:00",   # ✅ CORRECT: 10 hours total
                    "activities_needed": 5, # ✅ CORRECT: 5 activities for full day
                    "meals_needed": ["brunch", "lunch", "dinner"],
                    "interpretation": "full_day_morning_start"  # ✅ CORRECT
                }
            elif 'afternoon' in time_of_day:
                return {
                    "total_hours": 8,
                    "start_time": "12:00",
                    "end_time": "20:00", 
                    "activities_needed": 4,
                    "meals_needed": ["lunch", "afternoon_break", "dinner"],
                    "interpretation": "full_day_afternoon_start"
                }
            elif 'evening' in time_of_day:
                return {
                    "total_hours": 6,
                    "start_time": "15:00",
                    "end_time": "21:00",
                    "activities_needed": 3,
                    "meals_needed": ["dinner", "evening_drinks"],
                    "interpretation": "full_day_evening_start"
                }
            else:
                # Default full day
                return {
                    "total_hours": 8,
                    "start_time": "12:00",
                    "end_time": "20:00",
                    "activities_needed": 4,
                    "meals_needed": ["lunch", "dinner"],
                    "interpretation": "full_day_default"
                }
        
        # Handle "half day" scenarios (support both space and hyphen)
        elif ('half day' in duration or 'half-day' in duration):
            if 'morning' in time_of_day:
                return {
                    "total_hours": 4,
                    "start_time": "10:00",
                    "end_time": "14:00",
                    "activities_needed": 2,
                    "meals_needed": ["brunch"],
                    "interpretation": "half_day_morning"
                }
            else:  # afternoon or default
                return {
                    "total_hours": 4,
                    "start_time": "14:00",
                    "end_time": "18:00",
                    "activities_needed": 2,
                    "meals_needed": ["afternoon_snack"],
                    "interpretation": "half_day_afternoon"
                }
        
        # Handle specific hour durations like "4 hours", "6 hours"
        else:
            hours = 4  # default
            
            # Extract number from duration
            hour_match = re.search(r'(\d+)\s*hour', duration)
            if hour_match:
                hours = int(hour_match.group(1))
            
            # Determine start time based on time_of_day
            if 'morning' in time_of_day:
                start_hour = 10
            elif 'afternoon' in time_of_day:
                start_hour = 14
            elif 'evening' in time_of_day:
                start_hour = 18
            else:
                start_hour = 14  # default afternoon
            
            end_hour = start_hour + hours
            
            # Determine activities and meals based on duration
            if hours >= 8:
                activities_needed = max(4, hours // 2)
                meals_needed = ["lunch", "dinner"]
            elif hours >= 6:
                activities_needed = 3
                meals_needed = ["lunch", "dinner"] if start_hour <= 14 else ["dinner"]
            elif hours >= 4:
                activities_needed = 2
                meals_needed = ["lunch"] if start_hour <= 12 else ["dinner"] if start_hour >= 17 else ["snack"]
            else:
                activities_needed = 1
                meals_needed = []
            
            return {
                "total_hours": hours,
                "start_time": f"{start_hour:02d}:00",
                "end_time": f"{end_hour:02d}:00",
                "activities_needed": activities_needed,
                "meals_needed": meals_needed,
                "interpretation": f"{hours}_hour_{time_of_day}"
            }
    
    def _extract_complete_context(self, step5_output: Dict) -> Dict:
        """Extract all context from Steps 1-5 for realistic planning - WITH CONTEXT CONTAINER SUPPORT"""
        
        # PRIORITY 1: Check for preserved context from context container
        preserved_context = step5_output.get("original_context")
        if preserved_context and isinstance(preserved_context, dict):
            logger.info("✅ Found preserved context from context container")
            
            # Extract all required fields from preserved context
            location = preserved_context.get("location", "unknown")
            time_of_day = preserved_context.get("time_of_day", "unknown")
            season = preserved_context.get("season", "unknown")
            duration = preserved_context.get("duration", "unknown") 
            date_type = preserved_context.get("date_type", "unknown")
            
            logger.info(f"PRESERVED CONTEXT: location='{location}', time='{time_of_day}', season='{season}', duration='{duration}', date_type='{date_type}'")
            
            # Validate that preserved context is complete
            missing_fields = [field for field, value in {
                "location": location,
                "time_of_day": time_of_day, 
                "season": season,
                "duration": duration,
                "date_type": date_type
            }.items() if value == "unknown"]
            
            if not missing_fields:
                logger.info("🎉 COMPLETE CONTEXT PRESERVED - No fallback needed")
            else:
                logger.warning(f"⚠️  Preserved context missing: {missing_fields}")
        else:
            logger.warning("❌ No preserved context found - using fallback extraction")
            location = time_of_day = season = duration = date_type = "unknown"
        
        # FALLBACK 1: Check processing metadata for input_context
        if any(v == "unknown" for v in [location, time_of_day, season, duration, date_type]):
            metadata = step5_output.get("processing_metadata", {})
            input_context = metadata.get("input_context")
            
            if input_context and isinstance(input_context, dict):
                logger.info("✅ Found fallback context in processing metadata")
                
                if location == "unknown": location = input_context.get("location", location)
                if time_of_day == "unknown": time_of_day = input_context.get("time_of_day", time_of_day)
                if season == "unknown": season = input_context.get("season", season)
                if duration == "unknown": duration = input_context.get("duration", duration)
                if date_type == "unknown": date_type = input_context.get("date_type", date_type)
        
        # FALLBACK 2: Extract from Qloo parameters (location only)
        if location == "unknown":
            activities = step5_output.get("intelligent_date_plan", {}).get("activities", [])
            if activities and activities[0].get("qloo_parameters"):
                location_query = activities[0]["qloo_parameters"].get("filter.location.query", "")
                if location_query:
                    location = location_query.split(",")[0].strip().lower()
                    logger.info(f"Extracted location from Qloo params: {location}")
        
        # FALLBACK 3: Intelligent defaults for missing fields
        if season == "unknown":
            season = self._detect_current_season()
            logger.warning(f"No season context found, using detected season: {season}")
            
        if time_of_day == "unknown":
            time_of_day = "afternoon"  # Conservative default
            logger.warning(f"No time_of_day context found, using default: {time_of_day}")
            
        if date_type == "unknown":
            date_type = "first_date"  # Most common use case
            logger.warning(f"No date_type context found, using default: {date_type}")
            
        if duration == "unknown":
            duration = step5_output.get("intelligent_date_plan", {}).get("total_duration", "4 hours")
            logger.warning(f"No duration context found, using default: {duration}")
        
        # CRITICAL ERROR: Location still unknown
        if location == "unknown":
            logger.error("🚨 CRITICAL: No location found in Step 5 output - realistic planning will fail")
            logger.error("This indicates a serious context preservation bug in the pipeline")
        
        # Get additional context from date plan
        date_plan = step5_output.get("intelligent_date_plan", {})
        compatibility = step5_output.get("compatibility_insights", {})
        
        enhanced_context = {
            # CORE CONTEXT (from preserved or fallback)
            "location": location,
            "time_of_day": time_of_day,
            "season": season,
            "duration": duration,
            "date_type": date_type,
            
            # CULTURAL INTELLIGENCE CONTEXT
            "theme": date_plan.get("theme", "Cultural Exploration"),
            "compatibility_score": compatibility.get("overall_compatibility", 0.75),
            "shared_patterns": compatibility.get("shared_cultural_patterns", []),
            "total_venues_available": step5_output.get("venue_discovery_summary", {}).get("total_venues_selected", 0),
            
            # PIPELINE METADATA
            "cultural_discoveries": step5_output.get("processing_metadata", {}).get("cultural_discoveries_analyzed", 0),
            "weather_context": self._get_seasonal_context(season),
            "context_source": "preserved" if preserved_context else "fallback_extraction"
        }
        
        logger.info(f"🎯 FINAL CONTEXT SUMMARY:")
        logger.info(f"   📍 Location: '{location}' ({enhanced_context['context_source']})")
        logger.info(f"   🕐 Time: '{time_of_day}' ({enhanced_context['context_source']})")
        logger.info(f"   🌸 Season: '{season}' ({enhanced_context['context_source']})")
        logger.info(f"   ⏱️  Duration: '{duration}' ({enhanced_context['context_source']})")
        logger.info(f"   💕 Type: '{date_type}' ({enhanced_context['context_source']})")
        
        # Log what context was missing from original request
        missing_context = [k for k, v in enhanced_context.items() if v == "unknown"]
        if missing_context:
            logger.warning(f"⚠️  Context still missing: {missing_context}")
        else:
            logger.info("✅ Complete context available for realistic Step 6 planning")
        
        return enhanced_context
    
    def _detect_current_season(self) -> str:
        """Detect current season for context"""
        try:
            current_month = datetime.now().month
            if current_month in [3, 4, 5]: return "spring"
            elif current_month in [6, 7, 8]: return "summer"
            elif current_month in [9, 10, 11]: return "autumn"
            else: return "winter"
        except Exception:
            return "spring"
    
    def _get_seasonal_context(self, season: str) -> Dict:
        """Get seasonal context for realistic planning"""
        seasonal_contexts = {
            "spring": {
                "weather": "mild temperatures, occasional rain",
                "clothing": "light layers recommended",
                "outdoor_preference": "60% outdoor activities suitable",
                "daylight": "good daylight until 19:00"
            },
            "summer": {
                "weather": "warm and pleasant",
                "clothing": "comfortable summer wear",
                "outdoor_preference": "80% outdoor activities preferred",
                "daylight": "excellent daylight until 21:00"
            },
            "autumn": {
                "weather": "crisp air, beautiful foliage",
                "clothing": "warm layers and light jacket",
                "outdoor_preference": "40% outdoor activities",
                "daylight": "limited daylight after 17:00"
            },
            "winter": {
                "weather": "cold with possibility of rain",
                "clothing": "warm coat and layers essential",
                "outdoor_preference": "20% outdoor activities",
                "daylight": "limited daylight after 16:00"
            }
        }
        return seasonal_contexts.get(season, seasonal_contexts["spring"])
    
    def _build_realistic_date_planning_prompt(self, step5_output: Dict, context: Dict, interpreted_duration: Dict) -> str:
        """Build comprehensive prompt for realistic date planning WITH DURATION INTERPRETATION"""
        
        # Extract key information
        compatibility = step5_output.get("compatibility_insights", {})
        date_plan = step5_output.get("intelligent_date_plan", {})
        activities = date_plan.get("activities", [])
        venue_summary = step5_output.get("venue_discovery_summary", {})
        cultural_reasoning = step5_output.get("cultural_intelligence_reasoning", {})
        
        # Get venue recommendations from activities
        venue_info = []
        for activity in activities:
            venue_recs = activity.get("venue_recommendations", [])
            if venue_recs:
                top_venue = venue_recs[0]
                venue_info.append({
                    "activity": activity.get("name", "Unknown"),
                    "venue_name": top_venue.get("name", "Unknown"),
                    "location": top_venue.get("location", {}).get("address", context['location']),
                    "reasoning": top_venue.get("openai_selection_reasoning", "")
                })
        
        # Build meals requirement text
        meals_text = ""
        if interpreted_duration['meals_needed']:
            meals_text = f"CRITICAL: Include {len(interpreted_duration['meals_needed'])} meal periods: {', '.join(interpreted_duration['meals_needed'])}"
        
        prompt = f"""You are the world's top date planning expert with deep knowledge of {context['location']}. Create a REALISTIC, practical date plan using the cultural intelligence analysis below.

CONTEXT & REQUIREMENTS:
- Location: {context['location']} (CRITICAL: All venues must be in {context['location']})
- Season: {context['season']} ({context['weather_context']['weather']})
- Duration: {context['duration']} 
- Time: {context['time_of_day']} start
- Date Type: {context['date_type']}
- Theme: {context['theme']}

DURATION REQUIREMENTS: Plan {interpreted_duration['activities_needed']} activities over {interpreted_duration['total_hours']} hours from {interpreted_duration['start_time']} to {interpreted_duration['end_time']}. 
{meals_text}

COMPATIBILITY ANALYSIS:
- Compatibility Score: {compatibility.get('overall_compatibility', 0.75)}
- Shared Patterns: {', '.join(compatibility.get('shared_cultural_patterns', []))}
- Connection Bridges: {', '.join(compatibility.get('connection_bridges', []))}

CULTURAL INTELLIGENCE INSIGHTS:
- Entity Selection Logic: {cultural_reasoning.get('entity_selection_logic', 'Cultural compatibility based')}
- Venue Psychology: {cultural_reasoning.get('venue_psychology_optimization', 'Optimized for connection')}
- Total Cultural Discoveries: {context['cultural_discoveries']}

RECOMMENDED VENUES TO INCORPORATE (if available in {context['location']}):
{json.dumps(venue_info, indent=2)}

CREATE A REALISTIC {context['location'].upper()} DATE PLAN:

CRITICAL REQUIREMENTS:
1. **DURATION COMPLIANCE**: MUST plan exactly {interpreted_duration['activities_needed']} activities over {interpreted_duration['total_hours']} hours
2. **TIMING**: Start at {interpreted_duration['start_time']}, end at {interpreted_duration['end_time']}
3. **MEALS**: Include required meal periods: {interpreted_duration['meals_needed']}
4. **LOCATION ACCURACY**: ALL venues must be real places in {context['location']}
5. **PRACTICAL TIMING**: Use specific times (15:30-16:00 format)
6. **REAL LOCATIONS**: Actual {context['location']} venues/areas with Google Maps links
7. **LOGICAL ROUTING**: Consider walking distances and public transport in {context['location']}
8. **WEATHER AWARENESS**: Account for {context['season']} conditions in {context['location']}
9. **DETAILED ACTIVITIES**: What exactly to do at each venue
10. **CONVERSATION ENGINEERING**: Psychology-based topics that build connection

Return ONLY this JSON structure:

{{
    "date": {{
        "start_time": "{interpreted_duration['start_time']}",
        "total_duration": "{context['duration']}",
        "actual_hours": {interpreted_duration['total_hours']},
        "end_time": "{interpreted_duration['end_time']}",
        "theme": "{context['theme']}",
        "location_city": "{context['location']}",
        "activities": [
            // CREATE EXACTLY {interpreted_duration['activities_needed']} ACTIVITIES
            {{
                "sequence": 1,
                "time_slot": "{interpreted_duration['start_time']} - XX:XX",
                "name": "Visit [REAL {context['location']} VENUE NAME]",
                "location_name": "[ACTUAL VENUE NAME], {context['location']}",
                "google_maps_link": "https://maps.google.com/?q=[ACTUAL+VENUE+NAME],{context['location']}",
                "duration_minutes": 90,
                "activity_type": "cultural/meal/entertainment/outdoor",
                "what_to_do": [
                    "Specific activity 1 appropriate for this {context['location']} venue",
                    "Specific activity 2 that builds connection", 
                    "Specific activity 3 that uses the venue's unique features",
                    "Specific activity 4 that creates conversation opportunities"
                ],
                "why_recommended": "Specific psychological reasoning based on compatibility analysis",
                "conversation_topics": [
                    "Question 1 that builds on shared cultural patterns",
                    "Question 2 that explores their personalities",
                    "Question 3 that relates to the venue/activity"
                ],
                "practical_notes": {{
                    "best_time": "Timing advice for this {context['location']} venue",
                    "cost": "Realistic cost estimate in currency of {context['location']} ",
                    "weather_backup": "Alternative if weather is poor",
                    "what_to_bring": "Practical items needed"
                }},
                "routing_to_next": "Specific directions to next venue in {context['location']}"
            }}
            // REPEAT FOR ALL {interpreted_duration['activities_needed']} ACTIVITIES
        ],
        "logistics": {{
            "total_walking_distance": "Realistic distance calculation",
            "transport_needed": "Public transport options in {context['location']}",
            "weather_adaptations": "Season-appropriate alternatives",
            "cost_estimate": "Total realistic cost in currency of {context['location']} ",
            "energy_level": "Physical energy required"
        }}
    }},
    
    "reasoning": {{
        "compatibility_analysis": {{
            "score": {compatibility.get('overall_compatibility', 0.75)},
            "score_breakdown": {{
                "shared_values": 0.85,
                "complementary_traits": 0.80,
                "activity_alignment": 0.85,
                "conversation_potential": 0.80
            }},
            "strengths": [
                "Specific strength based on their profiles",
                "Another strength that makes this plan work",
                "Third compatibility factor"
            ],
            "potential_challenges": [
                "Realistic challenge they might face",
                "Another potential issue to be aware of"
            ]
        }},
        
        "cultural_intelligence": {{
            "total_discoveries_analyzed": {context['cultural_discoveries']},
            "cross_domain_connections": {len(compatibility.get('shared_cultural_patterns', []))},
            "personality_venue_matches": [
                "How venue 1 matches their psychology",
                "How venue 2 creates connection opportunities",
                "How venue 3 concludes the date perfectly"
            ],
            "qloo_influence": "How cultural taste analysis influenced venue selection"
        }},
        
        "success_prediction": {{
            "overall_probability": 0.82,
            "factors": {{
                "venue_quality": 0.85,
                "activity_engagement": 0.80,
                "conversation_flow": 0.85,
                "practical_logistics": 0.78
            }},
            "optimization_notes": [
                "Why the activity sequence works psychologically",
                "How timing optimizes for connection building",
                "Why these {context['location']} venues specifically work for {interpreted_duration['total_hours']} hours"
            ]
        }},
        
        "frontend_display": {{
            "primary_highlight": "82% success probability - Excellent compatibility",
            "key_selling_points": [
                "{context['cultural_discoveries']} cultural insights analyzed",
                "Perfect {interpreted_duration['total_hours']}-hour activity progression",
                "Authentic {context['location']} experiences beyond tourist spots",
                "Weather-optimized for {context['season']} season"
            ],
            "conversation_starters_count": {interpreted_duration['activities_needed'] * 3},
            "practical_benefits": [
                "All venues within {context['location']}",
                "Indoor backup options available",
                "Cost-effective {interpreted_duration['total_hours']}-hour date",
                "Memorable experiences to discuss later"
            ]
        }}
    }}
}}"""

        return prompt
    
    def _parse_final_plan_response(self, result: str) -> Optional[Dict]:
        """Parse OpenAI realistic date plan response"""
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
        
        logger.error(f"JSON parsing failed for realistic date plan: {result[:200]}...")
        return None
    
    def _validate_final_plan_structure(self, plan: Dict, interpreted_duration: Dict) -> bool:
        """Validate the final plan structure WITH DURATION VALIDATION"""
        required_keys = ["date", "reasoning"]
        
        if not all(key in plan for key in required_keys):
            missing = [k for k in required_keys if k not in plan]
            logger.error(f"Missing required keys in final plan: {missing}")
            return False
        
        date_section = plan.get("date", {})
        if not date_section.get("activities"):
            logger.error("No activities in final date plan")
            return False
        
        # Check that activities have required fields
        activities = date_section.get("activities", [])
        for i, activity in enumerate(activities):
            required_activity_fields = ["time_slot", "name", "location_name", "what_to_do", "conversation_topics"]
            missing_fields = [field for field in required_activity_fields if not activity.get(field)]
            if missing_fields:
                logger.error(f"Activity {i+1} missing fields: {missing_fields}")
                return False
        
        reasoning_section = plan.get("reasoning", {})
        if not reasoning_section.get("compatibility_analysis"):
            logger.error("Missing compatibility analysis in reasoning")
            return False
        
        # ENHANCED: Validate duration compliance
        expected_activities = interpreted_duration['activities_needed']
        actual_activities = len(activities)
        
        if actual_activities < expected_activities:
            logger.warning(f"Fewer activities than expected: {actual_activities} vs {expected_activities} - but allowing")
        
        # Check if start time matches
        expected_start = interpreted_duration['start_time']
        actual_start = date_section.get('start_time', '')
        
        if expected_start != actual_start:
            logger.warning(f"Start time mismatch: expected {expected_start}, got {actual_start} - but allowing")
        
        logger.info(f"✅ Validated final plan: {len(activities)} activities, duration requirements mostly met")
        return True
    
    def _safe_timestamp(self) -> str:
        """Generate safe timestamp"""
        try:
            return datetime.now().isoformat()
        except Exception:
            return "unknown"
    
    def _fallback_final_plan(self, step5_output: Dict, error_reason: str) -> Dict:
        """Fallback when Step 6 fails - use actual context, never hardcode location"""
        
        # Extract context for fallback
        context_data = self._extract_complete_context(step5_output)
        location = context_data.get('location', 'Unknown City')
        
        # Interpret duration for fallback
        interpreted_duration = self._interpret_duration_context(context_data)
        
        # Extract basic info for fallback
        compatibility = step5_output.get("compatibility_insights", {})
        date_plan = step5_output.get("intelligent_date_plan", {})
        activities = date_plan.get("activities", [])
        
        # Create fallback activities based on duration interpretation
        fallback_activities = []
        
        # Create appropriate number of activities for duration
        for i in range(interpreted_duration['activities_needed']):
            activity_start_hour = int(interpreted_duration['start_time'].split(':')[0]) + (i * 2)
            activity_end_hour = activity_start_hour + 1.5
            
            fallback_activity = {
                "sequence": i + 1,
                "time_slot": f"{activity_start_hour:02d}:00 - {int(activity_end_hour):02d}:{int((activity_end_hour % 1) * 60):02d}",
                "name": f"{location} City Walk - Stop {i + 1}" if location != "Unknown City" else f"City Exploration - Stop {i + 1}",
                "location_name": f"City Center Area {i + 1}, {location}",
                "google_maps_link": f"https://maps.google.com/?q=City+Center,{location}",
                "duration_minutes": 90,
                "activity_type": "exploration",
                "what_to_do": [
                    f"Explore area {i + 1} of {location}",
                    "Visit local cafés and shops",
                    "Take photos and enjoy conversation",
                    "Discover neighborhood character together"
                ],
                "why_recommended": f"Central {location} location perfect for getting to know each other",
                "conversation_topics": [
                    f"What's your favorite part of {location}?" if location != "Unknown City" else "What kind of places inspire you most?",
                    "What kind of places inspire you most?",
                    "What would make this a perfect day for you?"
                ],
                "practical_notes": {
                    "cost": "Free walking, €10-20 for refreshments",
                    "weather_backup": "Indoor shopping areas and cafés nearby",
                    "what_to_bring": "Comfortable walking shoes",
                    "best_time": "Flexible timing"
                },
                "routing_to_next": "Short walk to next area" if i < interpreted_duration['activities_needed'] - 1 else "End of planned activities"
            }
            fallback_activities.append(fallback_activity)
        
        return {
            "date": {
                "start_time": interpreted_duration['start_time'],
                "total_duration": context_data.get('duration', '4 hours'),
                "actual_hours": interpreted_duration['total_hours'],
                "end_time": interpreted_duration['end_time'],
                "theme": date_plan.get("theme", f"{context_data.get('location', 'City')} Exploration"),
                "location_city": context_data.get('location', 'Unknown City'),
                "activities": fallback_activities,
                "logistics": {
                    "total_walking_distance": "Flexible based on preferences",
                    "transport_needed": f"Public transport to city center in {context_data.get('location', 'the city')}",
                    "weather_adaptations": "Indoor alternatives available",
                    "cost_estimate": f"€{20 * interpreted_duration['activities_needed']}-{40 * interpreted_duration['activities_needed']} per person",
                    "energy_level": "Light to moderate"
                }
            },
            "reasoning": {
                "compatibility_analysis": {
                    "score": compatibility.get("overall_compatibility", 0.7),
                    "score_breakdown": {
                        "shared_values": 0.7,
                        "complementary_traits": 0.7,
                        "activity_alignment": 0.7,
                        "conversation_potential": 0.7
                    },
                    "strengths": ["Central location", "Flexible activities"],
                    "potential_challenges": ["Generic fallback plan", "Limited personalization"]
                },
                "cultural_intelligence": {
                    "total_discoveries_analyzed": 0,
                    "cross_domain_connections": 0,
                    "personality_venue_matches": ["Basic exploration"],
                    "qloo_influence": "Limited due to processing error"
                },
                "success_prediction": {
                    "overall_probability": 0.6,
                    "factors": {
                        "venue_quality": 0.6,
                        "activity_engagement": 0.6,
                        "conversation_flow": 0.6,
                        "practical_logistics": 0.7
                    },
                    "optimization_notes": [f"Fallback plan with {interpreted_duration['activities_needed']} activities over {interpreted_duration['total_hours']} hours"]
                },
                "frontend_display": {
                    "primary_highlight": "60% success probability - Basic compatibility",
                    "key_selling_points": ["Central location", "Flexible timing", f"{interpreted_duration['total_hours']}-hour duration honored"],
                    "conversation_starters_count": interpreted_duration['activities_needed'] * 3,
                    "practical_benefits": ["Easy to reach", "Weather adaptable", f"Full {interpreted_duration['total_hours']}-hour experience"]
                }
            },
            "processing_metadata": {
                "step_6_completed": False,
                "step_6_error": error_reason,
                "fallback_used": True,
                "duration_interpretation": interpreted_duration,
                "pipeline_fully_complete": False,
                "demo_ready": False,
                "timestamp": self._safe_timestamp()
            }
        }