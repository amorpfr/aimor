#!/usr/bin/env python3
"""
Test OpenAI Enhanced Venue Discovery
Compare the new OpenAI-driven selection vs the old hardcoded approach
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🤖 Testing OpenAI Enhanced Venue Discovery")
print("=" * 60)

def test_openai_venue_enhancement():
    """Test the new OpenAI-enhanced venue discovery"""
    
    # Use the same test data that was working
    mock_date_plan = {
        "compatibility_insights": {
            "overall_compatibility": 0.70,
            "shared_cultural_patterns": ["adventure", "art", "authentic experiences"],
            "connection_bridges": ["outdoor exploration", "cultural curiosity", "photography interests"]
        },
        "intelligent_date_plan": {
            "theme": "Adventure and Art",
            "total_duration": "4 hours",
            "activities": [
                {
                    "sequence": 1,
                    "name": "Photography Walking Tour",
                    "type": "outdoor_activity",
                    "duration": "2 hours",
                    "cultural_reasoning": "Combines Emma's photography passion with Alex's artistic curiosity. Shared visual exploration creates natural conversation opportunities while allowing both personalities to shine.",
                    "conversation_catalysts": ["art composition", "city exploration", "creative perspectives", "hidden cultural stories"],
                    "qloo_parameters": {
                        "filter.type": "urn:entity:place",
                        "filter.location.query": "Amsterdam, Netherlands",
                        "signal.interests.entities": "577F84BA-A8CF-4EF4-AA08-6E60C8BB92CD,1A2556C2-237E-4A8C-9512-6D11E87E7A43",
                        "filter.tags": "outdoor,walking tour",
                        "filter.price_level.min": 1,
                        "filter.price_level.max": 3,
                        "filter.popularity.min": 0.5,
                        "take": 5
                    }
                },
                {
                    "sequence": 2,
                    "name": "Dinner at an Ethiopian Restaurant",
                    "type": "restaurant",
                    "duration": "2 hours",
                    "cultural_reasoning": "Matches Emma's explicit Ethiopian cuisine interest while providing intimate setting for deeper conversation. Cultural food sharing creates natural bonding opportunity.",
                    "conversation_catalysts": ["travel experiences", "cultural food traditions", "authentic connections", "personal story sharing"],
                    "qloo_parameters": {
                        "filter.type": "urn:entity:place",
                        "filter.location.query": "Amsterdam, Netherlands",
                        "signal.interests.entities": "16D791C3-DCF2-45FA-BA62-7A45BF233352,5021A7FE-3A09-4B5A-8E18-DD6AD83F0EEB",
                        "filter.tags": "restaurant,ethiopian",
                        "filter.price_level.min": 1,
                        "filter.price_level.max": 3,
                        "filter.popularity.min": 0.5,
                        "take": 5
                    }
                }
            ]
        },
        "qloo_ready_queries": [
            {
                "activity_name": "Photography Walking Tour",
                "parameters": {
                    "filter.type": "urn:entity:place",
                    "filter.location.query": "Amsterdam, Netherlands", 
                    "signal.interests.entities": "577F84BA-A8CF-4EF4-AA08-6E60C8BB92CD,1A2556C2-237E-4A8C-9512-6D11E87E7A43",
                    "filter.tags": "outdoor,walking tour",
                    "filter.price_level.min": 1,
                    "filter.price_level.max": 3,
                    "filter.popularity.min": 0.5,
                    "take": 5
                }
            },
            {
                "activity_name": "Dinner at an Ethiopian Restaurant",
                "parameters": {
                    "filter.type": "urn:entity:place",
                    "filter.location.query": "Amsterdam, Netherlands",
                    "signal.interests.entities": "16D791C3-DCF2-45FA-BA62-7A45BF233352,5021A7FE-3A09-4B5A-8E18-DD6AD83F0EEB", 
                    "filter.tags": "restaurant,ethiopian",
                    "filter.price_level.min": 1,
                    "filter.price_level.max": 3,
                    "filter.popularity.min": 0.5,
                    "take": 5
                }
            }
        ]
    }
    
    print("📋 Test Input: Real date plan with OpenAI enhancement")
    print(f"   Theme: {mock_date_plan['intelligent_date_plan']['theme']}")
    print(f"   Compatibility: {mock_date_plan['compatibility_insights']['overall_compatibility']}")
    print(f"   Activities: {len(mock_date_plan['qloo_ready_queries'])}")
    
    try:
        # Import the new OpenAI-enhanced venue discoverer
        from services.venue_discoverer import VenueDiscoverer
        
        print("\n🤖 Initializing OpenAI-Enhanced VenueDiscoverer...")
        discoverer = VenueDiscoverer()
        
        if not discoverer.openai_available:
            print("⚠️  OpenAI not available - will use fallback selection")
        else:
            print("✅ OpenAI client initialized successfully")
        
        print("\n🔄 Executing OpenAI-enhanced venue discovery...")
        start_time = time.time()
        
        complete_plan = discoverer.discover_venues_for_date_plan(mock_date_plan)
        
        processing_time = time.time() - start_time
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        
        # Analyze OpenAI enhancement results
        if complete_plan:
            venue_summary = complete_plan.get("venue_discovery_summary", {})
            activities = complete_plan.get("intelligent_date_plan", {}).get("activities", [])
            
            print(f"\n✅ OpenAI-Enhanced Discovery Results:")
            print(f"   Selection method: {venue_summary.get('selection_method', 'unknown')}")
            print(f"   Candidates evaluated: {venue_summary.get('total_candidates_evaluated', 0)}")
            print(f"   Venues selected: {venue_summary.get('total_venues_selected', 0)}")
            print(f"   Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
            print(f"   Quality: {venue_summary.get('venue_quality', 'unknown')}")
            
            # Show detailed venue analysis
            for i, activity in enumerate(activities):
                print(f"\n   🎯 Activity {i+1}: {activity.get('name', 'Unknown')}")
                
                venue_recs = activity.get("venue_recommendations", [])
                if venue_recs:
                    top_venue = venue_recs[0]
                    print(f"      🏢 Top venue: {top_venue.get('name', 'Unknown')}")
                    print(f"      📍 Address: {top_venue.get('location', {}).get('address', 'No address')}")
                    print(f"      🤖 OpenAI reasoning: {top_venue.get('openai_selection_reasoning', 'No reasoning provided')}")
                    print(f"      🏆 OpenAI ranking: {top_venue.get('openai_ranking', 'N/A')}")
                    print(f"      ⭐ Qloo affinity: {top_venue.get('qloo_affinity', 0):.2f}")
                    
                    # Show business info
                    business_info = top_venue.get('business_info', {})
                    if business_info:
                        print(f"      💰 Price level: {business_info.get('price_description', 'Unknown')}")
                        if business_info.get('phone'):
                            print(f"      📞 Phone: {business_info['phone']}")
                    
                    # Show ratings
                    ratings = top_venue.get('ratings', {})
                    for rating_source, rating_data in ratings.items():
                        if isinstance(rating_data, dict) and rating_data.get('score'):
                            print(f"      ⭐ {rating_data.get('source', rating_source)}: {rating_data['score']}/5")
                    
                    # Show all venue options
                    if len(venue_recs) > 1:
                        print(f"      📋 Alternative options:")
                        for j, alt_venue in enumerate(venue_recs[1:3], 2):
                            print(f"         {j}. {alt_venue.get('name', 'Unknown')} (Ranking: {alt_venue.get('openai_ranking', 'N/A')})")
                else:
                    discovery_info = activity.get("venue_discovery", {})
                    print(f"      ❌ No venues selected")
                    if discovery_info.get("error_reason"):
                        print(f"      🔍 Error: {discovery_info['error_reason']}")
            
            return complete_plan
        else:
            print("❌ OpenAI-enhanced discovery failed - no response")
            return None
            
    except Exception as e:
        print(f"❌ OpenAI-enhanced discovery error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_openai_enhancement_quality(complete_plan):
    """Analyze the quality of OpenAI venue enhancement"""
    
    if not complete_plan:
        print("\n❌ Cannot analyze - no complete plan")
        return
    
    print(f"\n🧠 OPENAI ENHANCEMENT QUALITY ANALYSIS")
    print("=" * 60)
    
    # Check if OpenAI was actually used
    metadata = complete_plan.get("processing_metadata", {})
    openai_used = metadata.get("openai_venue_selection", False)
    
    print(f"🤖 OpenAI Selection Used: {openai_used}")
    
    if openai_used:
        print("✅ ENHANCED FEATURES DETECTED:")
        
        # Check for OpenAI reasoning in venues
        activities = complete_plan.get("intelligent_date_plan", {}).get("activities", [])
        
        reasoning_found = False
        ranking_found = False
        intelligent_selection = False
        
        for activity in activities:
            venue_recs = activity.get("venue_recommendations", [])
            for venue in venue_recs:
                if venue.get("openai_selection_reasoning"):
                    reasoning_found = True
                    print(f"   🧠 Intelligent reasoning: '{venue['openai_selection_reasoning'][:100]}...'")
                
                if venue.get("openai_ranking"):
                    ranking_found = True
                
                if venue.get("openai_selection_reasoning") and "perfect" in venue["openai_selection_reasoning"].lower():
                    intelligent_selection = True
        
        # Quality indicators
        venue_summary = complete_plan.get("venue_discovery_summary", {})
        candidates_evaluated = venue_summary.get("total_candidates_evaluated", 0)
        venues_selected = venue_summary.get("total_venues_selected", 0)
        
        print(f"   📊 Candidates evaluated: {candidates_evaluated}")
        print(f"   🎯 Intelligent selection ratio: {venues_selected}/{candidates_evaluated}")
        print(f"   🏆 Ranking system: {'✅ Working' if ranking_found else '❌ Missing'}")
        print(f"   🧠 Reasoning quality: {'✅ Intelligent' if intelligent_selection else '⚠️ Basic'}")
        
        # Compare venue types for diversity
        venue_types = []
        for activity in activities:
            venue_recs = activity.get("venue_recommendations", [])
            if venue_recs:
                top_venue = venue_recs[0]
                venue_name = top_venue.get("name", "Unknown")
                venue_types.append(venue_name)
            else:
                venue_types.append("No venue")
        
        unique_venues = len(set(venue_types))
        total_activities = len(activities)
        
        print(f"   🎯 Venue diversity: {unique_venues}/{total_activities} unique venues")
        
        if unique_venues == total_activities:
            print("   ✅ PERFECT DIVERSITY: Each activity has different venue type!")
        elif unique_venues > 1:
            print("   ✅ GOOD DIVERSITY: Multiple different venues selected")
        else:
            print("   ⚠️ LIMITED DIVERSITY: Same venue type for different activities")
    
    else:
        print("⚠️  OpenAI enhancement not used - fell back to basic selection")
    
    # Overall assessment
    success_indicators = [
        openai_used,
        reasoning_found,
        ranking_found,
        metadata.get("venues_discovered", 0) > 0
    ]
    
    success_score = sum(success_indicators) / len(success_indicators)
    
    print(f"\n🎯 ENHANCEMENT SUCCESS SCORE: {success_score:.1%}")
    
    if success_score >= 0.75:
        print("🚀 EXCELLENT: OpenAI enhancement working optimally!")
    elif success_score >= 0.5:
        print("✅ GOOD: OpenAI enhancement mostly working")
    else:
        print("⚠️ NEEDS WORK: OpenAI enhancement not fully functional")

def compare_with_previous_approach():
    """Compare with the previous hardcoded approach"""
    
    print(f"\n📊 ENHANCEMENT COMPARISON")
    print("=" * 60)
    
    print("🔧 PREVIOUS APPROACH (Hardcoded):")
    print("   ❌ Hardcoded keyword filtering ('restaurant', 'tour', etc.)")
    print("   ❌ Simple string matching for venue types")
    print("   ❌ No intelligent reasoning for selections")
    print("   ❌ Limited to predefined categories")
    print("   ❌ Same logic for all personality types")
    
    print("\n🤖 NEW APPROACH (OpenAI Enhanced):")
    print("   ✅ AI-driven venue selection with reasoning")
    print("   ✅ Psychological compatibility consideration")
    print("   ✅ Contextual analysis of date theme and purpose")
    print("   ✅ Flexible adaptation to any activity type")
    print("   ✅ Intelligent ranking system")
    print("   ✅ Conversation opportunity analysis")
    
    print("\n🎯 KEY IMPROVEMENTS:")
    print("   1. No more hardcoded keyword lists")
    print("   2. Venue selection considers psychological compatibility")
    print("   3. Reasoning provided for each venue choice")
    print("   4. Adaptable to any date theme or activity")
    print("   5. Higher quality, more thoughtful selections")

def main():
    """Run OpenAI enhancement testing"""
    
    print("Testing the new OpenAI-enhanced venue discovery system")
    print("Goal: Intelligent venue selection vs hardcoded filtering")
    
    # Check API connectivity
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv("OPENAI_API_KEY")
        qloo_key = os.getenv("QLOO_API_KEY")
        
        if not openai_key:
            print("❌ OpenAI API key missing - enhancement will fall back to basic selection")
        else:
            print(f"✅ OpenAI API key present")
            
        if not qloo_key:
            print("❌ Qloo API key missing - venue discovery will fail")
            return
        else:
            print(f"✅ Qloo API key present")
    except Exception as e:
        print(f"❌ Environment setup error: {e}")
        return
    
    # Test OpenAI enhancement
    complete_plan = test_openai_venue_enhancement()
    
    # Analyze enhancement quality
    analyze_openai_enhancement_quality(complete_plan)
    
    # Compare approaches
    compare_with_previous_approach()
    
    if complete_plan and complete_plan.get("processing_metadata", {}).get("openai_venue_selection"):
        print(f"\n🎯 NEXT STEPS:")
        print("1. ✅ OpenAI venue enhancement working - ready for Step 6!")
        print("2. 📝 Build Final Intelligence Layer (Step 6)")
        print("3. 🔗 Create complete pipeline endpoint") 
        print("4. 🚀 Deploy to Heroku")
    else:
        print(f"\n🔧 DEBUGGING NEEDED:")
        print("1. Check OpenAI API connectivity")
        print("2. Verify venue candidate generation from Qloo")
        print("3. Debug OpenAI prompt and response parsing")

if __name__ == "__main__":
    main()