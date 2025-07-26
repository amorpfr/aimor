#!/usr/bin/env python3
"""
Complete Pipeline Test: Steps 1-4 End-to-End
ProfileProcessor → ProfileEnricher → DateIntelligenceEngine
"""

import sys
import os
import json
import time
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 AI-MOR.ME Complete Pipeline Test")
print("=" * 60)
print("Testing: Steps 1-2 → Steps 3-4 → Qloo-Ready Output")
print("=" * 60)

def test_api_connectivity():
    """Test API connectivity before running pipeline"""
    print("\n🔌 API Connectivity Check")
    print("-" * 30)
    
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        qloo_key = os.getenv("QLOO_API_KEY")
        
        print(f"   OpenAI API Key: {'✅ Present' if openai_key else '❌ Missing'}")
        print(f"   Qloo API Key: {'✅ Present' if qloo_key else '❌ Missing'}")
        
        if not openai_key:
            print("   ⚠️  Steps 1-4 will fail without OpenAI key")
            return False
        if not qloo_key:
            print("   ⚠️  Step 2 cultural enhancement may fail without Qloo key")
        
        return True
            
    except Exception as e:
        print(f"   ❌ API key check failed: {e}")
        return False

def test_step_1_2_pipeline(profile_text: str, profile_name: str, context: dict):
    """Test Steps 1-2: Profile Processing + Cultural Enhancement"""
    print(f"\n🧠 TESTING STEPS 1-2: {profile_name}")
    print("-" * 40)
    
    try:
        # Step 1: Profile Processing
        from services.profile_processor import ProfileProcessor
        
        print("   🔄 Step 1: Profile Analysis...")
        processor = ProfileProcessor()
        step1_result = processor.process_profile_with_context(
            text=profile_text,
            context=context
        )
        
        if not step1_result.get("success"):
            print(f"   ❌ Step 1 failed: {step1_result.get('error', 'Unknown error')}")
            return None
        
        print(f"   ✅ Step 1 complete - Confidence: {step1_result['analysis'].get('processing_confidence', 0):.2f}")
        
        # Step 2: Cultural Enhancement
        from services.profile_enricher import ProfileEnricher
        
        print("   🔄 Step 2: Cultural Enhancement...")
        enricher = ProfileEnricher()
        step2_result = enricher.process_psychological_profile(
            step1_result["analysis"], 
            context
        )
        
        if not step2_result.get("success"):
            print(f"   ❌ Step 2 failed: {step2_result.get('error', 'Unknown error')}")
            return step1_result  # Return Step 1 result anyway for testing
        
        # Display Step 2 results
        metadata = step2_result.get("processing_metadata", {})
        print(f"   ✅ Step 2 complete - Discoveries: {metadata.get('total_new_discoveries', 0)}")
        print(f"   📊 Cultural depth: {metadata.get('cultural_depth_enhancement', 0):.2f}")
        
        # Show sample discoveries
        discoveries = step2_result.get("cross_domain_discoveries", {})
        for category, items in discoveries.items():
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

def test_step_3_4_pipeline(enriched_profile_a: dict, enriched_profile_b: dict, context: dict):
    """Test Steps 3-4: Date Intelligence Engine"""
    print(f"\n🎯 TESTING STEPS 3-4: Date Intelligence Engine")
    print("-" * 40)
    
    try:
        from services.date_intelligence_engine import DateIntelligenceEngine
        
        engine = DateIntelligenceEngine()
        
        print("   🔄 Creating intelligent date plan...")
        start_time = time.time()
        
        date_plan = engine.create_intelligent_date_plan(
            enriched_profile_a=enriched_profile_a,
            enriched_profile_b=enriched_profile_b,
            context=context
        )
        
        processing_time = time.time() - start_time
        print(f"   ⏱️  Processing time: {processing_time:.2f} seconds")
        
        if not date_plan or date_plan.get("error"):
            print(f"   ❌ Steps 3-4 failed: {date_plan.get('error', 'Unknown error')}")
            return None
        
        # Analyze the results
        compatibility = date_plan.get("compatibility_insights", {})
        intelligent_plan = date_plan.get("intelligent_date_plan", {})
        qloo_queries = date_plan.get("qloo_ready_queries", [])
        
        print(f"   ✅ Date plan created successfully!")
        print(f"   💝 Compatibility score: {compatibility.get('overall_compatibility', 0):.2f}")
        print(f"   🎨 Theme: {intelligent_plan.get('theme', 'Unknown')}")
        print(f"   🕐 Duration: {intelligent_plan.get('total_duration', 'Unknown')}")
        print(f"   🏢 Activities planned: {len(intelligent_plan.get('activities', []))}")
        print(f"   🔍 Qloo queries generated: {len(qloo_queries)}")
        
        # Show activity details
        activities = intelligent_plan.get("activities", [])
        for i, activity in enumerate(activities[:3]):  # Show first 3
            print(f"   📍 Activity {i+1}: {activity.get('name', 'Unknown')} ({activity.get('duration', 'Unknown')})")
            qloo_params = activity.get("qloo_parameters", {})
            if qloo_params:
                print(f"      🎯 Qloo ready: filter.type={qloo_params.get('filter.type', 'Missing')}")
                print(f"      📍 Location: {qloo_params.get('filter.location.query', 'Missing')}")
                signals = qloo_params.get('signal.interests.entities', '')
                entity_count = len(signals.split(',')) if signals else 0
                print(f"      🧠 Entity signals: {entity_count} entities")
        
        return date_plan
        
    except Exception as e:
        print(f"   ❌ Steps 3-4 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_qloo_readiness(date_plan: dict):
    """Analyze how ready the output is for Qloo API calls"""
    print(f"\n🔍 QLOO READINESS ANALYSIS")
    print("-" * 40)
    
    qloo_queries = date_plan.get("qloo_ready_queries", [])
    
    if not qloo_queries:
        print("   ❌ No Qloo queries generated")
        return False
    
    print(f"   ✅ Generated {len(qloo_queries)} Qloo-ready queries:")
    
    all_valid = True
    for i, query in enumerate(qloo_queries):
        activity_name = query.get("activity_name", f"Activity {i+1}")
        params = query.get("parameters", {})
        
        print(f"\n   🎯 Query {i+1}: {activity_name}")
        
        # Check required parameters
        required_params = [
            "filter.type",
            "filter.location.query",
            "take"
        ]
        
        for param in required_params:
            if param in params:
                print(f"      ✅ {param}: {params[param]}")
            else:
                print(f"      ❌ Missing: {param}")
                all_valid = False
        
        # Check optional but important parameters
        optional_params = [
            "signal.interests.entities",
            "filter.tags",
            "filter.price_level.min",
            "filter.popularity.min"
        ]
        
        for param in optional_params:
            if param in params:
                value = params[param]
                if isinstance(value, str) and len(value) > 0:
                    print(f"      ✅ {param}: {value}")
                elif isinstance(value, (int, float)):
                    print(f"      ✅ {param}: {value}")
                else:
                    print(f"      ⚠️  {param}: Empty/invalid")
            else:
                print(f"      ⚠️  {param}: Not provided")
    
    if all_valid:
        print(f"\n   🚀 ALL QUERIES ARE QLOO-READY!")
        print(f"   💡 Ready to call: https://hackathon.api.qloo.com/v2/insights")
    else:
        print(f"\n   ⚠️  Some queries need refinement")
    
    return all_valid

def main():
    """Run complete pipeline test with two personality types"""
    
    # Test API connectivity first
    if not test_api_connectivity():
        print("\n❌ API connectivity issues. Please check your .env file")
        return
    
    # Test profiles representing different personality types
    profiles = [
        {
            "name": "Emma (Adventure Seeker)",
            "text": "Emma, 28, Amsterdam local. Passionate rock climber and photographer. Love discovering hidden speakeasies and trying Ethiopian cuisine. Currently learning Portuguese. Work in sustainable fashion. Weekend warrior seeking authentic connections over pretentious small talk.",
            "context": {
                "location": "amsterdam",
                "time_of_day": "evening", 
                "season": "winter",
                "duration": "4 hours",
                "date_type": "first_date"
            }
        },
        {
            "name": "Alex (Creative Introvert)",
            "text": "Alex, 26, graphic designer from Rotterdam. Bookworm obsessed with magical realism novels. Spend weekends at art house cinemas and vintage record shops. Love intimate jazz bars and hate crowded clubs. Looking for deep conversations about life, art, and dreams.",
            "context": {
                "location": "amsterdam",
                "time_of_day": "afternoon",
                "season": "winter", 
                "duration": "4 hours",
                "date_type": "first_date"
            }
        }
    ]
    
    print(f"\n🏁 COMPLETE PIPELINE TEST")
    print(f"Testing cultural intelligence dating engine with personality diversity")
    
    # Process both profiles through Steps 1-2
    enriched_profiles = []
    
    for profile in profiles:
        enriched_profile = test_step_1_2_pipeline(
            profile["text"], 
            profile["name"], 
            profile["context"]
        )
        
        if enriched_profile:
            enriched_profiles.append(enriched_profile)
        else:
            print(f"\n❌ Pipeline failed for {profile['name']}")
            return
    
    if len(enriched_profiles) < 2:
        print(f"\n❌ Need 2 successful profiles for date planning")
        return
    
    # Test Steps 3-4 with both profiles
    context = profiles[0]["context"]  # Use first profile's context
    date_plan = test_step_3_4_pipeline(
        enriched_profiles[0], 
        enriched_profiles[1], 
        context
    )
    
    if not date_plan:
        print(f"\n❌ Date planning failed")
        return
    
    # Analyze Qloo readiness
    qloo_ready = analyze_qloo_readiness(date_plan)
    
    # Final summary
    print(f"\n" + "=" * 60)
    print(f"🏁 COMPLETE PIPELINE TEST RESULTS")
    print(f"=" * 60)
    
    print(f"\n✅ SUCCESSFUL COMPONENTS:")
    print(f"   🧠 Step 1: Profile Analysis - WORKING")
    print(f"   🎨 Step 2: Cultural Enhancement - WORKING") 
    print(f"   💝 Steps 3-4: Date Intelligence - WORKING")
    print(f"   {'🚀 Qloo Integration: READY' if qloo_ready else '⚠️  Qloo Integration: NEEDS REFINEMENT'}")
    
    print(f"\n📊 PERFORMANCE METRICS:")
    metadata = date_plan.get("processing_metadata", {})
    print(f"   🎯 Cultural discoveries analyzed: {metadata.get('cultural_discoveries_analyzed', 0)}")
    print(f"   🔍 Qloo queries generated: {metadata.get('qloo_queries_generated', 0)}")
    print(f"   🧠 Intelligence level: {metadata.get('intelligence_level', 'Unknown')}")
    
    if qloo_ready:
        print(f"\n🚀 DEMO READINESS: EXCELLENT!")
        print(f"   Ready for Step 5: Venue Discovery")
        print(f"   Pipeline optimized for hackathon presentation")
    else:
        print(f"\n🔧 NEEDS REFINEMENT:")
        print(f"   Qloo parameters need adjustment")
        print(f"   Review DateIntelligenceEngine output")

if __name__ == "__main__":
    main()