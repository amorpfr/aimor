#!/usr/bin/env python3
"""
Test Complete Steps 1-6 Pipeline
Context Debugging + Full Cultural Intelligence Dating Engine Test
"""

import sys
import os
import time
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔥 COMPLETE STEPS 1-6 PIPELINE TEST")
print("=" * 70)
print("Two Real Profiles → Complete Date Plan with Step 6 Final Intelligence")
print("Context Debugging + Realistic Date Planning")
print("=" * 70)

def test_complete_pipeline_with_context():
    """Test complete pipeline with explicit context debugging"""
    
    # Two distinct, realistic profiles with EXPLICIT CONTEXT
    profile_a = {
        "text": """Emma, 28, sustainable fashion designer from Rotterdam. Passionate about ethical fashion and zero-waste living. 
        Weekends spent exploring local farmers markets, upcycling vintage finds, and photographing street art. 
        Love plant-based restaurants and cozy wine bars. Currently learning pottery. Values authenticity over trends, 
        meaningful conversations over small talk. Looking for someone who appreciates both creativity and environmental consciousness.""",
        
        "context": {
            "location": "rotterdam",
            "time_of_day": "afternoon", 
            "season": "spring",
            "duration": "4 hours",
            "date_type": "first_date"
        }
    }
    
    profile_b = {
        "text": """Liam, 30, urban photographer originally from London, now based in Rotterdam. 
        Fascinated by city architecture and hidden cultural spots. Spends time in independent bookshops, art galleries, 
        and local coffee roasters. Vegetarian who loves discovering hole-in-the-wall eateries and craft breweries. 
        Practices mindfulness and values genuine connections. Seeks authentic experiences with people who see beauty in everyday moments.""",
        
        "context": {
            "location": "rotterdam", 
            "time_of_day": "afternoon",
            "season": "spring", 
            "duration": "4 hours",
            "date_type": "first_date"
        }
    }
    
    print(f"👤 PROFILE A: Emma (Sustainable Fashion Designer)")
    print(f"   Interests: Ethical fashion, zero-waste, farmers markets, street art")
    print(f"   Values: Creativity, environmental consciousness, authenticity")
    
    print(f"\n👤 PROFILE B: Liam (Urban Photographer)")
    print(f"   Interests: Architecture photography, bookshops, art galleries, coffee")
    print(f"   Values: Mindfulness, genuine connections, everyday beauty")
    
    print(f"\n⚙️  EXPLICIT CONTEXT:")
    print(f"   📍 Location: {profile_a['context']['location']}")
    print(f"   🕐 Time: {profile_a['context']['time_of_day']}")
    print(f"   🌸 Season: {profile_a['context']['season']}")
    print(f"   ⏱️  Duration: {profile_a['context']['duration']}")
    print(f"   💕 Type: {profile_a['context']['date_type']}")
    
    return profile_a, profile_b

def execute_steps_1_2(profile_data, profile_name):
    """Execute Steps 1-2: Profile Analysis + Cultural Enhancement"""
    
    print(f"\n🧠 STEPS 1-2: {profile_name}")
    print("-" * 50)
    
    try:
        # Step 1: Profile Analysis
        from services.profile_analyzer_optimized import ProfileProcessorOptimized as ProfileProcessor
        
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
        
        print(f"   ✅ Step 2 complete - Discoveries: {discoveries} ({step2_time:.1f}s)")
        
        # Show personalized discoveries (check if they're different)
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

def execute_steps_3_4(enriched_profile_a, enriched_profile_b, context):
    """Execute Steps 3-4: Date Intelligence Engine"""
    
    print(f"\n💝 STEPS 3-4: Date Intelligence Engine")
    print("-" * 50)
    
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
        
        print(f"   ✅ Date plan created ({processing_time:.1f}s)")
        print(f"   💝 Compatibility: {compatibility.get('overall_compatibility', 0):.2f}")
        print(f"   🎨 Theme: {intelligent_plan.get('theme', 'Unknown')}")
        print(f"   🕐 Duration: {intelligent_plan.get('total_duration', 'Unknown')}")
        
        return date_plan
        
    except Exception as e:
        print(f"   ❌ Steps 3-4 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def execute_step_5(date_plan):
    """Execute Step 5: OpenAI-Enhanced Venue Discovery"""
    
    print(f"\n🏢 STEP 5: OpenAI-Enhanced Venue Discovery")
    print("-" * 50)
    
    try:
        from services.venue_discoverer import VenueDiscoverer
        
        print(f"   🔄 Discovering venues with OpenAI intelligence...")
        start_time = time.time()
        
        discoverer = VenueDiscoverer()
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
        print(f"   🎯 Selected: {venue_summary.get('total_venues_selected', 0)}")
        print(f"   ✅ Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
        
        return complete_plan
        
    except Exception as e:
        print(f"   ❌ Step 5 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def debug_step5_context(step5_output):
    """Debug what context is actually available in Step 5 output"""
    
    print(f"\n🔍 STEP 5 CONTEXT DEBUGGING")
    print("=" * 50)
    
    print("📋 Checking for context in Step 5 output...")
    
    # Method 1: Direct context field
    if "context" in step5_output:
        print("✅ Found direct 'context' field:")
        context = step5_output["context"]
        for key, value in context.items():
            print(f"   {key}: {value}")
    else:
        print("❌ No direct 'context' field found")
    
    # Method 2: Qloo parameters location
    activities = step5_output.get("intelligent_date_plan", {}).get("activities", [])
    if activities:
        for i, activity in enumerate(activities):
            qloo_params = activity.get("qloo_parameters", {})
            if qloo_params:
                location_query = qloo_params.get("filter.location.query")
                if location_query:
                    print(f"✅ Found location in activity {i+1} Qloo params: {location_query}")
                    break
    else:
        print("❌ No activities with Qloo parameters found")
    
    # Method 3: Processing metadata
    metadata = step5_output.get("processing_metadata", {})
    if metadata:
        print("📊 Processing metadata available:")
        relevant_fields = ["timestamp", "context_factors", "intelligence_level", "step_5_method"]
        for field in relevant_fields:
            if field in metadata:
                print(f"   {field}: {metadata[field]}")
    
    # Method 4: Date plan details
    date_plan = step5_output.get("intelligent_date_plan", {})
    if date_plan:
        print("📅 Date plan details:")
        print(f"   theme: {date_plan.get('theme', 'Not found')}")
        print(f"   total_duration: {date_plan.get('total_duration', 'Not found')}")
    
    print("\n🔧 CONTEXT EXTRACTION ASSESSMENT:")
    
    # Simulate what Step 6 would extract
    location = "unknown"
    activities = step5_output.get("intelligent_date_plan", {}).get("activities", [])
    if activities and activities[0].get("qloo_parameters"):
        location_query = activities[0]["qloo_parameters"].get("filter.location.query", "")
        if location_query:
            location = location_query.split(",")[0].strip()
    
    duration = step5_output.get("intelligent_date_plan", {}).get("total_duration", "unknown")
    theme = step5_output.get("intelligent_date_plan", {}).get("theme", "unknown") 
    
    print(f"   Extractable location: {location}")
    print(f"   Extractable duration: {duration}")
    print(f"   Extractable theme: {theme}")
    print(f"   Missing: time_of_day, season, date_type (need to be preserved)")
    
    return {
        "location": location,
        "duration": duration,
        "theme": theme,
        "context_preservation_needed": True
    }

def execute_step_6(step5_output):
    """Execute Step 6: Final Intelligence Optimizer with detailed output"""
    
    print(f"\n🎯 STEP 6: Final Intelligence Optimizer")
    print("-" * 50)
    
    try:
        from services.final_intelligence_optimizer import FinalIntelligenceOptimizer
        
        print(f"   🔄 Creating realistic date plan...")
        start_time = time.time()
        
        optimizer = FinalIntelligenceOptimizer()
        final_plan = optimizer.optimize_complete_date_plan(step5_output)
        
        processing_time = time.time() - start_time
        
        if not final_plan:
            print("   ❌ Step 6 failed - no response")
            return None
        
        # Show actual processing time (not fake timing)
        minutes = int(processing_time // 60)
        seconds = processing_time % 60
        if minutes > 0:
            print(f"   ✅ Final plan created ({minutes}m {seconds:.1f}s) - SLOW!")
        else:
            print(f"   ✅ Final plan created ({seconds:.1f}s)")
        
        # Analyze final plan results
        date_section = final_plan.get("date", {})
        reasoning_section = final_plan.get("reasoning", {})
        
        if date_section:
            print(f"   📍 Location: {date_section.get('location_city', 'Unknown')}")
            print(f"   🕐 Start time: {date_section.get('start_time', 'Unknown')}")
            print(f"   ⏱️  Duration: {date_section.get('total_duration', 'Unknown')}")
            print(f"   🎨 Theme: {date_section.get('theme', 'Unknown')}")
            activities = date_section.get('activities', [])
            print(f"   🎯 Activities: {len(activities)}")
            
            # Show first activity as example
            if activities:
                first_activity = activities[0]
                print(f"   📍 First activity: {first_activity.get('name', 'Unknown')}")
                print(f"   🕐 Time slot: {first_activity.get('time_slot', 'Unknown')}")
                print(f"   📍 Location: {first_activity.get('location_name', 'Unknown')}")
        
        if reasoning_section:
            compatibility = reasoning_section.get("compatibility_analysis", {})
            success_pred = reasoning_section.get("success_prediction", {})
            print(f"   💝 Compatibility: {compatibility.get('score', 0):.2f}")
            print(f"   🎯 Success probability: {success_pred.get('overall_probability', 0):.2f}")
        
        # SHOW THE ACTUAL JSON OUTPUT - ALWAYS
        print(f"\n📋 STEP 6 COMPLETE JSON OUTPUT:")
        print("=" * 60)
        
        try:
            final_json = json.dumps(final_plan, indent=2)
            print(f"📏 JSON Length: {len(final_json)} characters")
            
            # Always show at least the first part of the JSON
            if len(final_json) > 3000:
                print("📄 FIRST 3000 CHARACTERS:")
                print(final_json[:3000])
                print(f"\n... [CONTINUING - Total length: {len(final_json)} characters] ...")
                
                # Show key sections separately
                date_section_json = json.dumps(date_section, indent=2)
                print(f"\n📅 DATE SECTION ({len(date_section_json)} chars):")
                if len(date_section_json) > 1500:
                    print(date_section_json[:1500] + "\n... [DATE SECTION TRUNCATED] ...")
                else:
                    print(date_section_json)
                
                reasoning_section_json = json.dumps(reasoning_section, indent=2)
                print(f"\n🧠 REASONING SECTION ({len(reasoning_section_json)} chars):")
                if len(reasoning_section_json) > 1500:
                    print(reasoning_section_json[:1500] + "\n... [REASONING SECTION TRUNCATED] ...")
                else:
                    print(reasoning_section_json)
            else:
                print("📄 COMPLETE JSON OUTPUT:")
                print(final_json)
                
        except Exception as json_error:
            print(f"❌ Error displaying JSON: {json_error}")
            print(f"📊 Plan structure: {list(final_plan.keys()) if isinstance(final_plan, dict) else type(final_plan)}")
        
        print("=" * 60)
        
        return final_plan
        
    except Exception as e:
        print(f"   ❌ Step 6 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_complete_results(final_result, step5_result):
    """Analyze complete 6-step pipeline results"""
    
    print(f"\n🎉 COMPLETE 6-STEP PIPELINE ANALYSIS")
    print("=" * 70)
    
    if not final_result:
        print("❌ Cannot analyze - Step 6 failed")
        return
    
    # Compare Step 5 vs Step 6 context handling
    print(f"\n📊 CONTEXT PRESERVATION ANALYSIS:")
    print("-" * 40)
    
    # Step 5 context
    step5_activities = step5_result.get("intelligent_date_plan", {}).get("activities", [])
    step5_location = "unknown"
    if step5_activities and step5_activities[0].get("qloo_parameters"):
        location_query = step5_activities[0]["qloo_parameters"].get("filter.location.query", "")
        if location_query:
            step5_location = location_query.split(",")[0].strip()
    
    # Step 6 context
    step6_date = final_result.get("date", {})
    step6_location = step6_date.get("location_city", "unknown")
    
    print(f"Step 5 location: {step5_location}")
    print(f"Step 6 location: {step6_location}")
    print(f"Context preserved: {'✅' if step5_location.lower() == step6_location.lower() else '❌'}")
    
    # Pipeline completeness
    print(f"\n🏁 PIPELINE COMPLETENESS:")
    print("-" * 40)
    
    metadata = final_result.get("processing_metadata", {})
    date_section = final_result.get("date", {})
    reasoning_section = final_result.get("reasoning", {})
    
    completeness_checks = [
        ("Step 6 completed", metadata.get("step_6_completed", False)),
        ("Pipeline fully complete", metadata.get("pipeline_fully_complete", False)),
        ("Demo ready", metadata.get("demo_ready", False)),
        ("Date section present", bool(date_section)),
        ("Reasoning section present", bool(reasoning_section)),
        ("Activities with timing", bool(date_section.get("activities"))),
        ("Realistic locations", step6_location != "unknown"),
        ("Success prediction", bool(reasoning_section.get("success_prediction")))
    ]
    
    completed_checks = sum(1 for _, status in completeness_checks if status)
    total_checks = len(completeness_checks)
    
    for check_name, status in completeness_checks:
        print(f"   {'✅' if status else '❌'} {check_name}")
    
    print(f"\n📈 PIPELINE SCORE: {completed_checks}/{total_checks} ({completed_checks/total_checks*100:.0f}%)")
    
    # Demo readiness assessment
    if completed_checks >= total_checks * 0.8:
        print(f"🚀 DEMO READY: Excellent pipeline performance!")
    elif completed_checks >= total_checks * 0.6:
        print(f"⚠️  MOSTLY READY: Minor issues to address")
    else:
        print(f"🔧 NEEDS WORK: Major issues require fixing")
    
    return completed_checks >= total_checks * 0.8

def main():
    """Run complete Steps 1-6 pipeline test with context debugging"""
    
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
    
    print(f"\n🚀 STARTING COMPLETE 6-STEP PIPELINE TEST")
    total_start_time = time.time()
    
    # Setup test profiles with explicit context
    profile_a, profile_b = test_complete_pipeline_with_context()
    
    # Execute Steps 1-2 for both profiles
    enriched_profile_a = execute_steps_1_2(profile_a, "Emma (Fashion Designer)")
    enriched_profile_b = execute_steps_1_2(profile_b, "Liam (Photographer)")
    
    if not enriched_profile_a or not enriched_profile_b:
        print("\n❌ Pipeline failed at Steps 1-2")
        return
    
    # Execute Steps 3-4: Date Intelligence
    date_plan = execute_steps_3_4(enriched_profile_a, enriched_profile_b, profile_a["context"])
    
    if not date_plan:
        print("\n❌ Pipeline failed at Steps 3-4")
        return
    
    # Execute Step 5: Venue Discovery
    step5_result = execute_step_5(date_plan)
    
    if not step5_result:
        print("\n❌ Pipeline failed at Step 5")
        return
    
    # Debug Step 5 context availability
    context_info = debug_step5_context(step5_result)
    
    # Execute Step 6: Final Intelligence
    final_result = execute_step_6(step5_result)
    
    total_time = time.time() - total_start_time
    
    print(f"\n⏱️  TOTAL PIPELINE TIME: {total_time:.1f} seconds")
    
    # Analyze complete results
    is_demo_ready = analyze_complete_results(final_result, step5_result)
    
    print(f"\n🎯 FINAL ASSESSMENT:")
    if is_demo_ready and final_result:
        print(f"🚀 COMPLETE SUCCESS: 6-step pipeline fully operational!")
        print(f"   Perfect foundation for hackathon demo")
        print(f"   All cultural intelligence components working")
        print(f"   Context preservation and realistic planning achieved")
    else:
        print(f"🔧 PARTIAL SUCCESS: Pipeline works but needs refinement")
        print(f"   Core functionality operational")
        print(f"   Context preservation or Step 6 needs debugging")
    
    print(f"\n📋 NEXT STEPS:")
    if context_info.get("context_preservation_needed"):
        print(f"1. Fix context preservation from Steps 1-5 → Step 6")
    print(f"2. Create main.py endpoint for complete pipeline")
    print(f"3. Deploy to Heroku for frontend integration")
    print(f"4. Final testing and demo preparation")

if __name__ == "__main__":
    main()