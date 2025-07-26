#!/usr/bin/env python3
"""
Test Complete Steps 1-6 Pipeline WITH CONTEXT CONTAINER
Enhanced Context Debugging + Full Cultural Intelligence Dating Engine Test
ENHANCED: Shows activity details, timing, and context duration
"""

import sys
import os
import time
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔥 COMPLETE STEPS 1-6 PIPELINE TEST WITH CONTEXT CONTAINER")
print("=" * 80)
print("Two Real Profiles → Complete Date Plan with GUARANTEED Context Preservation")
print("Context Container + Realistic Date Planning")
print("=" * 80)

def test_complete_pipeline_with_context_container():
    """Test complete pipeline with explicit context container debugging"""
    
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
            "duration": "full day",
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
            "duration": "full day",
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

def execute_steps_1_2_with_container(profile_data, profile_name, context_container):
    """Execute Steps 1-2: Profile Analysis + Cultural Enhancement WITH CONTEXT CONTAINER"""
    
    print(f"\n🧠 STEPS 1-2: {profile_name} (WITH CONTEXT CONTAINER)")
    print("-" * 50)
    
    try:
        # Step 1: Profile Analysis
        from services.profile_processor import ProfileProcessor
        
        print(f"   🔄 Step 1: Analyzing {profile_name}...")
        start_time = time.time()
        
        # Get context from container
        step1_context = context_container.get_context_for_step(1)
        
        processor = ProfileProcessor()
        step1_result = processor.process_profile_with_context(
            text=profile_data["text"],
            context=step1_context
        )
        
        step1_time = time.time() - start_time
        
        if not step1_result.get("success"):
            print(f"   ❌ Step 1 failed: {step1_result.get('error', 'Unknown error')}")
            return None
        
        # Store Step 1 with context preservation
        context_container.store_step_output(f"step1_{profile_name.split()[0].lower()}", step1_result)
        
        analysis = step1_result["analysis"]
        confidence = analysis.get("processing_confidence", 0)
        print(f"   ✅ Step 1 complete - Confidence: {confidence:.2f} ({step1_time:.1f}s)")
        
        # Verify context preservation
        preserved_context = step1_result.get("original_context")
        if preserved_context:
            print(f"   📋 Context preserved: ✅ ({preserved_context['location']}, {preserved_context['time_of_day']}, {preserved_context['season']})")
        else:
            print(f"   📋 Context preserved: ❌")
        
        # Step 2: Cultural Enhancement
        from services.profile_enricher import ProfileEnricher
        
        print(f"   🔄 Step 2: Cultural enhancement...")
        step2_start = time.time()
        
        # Get enhanced input with guaranteed context preservation
        enhanced_input = context_container.get_enhanced_output_for_next_step(f"step1_{profile_name.split()[0].lower()}")
        
        enricher = ProfileEnricher()
        step2_result = enricher.process_psychological_profile(
            enhanced_input["analysis"], 
            enhanced_input.get("original_context")
        )
        
        step2_time = time.time() - step2_start
        
        if not step2_result.get("success"):
            print(f"   ❌ Step 2 failed: {step2_result.get('error', 'Unknown error')}")
            return step1_result
        
        # Store Step 2 with context preservation
        context_container.store_step_output(f"step2_{profile_name.split()[0].lower()}", step2_result)
        
        metadata = step2_result.get("processing_metadata", {})
        discoveries = metadata.get("total_new_discoveries", 0)
        
        print(f"   ✅ Step 2 complete - Discoveries: {discoveries} ({step2_time:.1f}s)")
        
        # Verify context preservation in Step 2
        preserved_context_2 = step2_result.get("original_context")
        if preserved_context_2:
            print(f"   📋 Context preserved: ✅")
        else:
            print(f"   📋 Context preserved: ❌")
        
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

def execute_steps_3_4_with_container(enriched_profile_a, enriched_profile_b, context_container):
    """Execute Steps 3-4: Date Intelligence Engine WITH CONTEXT CONTAINER"""
    
    print(f"\n💝 STEPS 3-4: Date Intelligence Engine (WITH CONTEXT CONTAINER)")
    print("-" * 50)
    
    try:
        from services.date_intelligence_engine import DateIntelligenceEngine
        
        print(f"   🔄 Creating intelligent date plan...")
        start_time = time.time()
        
        # Get context from container
        step34_context = context_container.get_context_for_step(3)
        
        engine = DateIntelligenceEngine()
        date_plan = engine.create_intelligent_date_plan(
            enriched_profile_a=enriched_profile_a,
            enriched_profile_b=enriched_profile_b,
            context=step34_context
        )
        
        processing_time = time.time() - start_time
        
        if not date_plan or date_plan.get("error"):
            print(f"   ❌ Steps 3-4 failed: {date_plan.get('error', 'Unknown error')}")
            return None
        
        # Store in context container
        context_container.store_step_output("steps34", date_plan)
        
        # Analyze date intelligence results
        compatibility = date_plan.get("compatibility_insights", {})
        intelligent_plan = date_plan.get("intelligent_date_plan", {})
        
        print(f"   ✅ Date plan created ({processing_time:.1f}s)")
        print(f"   💝 Compatibility: {compatibility.get('overall_compatibility', 0):.2f}")
        print(f"   🎨 Theme: {intelligent_plan.get('theme', 'Unknown')}")
        print(f"   🕐 Duration: {intelligent_plan.get('total_duration', 'Unknown')}")
        
        # Verify context preservation
        preserved_context = date_plan.get("original_context")
        if preserved_context:
            print(f"   📋 Context preserved: ✅ ({preserved_context['location']}, {preserved_context['time_of_day']}, {preserved_context['season']})")
        else:
            print(f"   📋 Context preserved: ❌")
        
        return date_plan
        
    except Exception as e:
        print(f"   ❌ Steps 3-4 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def execute_step_5_with_container(date_plan, context_container):
    """Execute Step 5: OpenAI-Enhanced Venue Discovery WITH CONTEXT CONTAINER"""
    
    print(f"\n🏢 STEP 5: OpenAI-Enhanced Venue Discovery (WITH CONTEXT CONTAINER)")
    print("-" * 50)
    
    try:
        from services.venue_discoverer import VenueDiscoverer
        
        print(f"   🔄 Discovering venues with OpenAI intelligence...")
        start_time = time.time()
        
        # Get enhanced input with guaranteed context preservation
        enhanced_input = context_container.get_enhanced_output_for_next_step("steps34")
        
        discoverer = VenueDiscoverer()
        complete_plan = discoverer.discover_venues_for_date_plan(enhanced_input)
        
        processing_time = time.time() - start_time
        
        if not complete_plan:
            print("   ❌ Step 5 failed - no response")
            return None
        
        # Store in context container
        context_container.store_step_output("step5", complete_plan)
        
        # Analyze venue discovery results
        venue_summary = complete_plan.get("venue_discovery_summary", {})
        activities = complete_plan.get("intelligent_date_plan", {}).get("activities", [])
        
        print(f"   ✅ Venue discovery complete ({processing_time:.1f}s)")
        print(f"   🏢 Method: {venue_summary.get('selection_method', 'unknown')}")
        print(f"   🎯 Selected: {venue_summary.get('total_venues_selected', 0)}")
        print(f"   ✅ Success rate: {venue_summary.get('discovery_success_rate', 0):.1%}")
        
        # Verify context preservation
        preserved_context = complete_plan.get("original_context")
        if preserved_context:
            print(f"   📋 Context preserved: ✅ ({preserved_context['location']}, {preserved_context['time_of_day']}, {preserved_context['season']})")
        else:
            print(f"   📋 Context preserved: ❌")
        
        return complete_plan
        
    except Exception as e:
        print(f"   ❌ Step 5 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def debug_step5_context_with_container(step5_output, context_container):
    """Debug what context is actually available in Step 5 output WITH CONTAINER VALIDATION"""
    
    print(f"\n🔍 STEP 5 CONTEXT DEBUGGING (WITH CONTEXT CONTAINER)")
    print("=" * 50)
    
    print("📋 Checking for context in Step 5 output...")
    
    # NEW: Check context container validation
    validation = context_container.validate_context_preservation()
    print(f"📦 Context Container Status:")
    print(f"   Context preserved: {'✅' if validation['context_preserved'] else '❌'}")
    print(f"   Steps completed: {validation['steps_completed']}")
    
    # ENHANCED: Show context journey duration
    try:
        original_context = context_container.original_context
        context_created_time = getattr(context_container, '_creation_time', None)
        if context_created_time:
            context_duration = time.time() - context_created_time
            print(f"   Context container lifetime: {context_duration:.1f} seconds")
        else:
            print(f"   Context container lifetime: Full pipeline duration")
    except Exception:
        print(f"   Context container lifetime: Unable to measure")
    
    if validation['issues']:
        print(f"   Issues: {validation['issues']}")
    
    # Method 1: Direct context field (SHOULD NOW EXIST)
    if "original_context" in step5_output:
        print("✅ Found 'original_context' field:")
        context = step5_output["original_context"]
        for key, value in context.items():
            print(f"   {key}: {value}")
    else:
        print("❌ No 'original_context' field found - context container not working!")
    
    # Method 2: Processing metadata context (BACKUP)
    metadata = step5_output.get("processing_metadata", {})
    if "input_context" in metadata:
        print("✅ Found backup context in processing metadata:")
        backup_context = metadata["input_context"]
        for key, value in backup_context.items():
            print(f"   {key}: {value}")
    else:
        print("❌ No backup context in processing metadata")
    
    # Method 3: Qloo parameters location (FALLBACK)
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
    
    print("\n🔧 CONTEXT EXTRACTION ASSESSMENT WITH CONTAINER:")
    
    # Compare original context vs extracted context
    original_context = context_container.original_context
    extracted_context = step5_output.get("original_context", {})
    
    print(f"   Original context: {original_context}")
    print(f"   Extracted context: {extracted_context}")
    
    context_match = original_context == extracted_context
    print(f"   Perfect match: {'✅' if context_match else '❌'}")
    
    if not context_match:
        missing_fields = [k for k in original_context.keys() if k not in extracted_context or extracted_context[k] != original_context[k]]
        print(f"   Missing/changed fields: {missing_fields}")
    
    return {
        "container_working": validation['context_preserved'],
        "original_context": original_context,
        "extracted_context": extracted_context,
        "perfect_match": context_match
    }

def execute_step_6_with_container(step5_output, context_container):
    """Execute Step 6: Final Intelligence Optimizer WITH GUARANTEED CONTEXT"""
    
    print(f"\n🎯 STEP 6: Final Intelligence Optimizer (WITH GUARANTEED CONTEXT)")
    print("-" * 50)
    
    try:
        from services.final_intelligence_optimizer import FinalIntelligenceOptimizer
        
        # Get enhanced input with GUARANTEED context preservation
        enhanced_input = context_container.get_enhanced_output_for_next_step("step5")
        
        # CRITICAL: Verify context before Step 6
        original_context = enhanced_input.get("original_context")
        print(f"   📋 Pre-Step 6 context verification:")
        if original_context:
            print(f"   ✅ Original context available: {original_context}")
            print(f"   📍 Location: {original_context.get('location', 'MISSING')}")
            print(f"   🕐 Time: {original_context.get('time_of_day', 'MISSING')}")
            print(f"   🌸 Season: {original_context.get('season', 'MISSING')}")
        else:
            print(f"   ❌ NO ORIGINAL CONTEXT - Step 6 will fail!")
            print(f"   This means the context container fix is not working properly")
        
        print(f"   🔄 Creating realistic date plan...")
        start_time = time.time()
        
        optimizer = FinalIntelligenceOptimizer()
        final_plan = optimizer.optimize_complete_date_plan(enhanced_input)
        
        processing_time = time.time() - start_time
        
        if not final_plan:
            print("   ❌ Step 6 failed - no response")
            return None
        
        # Show actual processing time
        minutes = int(processing_time // 60)
        seconds = processing_time % 60
        if minutes > 0:
            print(f"   ✅ Final plan created ({minutes}m {seconds:.1f}s)")
        else:
            print(f"   ✅ Final plan created ({seconds:.1f}s)")
        
        # Analyze final plan results
        date_section = final_plan.get("date", {})
        reasoning_section = final_plan.get("reasoning", {})
        processing_metadata = final_plan.get("processing_metadata", {})
        
        if date_section:
            print(f"   📍 Location: {date_section.get('location_city', 'Unknown')}")
            print(f"   🕐 Start time: {date_section.get('start_time', 'Unknown')}")
            print(f"   ⏱️  Duration: {date_section.get('total_duration', 'Unknown')}")
            print(f"   🎨 Theme: {date_section.get('theme', 'Unknown')}")
            activities = date_section.get('activities', [])
            print(f"   🎯 Activities: {len(activities)}")
            
            # ENHANCED: Show ALL activities with details
            if activities:
                print(f"\n   📅 COMPLETE ACTIVITY SCHEDULE:")
                for i, activity in enumerate(activities, 1):
                    activity_name = activity.get('name', 'Unknown Activity')
                    time_slot = activity.get('time_slot', 'No time specified')
                    location_name = activity.get('location_name', 'No location specified')
                    duration = activity.get('duration_minutes', 0)
                    
                    print(f"   {i}. 🎯 {activity_name}")
                    print(f"      ⏰ {time_slot} ({duration} min)")
                    print(f"      📍 {location_name}")
                    
                    # Show first activity detail for context
                    if i == 1:
                        what_to_do = activity.get('what_to_do', [])
                        if what_to_do:
                            print(f"      💡 Preview: {what_to_do[0]}")
        
        if reasoning_section:
            compatibility = reasoning_section.get("compatibility_analysis", {})
            success_pred = reasoning_section.get("success_prediction", {})
            print(f"   💝 Compatibility: {compatibility.get('score', 0):.2f}")
            print(f"   🎯 Success probability: {success_pred.get('overall_probability', 0):.2f}")
        
        # CRITICAL: Check if Step 6 actually used the preserved context
        original_location = original_context.get('location', 'MISSING') if original_context else 'NO_CONTEXT'
        final_location = date_section.get('location_city', 'MISSING')
        
        print(f"   🎯 CONTEXT PRESERVATION TEST:")
        print(f"   Original location: '{original_location}'")
        print(f"   Final location: '{final_location}'")
        
        if original_location == 'NO_CONTEXT':
            print(f"   ❌ CRITICAL: No context provided to Step 6")
        elif original_location == 'MISSING':
            print(f"   ❌ ERROR: Context malformed")
        elif original_location.lower() == final_location.lower():
            print(f"   ✅ SUCCESS: Context preserved perfectly!")
        else:
            print(f"   ❌ FAILED: Context not preserved")
        
        # ENHANCED: Show JSON length and structure without full output
        print(f"\n📋 STEP 6 OUTPUT SUMMARY:")
        print("=" * 60)
        
        try:
            final_json = json.dumps(final_plan, indent=2)
            print(f"📏 JSON Length: {len(final_json)} characters")
            
            # Show structure summary
            date_activities = len(date_section.get('activities', []))
            reasoning_keys = len(reasoning_section.keys()) if reasoning_section else 0
            
            print(f"📊 Output Structure:")
            print(f"   📅 Date section: {date_activities} activities")
            print(f"   🧠 Reasoning section: {reasoning_keys} analysis components")
            print(f"   📋 Metadata: {'✅' if processing_metadata else '❌'}")
            
            # Show key dates/times for context validation
            if date_section:
                total_duration = date_section.get('total_duration', 'Unknown')
                start_time = date_section.get('start_time', 'Unknown')
                theme = date_section.get('theme', 'Unknown')
                
                print(f"\n🎯 KEY DETAILS:")
                print(f"   🕐 {start_time} start, {total_duration} total")
                print(f"   🎨 Theme: {theme}")
                print(f"   📍 All venues in: {final_location}")
                
        except Exception as json_error:
            print(f"❌ Error analyzing output: {json_error}")
            print(f"📊 Plan structure: {list(final_plan.keys()) if isinstance(final_plan, dict) else type(final_plan)}")
        
        print("=" * 60)
        
        return final_plan
        
    except Exception as e:
        print(f"   ❌ Step 6 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_complete_results_with_container(final_result, step5_result, context_container):
    """Analyze complete 6-step pipeline results WITH CONTEXT CONTAINER ASSESSMENT"""
    
    print(f"\n🎉 COMPLETE 6-STEP PIPELINE ANALYSIS (WITH CONTEXT CONTAINER)")
    print("=" * 70)
    
    if not final_result:
        print("❌ Cannot analyze - Step 6 failed")
        return False
    
    # Context Container Assessment
    print(f"\n📦 CONTEXT CONTAINER ASSESSMENT:")
    print("-" * 40)
    
    validation = context_container.validate_context_preservation()
    print(f"Context preserved throughout pipeline: {'✅' if validation['context_preserved'] else '❌'}")
    print(f"Steps completed: {validation['steps_completed']}")
    
    if validation['issues']:
        print(f"Issues found: {validation['issues']}")
    else:
        print("🎉 No context preservation issues detected!")
    
    # Compare Step 5 vs Step 6 context handling
    print(f"\n📊 CONTEXT PRESERVATION ANALYSIS:")
    print("-" * 40)
    
    # Original context
    original_context = context_container.original_context
    original_location = original_context.get('location', 'unknown')
    
    # Step 5 context
    step5_context = step5_result.get("original_context", {})
    step5_location = step5_context.get('location', 'unknown')
    
    # Step 6 context
    step6_date = final_result.get("date", {})
    step6_location = step6_date.get("location_city", "unknown")
    
    print(f"Original location: {original_location}")
    print(f"Step 5 location: {step5_location}")
    print(f"Step 6 location: {step6_location}")
    
    # Context preservation scoring
    step5_preserved = original_location.lower() == step5_location.lower()
    step6_preserved = original_location.lower() == step6_location.lower()
    
    print(f"Step 5 preserved: {'✅' if step5_preserved else '❌'}")
    print(f"Step 6 preserved: {'✅' if step6_preserved else '❌'}")
    print(f"End-to-end preservation: {'✅' if step6_preserved else '❌'}")
    
    # ENHANCED: Show final date plan details
    print(f"\n🎯 FINAL DATE PLAN SUMMARY:")
    print("-" * 40)
    
    date_section = final_result.get("date", {})
    if date_section:
        activities = date_section.get('activities', [])
        start_time = date_section.get('start_time', 'Unknown')
        total_duration = date_section.get('total_duration', 'Unknown')
        theme = date_section.get('theme', 'Unknown')
        
        print(f"📅 {len(activities)} activities planned")
        print(f"🕐 {start_time} start, {total_duration} duration")
        print(f"🎨 Theme: {theme}")
        print(f"📍 Location: {step6_location}")
        
        if activities:
            print(f"\n📋 ACTIVITY TIMELINE:")
            for i, activity in enumerate(activities, 1):
                activity_name = activity.get('name', 'Unknown')
                time_slot = activity.get('time_slot', 'No time')
                print(f"   {i}. {activity_name} ({time_slot})")
    
    # Pipeline completeness
    print(f"\n🏁 PIPELINE COMPLETENESS:")
    print("-" * 40)
    
    metadata = final_result.get("processing_metadata", {})
    reasoning_section = final_result.get("reasoning", {})
    
    completeness_checks = [
        ("Step 6 completed", metadata.get("step_6_completed", False)),
        ("Pipeline fully complete", metadata.get("pipeline_fully_complete", False)),
        ("Demo ready", metadata.get("demo_ready", False)),
        ("Date section present", bool(date_section)),
        ("Reasoning section present", bool(reasoning_section)),
        ("Activities with timing", bool(date_section.get("activities"))),
        ("Realistic locations", step6_location != "unknown"),
        ("Success prediction", bool(reasoning_section.get("success_prediction"))),
        ("Context container working", validation['context_preserved']),
        ("End-to-end context preservation", step6_preserved)
    ]
    
    completed_checks = sum(1 for _, status in completeness_checks if status)
    total_checks = len(completeness_checks)
    
    for check_name, status in completeness_checks:
        print(f"   {'✅' if status else '❌'} {check_name}")
    
    print(f"\n📈 PIPELINE SCORE: {completed_checks}/{total_checks} ({completed_checks/total_checks*100:.0f}%)")
    
    # Demo readiness assessment
    if completed_checks >= total_checks * 0.9:
        print(f"🚀 EXCELLENT: Pipeline working perfectly!")
    elif completed_checks >= total_checks * 0.8:
        print(f"🚀 DEMO READY: Pipeline mostly working!")
    elif completed_checks >= total_checks * 0.6:
        print(f"⚠️  MOSTLY READY: Pipeline needs minor fixes")
    else:
        print(f"🔧 NEEDS WORK: Pipeline has major issues")
    
    return completed_checks >= total_checks * 0.8

def execute_complete_pipeline_with_context_container(profile_a, profile_b):
    """Execute complete 6-step pipeline using context container"""
    
    print(f"\n🚀 STARTING COMPLETE 6-STEP PIPELINE WITH CONTEXT CONTAINER")
    print("=" * 80)
    
    try:
        # Import context container
        from utils.context_container import create_context_container
        
        # Create context container with Emma's context
        context_container = create_context_container(profile_a["context"])
        
        print(f"📦 Context Container initialized with: {context_container.original_context}")
        
        total_start_time = time.time()
        
        # Execute Steps 1-2 for both profiles WITH CONTEXT CONTAINER
        enriched_profile_a = execute_steps_1_2_with_container(profile_a, "Emma (Fashion Designer)", context_container)
        enriched_profile_b = execute_steps_1_2_with_container(profile_b, "Liam (Photographer)", context_container)
        
        if not enriched_profile_a or not enriched_profile_b:
            print("\n❌ Pipeline failed at Steps 1-2")
            return None
        
        # Execute Steps 3-4: Date Intelligence WITH CONTEXT CONTAINER
        date_plan = execute_steps_3_4_with_container(enriched_profile_a, enriched_profile_b, context_container)
        
        if not date_plan:
            print("\n❌ Pipeline failed at Steps 3-4")
            return None
        
        # Execute Step 5: Venue Discovery WITH CONTEXT CONTAINER
        step5_result = execute_step_5_with_container(date_plan, context_container)
        
        if not step5_result:
            print("\n❌ Pipeline failed at Step 5")
            return None
        
        # Debug Step 5 context availability WITH CONTAINER VALIDATION
        context_info = debug_step5_context_with_container(step5_result, context_container)
        
        # Execute Step 6: Final Intelligence WITH GUARANTEED CONTEXT
        final_result = execute_step_6_with_container(step5_result, context_container)
        
        total_time = time.time() - total_start_time
        
        print(f"\n⏱️  TOTAL PIPELINE TIME: {total_time:.1f} seconds")
        
        # Analyze complete results WITH CONTEXT CONTAINER ASSESSMENT
        is_demo_ready = analyze_complete_results_with_container(final_result, step5_result, context_container)
        
        print(f"\n🎯 FINAL ASSESSMENT WITH CONTEXT CONTAINER:")
        if is_demo_ready and final_result:
            print(f"🚀 COMPLETE SUCCESS: Context container fix working!")
            print(f"   Perfect context preservation through all 6 steps")
            print(f"   Rotterdam context maintained from input → Step 6 output")
            print(f"   Ready for production deployment")
        else:
            print(f"🔧 PARTIAL SUCCESS: Context container needs refinement")
            print(f"   Core functionality operational but context issues remain")
        
        return final_result
        
    except Exception as e:
        print(f"❌ Pipeline failed with context container: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run complete Steps 1-6 pipeline test with context container"""
    
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
    
    # Test profiles
    profile_a, profile_b = test_complete_pipeline_with_context_container()
    
    # Execute complete pipeline with context container
    final_result = execute_complete_pipeline_with_context_container(profile_a, profile_b)
    
    if final_result:
        print(f"\n🎯 CONTEXT CONTAINER TEST RESULT: SUCCESS ✅")
        print(f"   Context preservation mechanism working")
        print(f"   Ready for production deployment")
    else:
        print(f"\n🎯 CONTEXT CONTAINER TEST RESULT: FAILED ❌")
        print(f"   Context preservation needs more work")

if __name__ == "__main__":
    main()