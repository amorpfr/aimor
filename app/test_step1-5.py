#!/usr/bin/env python3
"""
Test Complete Steps 1-5 Pipeline
Two real profiles → Complete date plan with actual venues
No hardcoding, pure AI pipeline test
"""

import sys
import os
import time
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔥 COMPLETE STEPS 1-5 PIPELINE TEST")
print("=" * 60)
print("Two Real Profiles → Complete Date Plan with Venues")
print("No hardcoding - pure AI cultural intelligence pipeline")
print("=" * 60)

def test_complete_pipeline_two_profiles():
    """Test complete pipeline with two different profile inputs"""
    
    # Two distinct, realistic profiles
    profile_a = {
        "text": """Maya, 29, urban planner from Amsterdam. Passionate about sustainable architecture and community gardens. 
        Weekends spent cycling through different neighborhoods, discovering local markets and street art. 
        Love experimental cuisine and intimate wine bars. Currently learning ceramics. Values authenticity over trends, 
        deep conversations over small talk. Looking for someone who appreciates both city culture and environmental consciousness.""",
        
        "context": {
            "location": "amsterdam",
            "time_of_day": "afternoon",
            "season": "spring",
            "duration": "5 hours",
            "date_type": "first_date"
        }
    }
    
    profile_b = {
        "text": """Carlos, 27, documentary filmmaker originally from Barcelona, now based in Amsterdam. 
        Fascinated by human stories and social movements. Spends time in art house cinemas, underground music venues, 
        and community workshops. Vegetarian who loves exploring plant-based restaurants and cooking collaboratively. 
        Practices meditation and values mindful living. Seeks genuine connections with people who think deeply about the world.""",
        
        "context": {
            "location": "amsterdam", 
            "time_of_day": "afternoon",
            "season": "spring",
            "duration": "5 hours",
            "date_type": "first_date"
        }
    }
    
    print(f"👤 PROFILE A: Maya (Urban Planner)")
    print(f"   Interests: Sustainable architecture, community gardens, cycling, street art")
    print(f"   Values: Authenticity, environmental consciousness, deep conversations")
    
    print(f"\n👤 PROFILE B: Carlos (Documentary Filmmaker)")
    print(f"   Interests: Human stories, art house cinema, underground music, plant-based food")
    print(f"   Values: Social awareness, mindful living, genuine connections")
    
    print(f"\n⚙️  CONTEXT: Amsterdam, Spring afternoon, 5-hour first date")
    
    return profile_a, profile_b

def execute_step_1_2(profile_data, profile_name):
    """Execute Steps 1-2: Profile Analysis + Cultural Enhancement"""
    
    print(f"\n🧠 STEPS 1-2: {profile_name}")
    print("-" * 40)
    
    try:
        # Step 1: Profile Analysis
        from services.profile_processor import ProfileProcessor
        
        print(f"   🔄 Step 1: Analyzing {profile_name}...")
        start_time = time.time()
        
        processor = ProfileProcessor()
        step1_result = processor.process_profile_with_context(
            text=profile_data["text"],
            context=profile_data["context"]
        )
        
        step1_time = time.time() - start_time
        
        if not step1_result.get("success"):
            print(f"   ❌ Step 1 failed: {step1_result.get('error', 'Unknown error')}")
            return None
        
        analysis = step1_result["analysis"]
        confidence = analysis.get("processing_confidence", 0)
        print(f"   ✅ Step 1 complete - Confidence: {confidence:.2f} ({step1_time:.1f}s)")
        
        # Show key psychological insights
        psychology = analysis.get("advanced_psychological_profile", {})
        big_five = psychology.get("big_five_detailed", {})
        dating_psych = psychology.get("dating_psychology", {})
        
        print(f"   🧠 Key traits: Openness {big_five.get('openness', {}).get('score', 0):.2f}, "
              f"Adventurousness {dating_psych.get('adventurousness', {}).get('score', 0):.2f}")
        
        # Step 2: Cultural Enhancement
        from services.profile_enricher import ProfileEnricher
        
        print(f"   🔄 Step 2: Cultural enhancement...")
        step2_start = time.time()
        
        enricher = ProfileEnricher()
        step2_result = enricher.process_psychological_profile(
            analysis, profile_data["context"]
        )
        
        step2_time = time.time() - step2_start
        
        if not step2_result.get("success"):
            print(f"   ❌ Step 2 failed: {step2_result.get('error', 'Unknown error')}")
            return step1_result
        
        metadata = step2_result.get("processing_metadata", {})
        discoveries = metadata.get("total_new_discoveries", 0)
        cultural_depth = metadata.get("cultural_depth_enhancement", 0)
        
        print(f"   ✅ Step 2 complete - Discoveries: {discoveries}, Depth: {cultural_depth:.2f} ({step2_time:.1f}s)")
        
        # Show sample cultural discoveries
        cross_domain = step2_result.get("cross_domain_discoveries", {})
        for category, items in cross_domain.items():
            if isinstance(items, list) and items and category != "discovery_confidence":
                sample_names = [item.get("name", "Unknown") for item in items[:2] if isinstance(item, dict)]
                if sample_names:
                    print(f"   🎯 {category}: {', '.join(sample_names)}")
        
        return step2_result
        
    except Exception as e:
        print(f"   ❌ Steps 1-2 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def execute_step_3_4(enriched_profile_a, enriched_profile_b, context):
    """Execute Steps 3-4: Date Intelligence Engine"""
    
    print(f"\n💝 STEPS 3-4: Date Intelligence Engine")
    print("-" * 40)
    
    try:
        from services.date_intelligence_engine import DateIntelligenceEngine
        
        print(f"   🔄 Creating intelligent date plan...")
        start_time = time.time()
        
        engine = DateIntelligenceEngine()
        date_plan = engine.create_intelligent_date_plan(
            enriched_profile_a=enriched_profile_a,
            enriched_profile_b=enriched_profile_b,
            context=context
        )
        
        processing_time = time.time() - start_time
        
        if not date_plan or date_plan.get("error"):
            print(f"   ❌ Steps 3-4 failed: {date_plan.get('error', 'Unknown error')}")
            return None
        
        # Analyze date intelligence results
        compatibility = date_plan.get("compatibility_insights", {})
        intelligent_plan = date_plan.get("intelligent_date_plan", {})
        qloo_queries = date_plan.get("qloo_ready_queries", [])
        
        print(f"   ✅ Date plan created ({processing_time:.1f}s)")
        print(f"   💝 Compatibility: {compatibility.get('overall_compatibility', 0):.2f}")
        print(f"   🎨 Theme: {intelligent_plan.get('theme', 'Unknown')}")
        print(f"   🕐 Duration: {intelligent_plan.get('total_duration', 'Unknown')}")
        print(f"   🎯 Activities: {len(intelligent_plan.get('activities', []))}")
        print(f"   🔍 Qloo queries: {len(qloo_queries)}")
        
        # Show activity preview
        activities = intelligent_plan.get("activities", [])
        for i, activity in enumerate(activities[:2]):
            print(f"   📍 Activity {i+1}: {activity.get('name', 'Unknown')} ({activity.get('duration', 'Unknown')})")
            reasoning = activity.get('cultural_reasoning', '')
            if reasoning:
                print(f"      💭 Why: {reasoning[:80]}...")
        
        return date_plan
        
    except Exception as e:
        print(f"   ❌ Steps 3-4 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def execute_step_5(date_plan):
    """Execute Step 5: OpenAI-Enhanced Venue Discovery"""
    
    print(f"\n🏢 STEP 5: OpenAI-Enhanced Venue Discovery")
    print("-" * 40)
    
    try:
        from services.venue_discoverer import VenueDiscoverer
        
        print(f"   🔄 Discovering venues with OpenAI intelligence...")
        start_time = time.time()
        
        discoverer = VenueDiscoverer()
        
        if not discoverer.openai_available:
            print("   ⚠️  OpenAI not available - using fallback selection")
        
        complete_plan = discoverer.discover_venues_for_date_plan(date_plan)
        
        processing_time = time.time() - start_time
        
        if not complete_plan:
            print("   ❌ Step 5 failed - no response")
            return None
        
        # Analyze venue discovery results
        venue_summary = complete_plan.get("venue_discovery_summary", {})
        activities = complete_plan.get("intelligent_date_plan", {}).get("activities", [])
        
        print(f"   ✅ Venue discovery complete ({processing_time:.1f}s)")
        print(f"   🏢 Method: {venue_summary.get('selection_method', 'unknown')}")
        print(f"   📊 Candidates: {venue_summary.get('total_candidates_evaluated', 0)}")
        print(f"   🎯 Selected: {venue_summary.get('total_venues_selected', 0)}")
        print(f"   ✅ Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
        
        # Show venue details
        for i, activity in enumerate(activities):
            print(f"\n   🎯 Activity {i+1}: {activity.get('name', 'Unknown')}")
            
            venue_recs = activity.get("venue_recommendations", [])
            if venue_recs:
                top_venue = venue_recs[0]
                print(f"      🏢 Venue: {top_venue.get('name', 'Unknown')}")
                print(f"      📍 Location: {top_venue.get('location', {}).get('address', 'No address')}")
                
                # Show OpenAI reasoning
                reasoning = top_venue.get("openai_selection_reasoning", "")
                if reasoning:
                    print(f"      🤖 AI Reasoning: {reasoning}")
                
                # Show ratings and practical info
                ratings = top_venue.get('ratings', {})
                for rating_source, rating_data in ratings.items():
                    if isinstance(rating_data, dict) and rating_data.get('score'):
                        print(f"      ⭐ {rating_data.get('source', rating_source)}: {rating_data['score']}/5")
                
                business_info = top_venue.get('business_info', {})
                if business_info.get('price_description'):
                    print(f"      💰 Price: {business_info['price_description']}")
                if business_info.get('phone'):
                    print(f"      📞 Phone: {business_info['phone']}")
            else:
                print(f"      ❌ No venues found")
        
        return complete_plan
        
    except Exception as e:
        print(f"   ❌ Step 5 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_complete_pipeline_results(final_result):
    """Analyze the complete 5-step pipeline results AND show raw output"""
    
    if not final_result:
        print("\n❌ Cannot analyze - pipeline failed")
        return
    
    print(f"\n🎉 COMPLETE PIPELINE ANALYSIS")
    print("=" * 60)
    
    # First show raw JSON structure
    print(f"\n📄 RAW OUTPUT STRUCTURE:")
    print("-" * 30)
    
    def show_json_structure(data, prefix="", max_depth=3, current_depth=0):
        """Show JSON structure without overwhelming detail"""
        if current_depth >= max_depth:
            return
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"{prefix}📁 {key}: {{...}} ({len(value)} keys)")
                    if current_depth < max_depth - 1:
                        show_json_structure(value, prefix + "  ", max_depth, current_depth + 1)
                elif isinstance(value, list):
                    print(f"{prefix}📋 {key}: [...] ({len(value)} items)")
                    if value and current_depth < max_depth - 1:
                        print(f"{prefix}  └─ Sample item type: {type(value[0]).__name__}")
                        if isinstance(value[0], dict):
                            show_json_structure(value[0], prefix + "    ", max_depth, current_depth + 2)
                else:
                    if isinstance(value, str) and len(value) > 50:
                        print(f"{prefix}📝 {key}: \"{value[:50]}...\"")
                    else:
                        print(f"{prefix}📝 {key}: {value}")
        elif isinstance(data, list):
            print(f"{prefix}📋 List with {len(data)} items")
            if data:
                show_json_structure(data[0], prefix + "  ", max_depth, current_depth + 1)
    
    print("🔍 COMPLETE OUTPUT STRUCTURE:")
    show_json_structure(final_result)
    
    # Show key sections in detail
    print(f"\n📊 KEY SECTIONS DETAIL:")
    print("-" * 30)
    
    # Compatibility insights
    compatibility = final_result.get("compatibility_insights", {})
    if compatibility:
        print(f"\n💝 COMPATIBILITY_INSIGHTS:")
        print(json.dumps(compatibility, indent=2)[:500] + "..." if len(str(compatibility)) > 500 else json.dumps(compatibility, indent=2))
    
    # Date plan activities
    activities = final_result.get("intelligent_date_plan", {}).get("activities", [])
    if activities:
        print(f"\n🎯 ACTIVITIES (showing first activity):")
        print(json.dumps(activities[0], indent=2)[:800] + "..." if len(str(activities[0])) > 800 else json.dumps(activities[0], indent=2))
    
    # Venue recommendations
    if activities and activities[0].get("venue_recommendations"):
        print(f"\n🏢 VENUE_RECOMMENDATIONS (showing first venue):")
        venue = activities[0]["venue_recommendations"][0]
        print(json.dumps(venue, indent=2)[:600] + "..." if len(str(venue)) > 600 else json.dumps(venue, indent=2))
    
    # Cultural intelligence reasoning
    cultural_reasoning = final_result.get("cultural_intelligence_reasoning", {})
    if cultural_reasoning:
        print(f"\n🧠 CULTURAL_INTELLIGENCE_REASONING:")
        print(json.dumps(cultural_reasoning, indent=2)[:500] + "..." if len(str(cultural_reasoning)) > 500 else json.dumps(cultural_reasoning, indent=2))
    
    # Processing metadata
    metadata = final_result.get("processing_metadata", {})
    if metadata:
        print(f"\n⚙️  PROCESSING_METADATA:")
        print(json.dumps(metadata, indent=2))
    
    # FULL JSON OUTPUT (truncated for readability)
    print(f"\n📋 COMPLETE RAW JSON OUTPUT:")
    print("=" * 40)
    full_json = json.dumps(final_result, indent=2)
    if len(full_json) > 3000:
        print(full_json[:3000])
        print(f"\n... [TRUNCATED - Full output is {len(full_json)} characters] ...")
        print(f"\n🔍 To see complete output, add this to your test:")
        print(f"   print(json.dumps(final_result, indent=2))")
    else:
        print(full_json)
    
    # Now do the analysis...
    print(f"\n" + "=" * 60)
    print(f"🏁 PIPELINE STATUS ANALYSIS")
    print(f"=" * 60)
    
    # Pipeline completeness
    metadata = final_result.get("processing_metadata", {})
    
    print(f"🏁 PIPELINE STATUS:")
    print(f"   ✅ Pipeline complete: {metadata.get('pipeline_complete', False)}")
    print(f"   ✅ Demo ready: {metadata.get('ready_for_demo', False)}")
    print(f"   🤖 OpenAI venue selection: {metadata.get('openai_venue_selection', False)}")
    
    # Performance metrics
    print(f"\n📊 PERFORMANCE METRICS:")
    print(f"   🎯 Cultural discoveries: {metadata.get('cultural_discoveries_analyzed', 0)}")
    print(f"   🔍 Qloo queries: {metadata.get('qloo_queries_generated', 0)}")
    print(f"   🏢 Venue candidates: {metadata.get('candidates_evaluated', 0)}")
    print(f"   🎯 Venues selected: {metadata.get('venues_discovered', 0)}")
    
    # Date plan quality
    compatibility = final_result.get("compatibility_insights", {})
    date_plan = final_result.get("intelligent_date_plan", {})
    
    print(f"\n💝 DATE PLAN QUALITY:")
    print(f"   Compatibility score: {compatibility.get('overall_compatibility', 0):.2f}")
    print(f"   Theme: {date_plan.get('theme', 'Unknown')}")
    print(f"   Duration: {date_plan.get('total_duration', 'Unknown')}")
    print(f"   Activities: {len(date_plan.get('activities', []))}")
    
    # Cultural intelligence insights
    cultural_reasoning = final_result.get("cultural_intelligence_reasoning", {})
    
    print(f"\n🧠 CULTURAL INTELLIGENCE:")
    connections = cultural_reasoning.get("cross_domain_connections", [])
    if connections:
        print(f"   Cross-domain connections: {len(connections)} discovered")
        for connection in connections[:2]:
            print(f"   🔗 {connection}")
    
    # Venue discovery success
    venue_summary = final_result.get("venue_discovery_summary", {})
    
    print(f"\n🏢 VENUE INTELLIGENCE:")
    print(f"   Selection method: {venue_summary.get('selection_method', 'unknown')}")
    print(f"   Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
    print(f"   Quality: {venue_summary.get('venue_quality', 'unknown')}")
    
    # What makes this impressive for demo
    print(f"\n🚀 DEMO APPEAL FACTORS:")
    
    appeal_factors = []
    
    if compatibility.get('overall_compatibility', 0) > 0.7:
        appeal_factors.append("High compatibility score (>70%)")
    
    if metadata.get('openai_venue_selection'):
        appeal_factors.append("AI-driven venue selection with reasoning")
    
    if venue_summary.get('discovery_success_rate', 0) == 1.0:
        appeal_factors.append("100% venue discovery success")
    
    activities = date_plan.get('activities', [])
    unique_venue_types = set()
    for activity in activities:
        venue_recs = activity.get('venue_recommendations', [])
        if venue_recs:
            unique_venue_types.add(venue_recs[0].get('name', 'Unknown'))
    
    if len(unique_venue_types) == len(activities) and len(activities) > 1:
        appeal_factors.append("Perfect venue diversity (no duplicates)")
    
    if len(appeal_factors) >= 3:
        print(f"   🔥 HIGHLY IMPRESSIVE: {len(appeal_factors)} strong factors")
        for factor in appeal_factors:
            print(f"   ✅ {factor}")
    else:
        print(f"   ⚠️  NEEDS IMPROVEMENT: Only {len(appeal_factors)} strong factors")
    
    return len(appeal_factors) >= 3

def main():
    """Run complete Steps 1-5 pipeline test"""
    
    # Check API connectivity
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv("OPENAI_API_KEY")
        qloo_key = os.getenv("QLOO_API_KEY")
        
        if not openai_key or not qloo_key:
            print("❌ Missing API keys - pipeline will fail")
            return
        
        print(f"✅ API keys configured")
    except Exception as e:
        print(f"❌ Environment setup error: {e}")
        return
    
    print(f"\n🚀 STARTING COMPLETE PIPELINE TEST")
    total_start_time = time.time()
    
    # Setup test profiles
    profile_a, profile_b = test_complete_pipeline_two_profiles()
    
    # Execute Steps 1-2 for both profiles
    enriched_profile_a = execute_step_1_2(profile_a, "Maya (Urban Planner)")
    enriched_profile_b = execute_step_1_2(profile_b, "Carlos (Filmmaker)")
    
    if not enriched_profile_a or not enriched_profile_b:
        print("\n❌ Pipeline failed at Steps 1-2")
        return
    
    # Execute Steps 3-4: Date Intelligence
    date_plan = execute_step_3_4(enriched_profile_a, enriched_profile_b, profile_a["context"])
    
    if not date_plan:
        print("\n❌ Pipeline failed at Steps 3-4")
        return
    
    # Execute Step 5: Venue Discovery
    final_result = execute_step_5(date_plan)
    
    total_time = time.time() - total_start_time
    
    print(f"\n⏱️  TOTAL PIPELINE TIME: {total_time:.1f} seconds")
    
    # Analyze complete results
    is_impressive = analyze_complete_pipeline_results(final_result)
    
    print(f"\n🎯 PIPELINE READINESS ASSESSMENT:")
    if is_impressive and final_result:
        print(f"🚀 READY FOR STEP 6: Pipeline produces impressive, diverse results!")
        print(f"   Perfect foundation for comprehensive output structuring")
        print(f"   All AI components working with real intelligence")
    else:
        print(f"🔧 NEEDS REFINEMENT: Pipeline works but results need improvement")
        print(f"   Consider debugging specific components before Step 6")
    
    print(f"\n📋 NEXT DEVELOPMENT PRIORITIES:")
    print(f"1. Build Step 6: Final Intelligence Layer for comprehensive output")
    print(f"2. Create complete pipeline endpoint (/generate-complete-date-plan)")
    print(f"3. Deploy to Heroku for frontend integration")

if __name__ == "__main__":
    main()