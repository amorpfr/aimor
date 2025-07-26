#!/usr/bin/env python3
"""
Test Step 5: Venue Discovery Service
Using real output from the complete pipeline test
"""

import sys
import os
import json
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🏢 Testing Step 5: Venue Discovery Service")
print("=" * 50)

def test_step_5_with_real_queries():
    """Test Step 5 using the actual queries from your pipeline test"""
    
    # This is the actual output from your successful pipeline test
    mock_date_plan = {
        "compatibility_insights": {
            "overall_compatibility": 0.70,
            "shared_cultural_patterns": ["adventure", "art"],
            "connection_bridges": ["outdoor exploration", "cultural curiosity"]
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
                    "cultural_reasoning": "Combines Emma's photography interest with Alex's artistic nature",
                    "conversation_catalysts": ["art composition", "city exploration", "creative perspectives"],
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
                    "cultural_reasoning": "Matches Emma's explicit interest in Ethiopian cuisine with intimate dinner setting",
                    "conversation_catalysts": ["travel experiences", "cultural food traditions", "authentic connections"],
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
    
    print("📋 Test Input: Real date plan with Qloo-ready queries")
    print(f"   Activities: {len(mock_date_plan['qloo_ready_queries'])}")
    print(f"   Query 1: {mock_date_plan['qloo_ready_queries'][0]['activity_name']}")
    print(f"   Query 2: {mock_date_plan['qloo_ready_queries'][1]['activity_name']}")
    
    try:
        from services.venue_discoverer import VenueDiscoverer
        
        print("\n🔄 Initializing VenueDiscoverer...")
        discoverer = VenueDiscoverer()
        
        print("🔄 Executing venue discovery...")
        start_time = time.time()
        
        complete_plan = discoverer.discover_venues_for_date_plan(mock_date_plan)
        
        processing_time = time.time() - start_time
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        
        # Analyze results
        if complete_plan:
            venue_summary = complete_plan.get("venue_discovery_summary", {})
            activities = complete_plan.get("intelligent_date_plan", {}).get("activities", [])
            
            print(f"\n✅ Step 5 completed!")
            print(f"   Total venues found: {venue_summary.get('total_venues_found', 0)}")
            print(f"   Successful discoveries: {venue_summary.get('successful_activity_discoveries', 0)}/{venue_summary.get('total_activities', 0)}")
            print(f"   Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
            print(f"   Quality: {venue_summary.get('venue_quality', 'unknown')}")
            
            # Show venue details
            for i, activity in enumerate(activities):
                print(f"\n   🎯 Activity {i+1}: {activity.get('name', 'Unknown')}")
                
                venue_recs = activity.get("venue_recommendations", [])
                if venue_recs:
                    top_venue = venue_recs[0]
                    print(f"      🏢 Top venue: {top_venue.get('name', 'Unknown')}")
                    print(f"      📍 Address: {top_venue.get('location', {}).get('address', 'No address')}")
                    print(f"      ⭐ Qloo affinity: {top_venue.get('qloo_affinity', 0):.2f}")
                    print(f"      💰 Price level: {top_venue.get('business_info', {}).get('price_description', 'Unknown')}")
                    
                    # Show ratings if available
                    ratings = top_venue.get('ratings', {})
                    if ratings:
                        for rating_source, rating_data in ratings.items():
                            print(f"      ⭐ {rating_data['source']}: {rating_data['score']}/5")
                else:
                    discovery_info = activity.get("venue_discovery", {})
                    print(f"      ❌ No venues found")
                    if discovery_info.get("error_reason"):
                        print(f"      🔍 Error: {discovery_info['error_reason']}")
            
            return complete_plan
        else:
            print("❌ Step 5 failed - no response")
            return None
            
    except Exception as e:
        print(f"❌ Step 5 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_complete_pipeline(complete_plan):
    """Analyze the complete 5-step pipeline results"""
    
    if not complete_plan:
        print("\n❌ Cannot analyze - no complete plan")
        return
    
    print(f"\n🎉 COMPLETE 5-STEP PIPELINE ANALYSIS")
    print("=" * 50)
    
    # Pipeline completeness
    metadata = complete_plan.get("processing_metadata", {})
    print(f"✅ Pipeline complete: {metadata.get('pipeline_complete', False)}")
    print(f"✅ Demo ready: {metadata.get('ready_for_demo', False)}")
    
    # Performance metrics
    print(f"\n📊 PERFORMANCE METRICS:")
    print(f"   🎯 Cultural discoveries: {metadata.get('cultural_discoveries_analyzed', 0)}")
    print(f"   🔍 Qloo queries: {metadata.get('qloo_queries_generated', 0)}")
    print(f"   🏢 Venues discovered: {metadata.get('venues_discovered', 0)}")
    print(f"   🧠 Intelligence level: {metadata.get('intelligence_level', 'unknown')}")
    
    # Date plan quality
    compatibility = complete_plan.get("compatibility_insights", {})
    date_plan = complete_plan.get("intelligent_date_plan", {})
    
    print(f"\n💝 DATE PLAN QUALITY:")
    print(f"   Compatibility score: {compatibility.get('overall_compatibility', 0):.2f}")
    print(f"   Theme: {date_plan.get('theme', 'Unknown')}")
    print(f"   Duration: {date_plan.get('total_duration', 'Unknown')}")
    
    # Venue discovery success
    venue_summary = complete_plan.get("venue_discovery_summary", {})
    print(f"\n🏢 VENUE DISCOVERY SUCCESS:")
    print(f"   Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
    print(f"   Quality: {venue_summary.get('venue_quality', 'unknown')}")
    
    # Demo readiness assessment
    demo_ready = (
        metadata.get('pipeline_complete', False) and
        venue_summary.get('discovery_success_rate', 0) > 0.5 and
        compatibility.get('overall_compatibility', 0) > 0.6
    )
    
    print(f"\n🚀 DEMO READINESS: {'EXCELLENT!' if demo_ready else 'NEEDS WORK'}")
    if demo_ready:
        print("   Ready for hackathon presentation!")
        print("   All 5 steps working with real venue data")
    else:
        print("   Some components need refinement")

def main():
    """Test Step 5 with real pipeline data"""
    
    print("Testing Step 5 with your actual working pipeline output")
    
    # Check API connectivity
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        qloo_key = os.getenv("QLOO_API_KEY")
        if not qloo_key:
            print("❌ Qloo API key missing - Step 5 will fail")
            return
        else:
            print(f"✅ Qloo API key present")
    except Exception as e:
        print(f"❌ Environment setup error: {e}")
        return
    
    # Test Step 5
    complete_plan = test_step_5_with_real_queries()
    
    # Analyze complete pipeline
    analyze_complete_pipeline(complete_plan)
    
    if complete_plan and complete_plan.get("processing_metadata", {}).get("pipeline_complete"):
        print(f"\n🎯 NEXT STEPS:")
        print("1. ✅ All 5 steps working - ready for integration")
        print("2. 📝 Create /generate-complete-date-plan endpoint") 
        print("3. 🎨 Polish cultural discovery quality")
        print("4. 🚀 Demo preparation")

if __name__ == "__main__":
    main()