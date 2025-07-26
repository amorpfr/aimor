# app/services/venue_discoverer.py

import requests
import logging
import time
import openai
import json
from typing import Dict, List, Optional
from utils.config import settings

logger = logging.getLogger(__name__)

class VenueDiscoverer:
    """
    STEP 5: OpenAI-Enhanced Venue Discovery Service
    
    Gets venue candidates from Qloo, then uses OpenAI intelligence
    to select the most appropriate venues for each activity.
    """
    
    def __init__(self):
        self.qloo_api_key = settings.QLOO_API_KEY
        self.openai_api_key = settings.OPENAI_API_KEY
        self.base_url = "https://hackathon.api.qloo.com"
        self.headers = {
            "x-api-key": self.qloo_api_key,
            "Content-Type": "application/json"
        }
        
        # Initialize OpenAI client
        try:
            self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            self.openai_available = True
        except Exception as e:
            logger.error(f"OpenAI client initialization failed: {e}")
            self.openai_available = False
        
        # Optimized timeouts
        self.insights_timeout = 30
        self.max_retries = 2
        
    def discover_venues_for_date_plan(self, date_plan: Dict) -> Dict:
        """
        Execute OpenAI-enhanced venue discovery for complete date plan
        """
        
        try:
            logger.info("=== STEP 5: OPENAI-ENHANCED VENUE DISCOVERY ===")
            
            # Extract Qloo-ready queries from date plan
            qloo_queries = date_plan.get("qloo_ready_queries", [])
            activities = date_plan.get("intelligent_date_plan", {}).get("activities", [])
            
            if not qloo_queries:
                logger.error("No Qloo queries found in date plan")
                return self._fallback_venue_response(date_plan, "no_qloo_queries")
            
            logger.info(f"Processing {len(qloo_queries)} venue discovery queries with OpenAI intelligence")
            
            # Execute OpenAI-enhanced venue discovery for each activity
            enriched_activities = []
            venue_discovery_results = []
            
            for i, (query, activity) in enumerate(zip(qloo_queries, activities)):
                activity_name = query.get('activity_name', f'Activity {i+1}')
                logger.info(f"Discovering venues for: {activity_name}")
                
                # Step 1: Get venue candidates from Qloo (no filtering)
                venue_candidates = self._get_venue_candidates_from_qloo(query, i+1)
                
                # Step 2: Use OpenAI to intelligently select best venues
                selected_venues = self._openai_venue_selection(
                    venue_candidates, activity, query, date_plan
                )
                
                # Step 3: Enrich activity with OpenAI-selected venues
                enriched_activity = self._enrich_activity_with_venues(activity, selected_venues)
                enriched_activities.append(enriched_activity)
                
                # Store discovery results for analysis
                venue_discovery_results.append({
                    "activity_name": activity_name,
                    "candidates_found": len(venue_candidates),
                    "venues_selected": len(selected_venues),
                    "selection_method": "openai_intelligent_selection",
                    "venues": selected_venues
                })
            
            # Build complete response with OpenAI-selected venues
            complete_date_plan = self._build_complete_date_plan(
                date_plan, enriched_activities, venue_discovery_results
            )
            
            logger.info("✅ Step 5 OpenAI-enhanced venue discovery completed successfully")
            return complete_date_plan
            
        except Exception as e:
            logger.error(f"Step 5 OpenAI-enhanced venue discovery failed: {str(e)}")
            return self._fallback_venue_response(date_plan, str(e))
    
    def _get_venue_candidates_from_qloo(self, query: Dict, activity_number: int) -> List[Dict]:
        """Get raw venue candidates from Qloo without any filtering"""
        
        activity_name = query.get("activity_name", f"Activity {activity_number}")
        parameters = query.get("parameters", {})
        
        if not parameters:
            logger.warning(f"No parameters for {activity_name}")
            return []
        
        # Strategy: Get maximum venue candidates using entity signals (what works!)
        # Let OpenAI do the intelligent filtering later
        
        candidate_approaches = [
            # Approach 1: Entity signals + location (most effective)
            {
                "filter.type": "urn:entity:place",
                "filter.location.query": parameters.get("filter.location.query", "Amsterdam, Netherlands"),
                "signal.interests.entities": parameters.get("signal.interests.entities", ""),
                "take": 15  # Get many candidates for OpenAI to choose from
            },
            # Approach 2: Entity signals + broader parameters
            {
                "filter.type": "urn:entity:place", 
                "filter.location.query": parameters.get("filter.location.query", "Amsterdam, Netherlands"),
                "signal.interests.entities": parameters.get("signal.interests.entities", ""),
                "filter.popularity.min": 0.2,  # Cast wider net
                "take": 12
            },
            # Approach 3: Location-based fallback
            {
                "filter.type": "urn:entity:place",
                "filter.location.query": parameters.get("filter.location.query", "Amsterdam, Netherlands"),
                "filter.popularity.min": 0.3,
                "take": 10
            }
        ]
        
        # Try approaches until we get good candidates
        for approach_idx, params in enumerate(candidate_approaches):
            logger.info(f"Getting candidates with approach {approach_idx + 1} for {activity_name}")
            
            try:
                # Clean parameters (remove empty values)
                clean_params = {k: v for k, v in params.items() if v}
                
                response = requests.get(
                    f"{self.base_url}/v2/insights",
                    headers=self.headers,
                    params=clean_params,
                    timeout=self.insights_timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("results", {}).get("entities", [])
                    
                    if entities:
                        # Process all venue candidates (no filtering here)
                        candidates = []
                        for entity in entities:
                            venue = self._process_venue_entity(entity)
                            if venue:
                                candidates.append(venue)
                        
                        if candidates:
                            logger.info(f"✅ {activity_name}: Found {len(candidates)} venue candidates")
                            return candidates
                        
                else:
                    logger.warning(f"Qloo API error: HTTP {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error getting candidates: {e}")
                continue
        
        logger.warning(f"❌ {activity_name}: No venue candidates found")
        return []
    
    def _openai_venue_selection(self, venue_candidates: List[Dict], activity: Dict, query: Dict, date_plan: Dict) -> List[Dict]:
        """Use OpenAI to intelligently select best venues from candidates"""
        
        if not venue_candidates:
            logger.warning("No venue candidates for OpenAI selection")
            return []
        
        if not self.openai_available:
            logger.warning("OpenAI not available, using first few candidates")
            return venue_candidates[:3]
        
        try:
            # Build intelligent venue selection prompt
            prompt = self._build_venue_selection_prompt(venue_candidates, activity, query, date_plan)
            
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL or "gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a world-class venue curator and dating expert. Your job is to intelligently select the best venues from candidates based on psychological compatibility, activity purpose, and cultural intelligence. Always return valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for consistent selection
                max_tokens=2000,  # Increased for complete responses
                timeout=45  # Increased timeout
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"OpenAI venue selection response length: {len(result)} characters")
            
            selection_data = self._parse_venue_selection_response(result)
            
            if selection_data and selection_data.get("selected_venues"):
                # Map selected venue IDs back to full venue data
                selected_ids = [v.get("venue_id") for v in selection_data["selected_venues"]]
                selected_venues = []
                
                for venue in venue_candidates:
                    if venue.get("id") in selected_ids:
                        # Add OpenAI reasoning to venue data
                        for selected in selection_data["selected_venues"]:
                            if selected.get("venue_id") == venue.get("id"):
                                venue["openai_selection_reasoning"] = selected.get("reasoning", "")
                                venue["openai_ranking"] = selected.get("ranking", 0)
                                venue["conversation_opportunities"] = selected.get("conversation_opportunities", [])
                                venue["atmosphere_match"] = selected.get("atmosphere_match", "")
                                break
                        selected_venues.append(venue)
                
                # Sort by OpenAI ranking
                selected_venues.sort(key=lambda x: x.get("openai_ranking", 999))
                
                logger.info(f"✅ OpenAI selected {len(selected_venues)} venues with intelligent reasoning")
                return selected_venues[:5]  # Top 5 selections
            else:
                logger.warning("OpenAI response parsed but no selected_venues found")
            
        except Exception as e:
            logger.error(f"OpenAI venue selection failed: {e}")
            logger.error(f"Response that failed: {result[:500] if 'result' in locals() else 'No response'}")
        
        # Fallback: return top candidates by affinity
        logger.warning("Falling back to affinity-based selection")
        sorted_candidates = sorted(venue_candidates, key=lambda x: x.get("qloo_affinity", 0), reverse=True)
        return sorted_candidates[:3]
    
    def _build_venue_selection_prompt(self, candidates: List[Dict], activity: Dict, query: Dict, date_plan: Dict) -> str:
        """Build concise prompt for OpenAI venue selection"""
        
        # Extract context
        activity_name = activity.get("name", "Unknown Activity")
        activity_reasoning = activity.get("cultural_reasoning", "")
        theme = date_plan.get("intelligent_date_plan", {}).get("theme", "Unknown")

        # Extract user location for geographic context
        qloo_params = query.get("parameters", {})
        user_location = qloo_params.get("filter.location.query", "the user's city")

        # Prepare venue candidate data (limit for prompt efficiency)
        candidate_summaries = []
        for i, venue in enumerate(candidates[:8]):  # Reduced to 8 for shorter prompt
            summary = {
                "venue_id": venue.get("id", f"venue_{i}"),
                "name": venue.get("name", "Unknown"),
                "type": venue.get("type", "venue"),
                "description": venue.get("description", "")[:120],  # Shorter descriptions
                "neighborhood": venue.get("location", {}).get("neighborhood", "Amsterdam"),
                "price": venue.get("business_info", {}).get("price_description", "Unknown"),
                "rating": venue.get("ratings", {}).get("qloo_rating", {}).get("score", "N/A")
            }
            candidate_summaries.append(summary)
        
        prompt = f"""Select the best 3 venues for this date activity using cultural intelligence.

ACTIVITY: {activity_name}
PURPOSE: {activity_reasoning}
DATE THEME: {theme}
CULTURAL CONTEXT: discoveries represent global taste preferences. Select venues specifically located in {user_location}.
VENUE OPTIONS:
{json.dumps(candidate_summaries, indent=1)}

Select 3 venues that best match the activity purpose and will create meaningful connection.

Return ONLY this JSON format:
{{
    "selected_venues": [
        {{
            "venue_id": "exact_venue_id_from_above",
            "ranking": 1,
            "reasoning": "Brief explanation why this venue is perfect"
        }},
        {{
            "venue_id": "exact_venue_id_from_above", 
            "ranking": 2,
            "reasoning": "Brief reasoning"
        }},
        {{
            "venue_id": "exact_venue_id_from_above",
            "ranking": 3, 
            "reasoning": "Brief reasoning"
        }}
    ]
}}

Choose venues that create conversation opportunities and match the activity energy."""
        
        return prompt
    
    def _parse_venue_selection_response(self, result: str) -> Optional[Dict]:
        """Parse OpenAI venue selection response"""
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
        
        logger.error(f"Failed to parse OpenAI venue selection: {result[:200]}...")
        return None
    
    def _process_venue_entity(self, entity: Dict) -> Optional[Dict]:
        """Process Qloo entity into venue information (unchanged from before)"""
        
        try:
            # Extract basic venue info
            venue = {
                "id": entity.get("entity_id", ""),
                "name": entity.get("name", "Unknown Venue"),
                "type": self._extract_venue_type(entity),
                "description": entity.get("description", ""),
                "qloo_affinity": entity.get("affinity", 0),
                "popularity": entity.get("popularity", 0)
            }
            
            # Extract location information
            properties = entity.get("properties", {})
            geocode = properties.get("geocode", {})
            
            if geocode:
                venue["location"] = {
                    "address": self._build_address(geocode),
                    "neighborhood": geocode.get("name", ""),
                    "city": geocode.get("admin1_region", ""),
                    "country": geocode.get("country_code", ""),
                    "coordinates": {
                        "latitude": geocode.get("latitude"),
                        "longitude": geocode.get("longitude")
                    }
                }
            
            # Extract business information
            venue["business_info"] = self._extract_business_info(properties)
            
            # Extract ratings and reviews
            venue["ratings"] = self._extract_ratings(properties)
            
            # Only return venues with basic required info
            if venue["name"] != "Unknown Venue":
                return venue
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error processing venue entity: {e}")
            return None
    
    def _extract_venue_type(self, entity: Dict) -> str:
        """Extract venue type from entity"""
        entity_type = entity.get("type", "").replace("urn:entity:", "")
        
        # Map Qloo types to readable venue types
        type_mappings = {
            "place": "venue",
            "restaurant": "restaurant", 
            "cafe": "cafe",
            "bar": "bar",
            "museum": "museum",
            "gallery": "gallery"
        }
        
        return type_mappings.get(entity_type, "venue")
    
    def _build_address(self, geocode: Dict) -> str:
        """Build readable address from geocode data"""
        address_parts = []
        
        if geocode.get("street_address"):
            address_parts.append(geocode["street_address"])
        
        if geocode.get("name"):
            address_parts.append(geocode["name"])
            
        if geocode.get("admin1_region"):
            address_parts.append(geocode["admin1_region"])
            
        return ", ".join(filter(None, address_parts)) or "Address not available"
    
    def _extract_business_info(self, properties: Dict) -> Dict:
        """Extract business information from properties"""
        business_info = {}
        
        if properties.get("price_level"):
            business_info["price_level"] = properties["price_level"]
            business_info["price_description"] = self._price_level_description(properties["price_level"])
        
        if properties.get("hours"):
            business_info["hours"] = properties["hours"]
        
        if properties.get("phone"):
            business_info["phone"] = properties["phone"]
            
        if properties.get("website"):
            business_info["website"] = properties["website"]
        
        return business_info
    
    def _price_level_description(self, price_level: int) -> str:
        """Convert price level to description"""
        descriptions = {
            1: "Budget-friendly",
            2: "Moderate",
            3: "Upscale", 
            4: "High-end"
        }
        return descriptions.get(price_level, "Price level unknown")
    
    def _extract_ratings(self, properties: Dict) -> Dict:
        """Extract ratings from various sources"""
        ratings = {}
        
        if properties.get("business_rating"):
            ratings["qloo_rating"] = {
                "score": properties["business_rating"],
                "source": "Qloo"
            }
        
        external = properties.get("external", {})
        
        if external.get("tripadvisor"):
            ta_data = external["tripadvisor"]
            if ta_data.get("rating"):
                ratings["tripadvisor"] = {
                    "score": ta_data["rating"],
                    "review_count": ta_data.get("rating_count", 0),
                    "source": "TripAdvisor"
                }
        
        return ratings
    
    def _enrich_activity_with_venues(self, activity: Dict, selected_venues: List[Dict]) -> Dict:
        """Enrich activity with OpenAI-selected venues"""
        
        enriched_activity = activity.copy()
        
        # Add OpenAI-selected venue recommendations
        enriched_activity["venue_recommendations"] = selected_venues[:3]  # Top 3
        enriched_activity["backup_venues"] = selected_venues[3:5] if len(selected_venues) > 3 else []
        
        # Add venue discovery metadata
        enriched_activity["venue_discovery"] = {
            "venues_found": len(selected_venues),
            "discovery_success": len(selected_venues) > 0,
            "selection_method": "openai_intelligent_selection",
            "top_venue_name": selected_venues[0]["name"] if selected_venues else "No venues found",
            "recommendation_quality": "excellent" if len(selected_venues) >= 3 else "good" if selected_venues else "none"
        }
        
        # Update activity with top venue info
        if selected_venues:
            top_venue = selected_venues[0]
            enriched_activity["recommended_venue"] = {
                "name": top_venue["name"],
                "address": top_venue.get("location", {}).get("address", "Address not available"),
                "type": top_venue["type"],
                "description": top_venue["description"],
                "openai_reasoning": top_venue.get("openai_selection_reasoning", "Selected for optimal date experience"),
                "why_recommended": f"OpenAI selected as the best match for {activity.get('name', 'this activity')} based on cultural intelligence and compatibility analysis"
            }
        
        return enriched_activity
    
    def _build_complete_date_plan(self, original_plan: Dict, enriched_activities: List[Dict], venue_results: List[Dict]) -> Dict:
        """Build complete date plan with OpenAI-enhanced venue information"""
        
        complete_plan = original_plan.copy()
        complete_plan["intelligent_date_plan"]["activities"] = enriched_activities
        
        if "original_context" in original_plan:
            complete_plan["original_context"] = original_plan["original_context"]

        # Add OpenAI-enhanced venue discovery summary
        total_candidates = sum(result["candidates_found"] for result in venue_results)
        total_selected = sum(result["venues_selected"] for result in venue_results)
        successful_discoveries = sum(1 for result in venue_results if result["venues_selected"] > 0)
        
        complete_plan["venue_discovery_summary"] = {
            "total_candidates_evaluated": total_candidates,
            "total_venues_selected": total_selected,
            "successful_activity_discoveries": successful_discoveries,
            "total_activities": len(venue_results),
            "discovery_success_rate": successful_discoveries / len(venue_results) if venue_results else 0,
            "selection_method": "openai_intelligent_curation",
            "venue_quality": "excellent" if successful_discoveries == len(venue_results) else "partial"
        }
        
        complete_plan["detailed_venue_results"] = venue_results
        
        # Update processing metadata
        if "processing_metadata" not in complete_plan:
            complete_plan["processing_metadata"] = {}
        
        complete_plan["processing_metadata"].update({
            "step_5_completed": True,
            "step_5_method": "openai_enhanced_venue_discovery",
            "venues_discovered": total_selected,
            "candidates_evaluated": total_candidates,
            "openai_venue_selection": True,
            "pipeline_complete": True,
            "ready_for_demo": successful_discoveries > 0
        })
        complete_plan["processing_metadata"]["input_context"] = original_plan.get("original_context")

        return complete_plan
    
    def _fallback_venue_response(self, original_plan: Dict, error_reason: str) -> Dict:
        """Fallback response when OpenAI-enhanced discovery fails"""
        
        fallback_plan = original_plan.copy()
        
        activities = fallback_plan.get("intelligent_date_plan", {}).get("activities", [])
        
        for activity in activities:
            activity["venue_recommendations"] = []
            activity["backup_venues"] = []
            activity["venue_discovery"] = {
                "venues_found": 0,
                "discovery_success": False,
                "selection_method": "fallback_mode",
                "error_reason": error_reason,
                "recommendation_quality": "none"
            }
        
        fallback_plan["venue_discovery_summary"] = {
            "total_candidates_evaluated": 0,
            "total_venues_selected": 0,
            "successful_activity_discoveries": 0,
            "total_activities": len(activities),
            "discovery_success_rate": 0,
            "selection_method": "fallback_mode",
            "venue_quality": "unavailable",
            "error_reason": error_reason
        }
        
        if "processing_metadata" not in fallback_plan:
            fallback_plan["processing_metadata"] = {}
            
        fallback_plan["processing_metadata"].update({
            "step_5_completed": False,
            "step_5_error": error_reason,
            "openai_venue_selection": False,
            "pipeline_complete": False,
            "ready_for_demo": False
        })
        
        return fallback_plan