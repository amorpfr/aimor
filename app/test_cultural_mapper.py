#!/usr/bin/env python3
"""
Test Steps 1-2 Only: Profile Analysis + Cultural Enhancement
Updated to match the new Step 2 focused CulturalMapper
"""

print("🚀 Testing Steps 1-2: Profile Analysis + Cultural Enhancement")
print("=" * 60)

import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_step_1_profile_analysis():
    """Test Step 1: Existing Profile Analysis"""
    print("\n🧠 STEP 1: Profile Analysis (Existing System)")
    print("-" * 40)
    
    try:
        from services.profile_processor import ProfileProcessor
        
        # Sample profile
        sample_text = "Emma, 28, Amsterdam local. Passionate rock climber and photographer. Love discovering hidden speakeasies and trying Ethiopian cuisine."
        
        context = {
            "location": "amsterdam",
            "time_of_day": "evening", 
            "season": "winter",
            "duration": "4 hours",
            "date_type": "first_date"
        }
        
        processor = ProfileProcessor()
        result = processor.process_profile_with_context(
            text=sample_text,
            context=context
        )
        
        if result.get("success"):
            print("✅ Step 1 - Profile Analysis: SUCCESS")
            analysis = result.get("analysis", {})
            print(f"   Confidence: {analysis.get('processing_confidence', 0):.2f}")
            
            # Check for Qloo-ready entities
            qloo_entities = analysis.get("qloo_optimized_entities", {})
            explicit = qloo_entities.get("explicitly_mentioned", {})
            
            print(f"   Activities: {explicit.get('activities', [])}")
            print(f"   Food preferences: {explicit.get('food_preferences', [])}")
            print(f"   Locations: {explicit.get('locations', [])}")
            
            return result
        else:
            print(f"❌ Step 1 failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Step 1 error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_alternative_profile():
    """Test with a different personality profile"""
    print("\n🎨 ALTERNATIVE PROFILE TEST")
    print("-" * 40)
    
    try:
        from services.profile_processor import ProfileProcessor
        
        # Different personality type - creative introvert
        sample_text = "Alex, 26, graphic designer from Rotterdam. Bookworm obsessed with sci-fi novels and indie films. Spend weekends at art galleries and vinyl record shops. Love quiet coffee shops with character and hate crowded places."
        
        context = {
            "location": "amsterdam",
            "time_of_day": "afternoon", 
            "season": "spring",
            "duration": "3 hours",
            "date_type": "first_date"
        }
        
        processor = ProfileProcessor()
        result = processor.process_profile_with_context(
            text=sample_text,
            context=context
        )
        
        if result.get("success"):
            print("✅ Alternative Profile Analysis: SUCCESS")
            analysis = result.get("analysis", {})
            print(f"   Confidence: {analysis.get('processing_confidence', 0):.2f}")
            
            # Check personality differences
            psychology = analysis.get("advanced_psychological_profile", {})
            dating_psych = psychology.get("dating_psychology", {})
            
            print(f"   Personality Type: Creative Introvert")
            print(f"   Cultural Sophistication: {dating_psych.get('cultural_sophistication', {}).get('score', 0):.2f}")
            print(f"   Intellectual Curiosity: {dating_psych.get('intellectual_curiosity', {}).get('score', 0):.2f}")
            
            # Check activities
            qloo_entities = analysis.get("qloo_optimized_entities", {})
            explicit = qloo_entities.get("explicitly_mentioned", {})
            
            print(f"   Activities: {explicit.get('activities', [])}")
            print(f"   Interests: {explicit.get('interests', [])}")
            
            return result
        else:
            print(f"❌ Alternative profile failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Alternative profile error: {e}")
        return None

def test_step_2_cultural_enhancement(step1_result, profile_name="Main Profile"):
    """Test Step 2: Cultural Enhancement - Updated for new CulturalMapper"""
    print(f"\n🎯 STEP 2: Cross-Domain Cultural Enhancement ({profile_name})")
    print("-" * 40)
    
    if not step1_result:
        print(f"❌ Cannot test Step 2 - {profile_name} Step 1 failed")
        return None
    
    try:
        from services.profile_enricher import ProfileEnricher
        print("✅ ProfileEnricher imported successfully")
        
        enricher = ProfileEnricher()
        print("✅ ProfileEnricher initialized")
        print("   Using improved timeouts: 30s search, 45s insights")
        
        # Extract the analysis from Step 1
        psychological_profile = step1_result.get("analysis", {})
        context = step1_result.get("input_context", {})
        
        print("   Processing psychological profile with Qloo cross-domain discovery...")
        enhanced_profile = enricher.process_psychological_profile(
            psychological_profile, 
            context
        )
        
        if enhanced_profile.get("success"):
            print(f"✅ Step 2 - Cross-Domain Enhancement ({profile_name}): SUCCESS")
            
            # Display Step 2 specific results
            metadata = enhanced_profile.get("processing_metadata", {})
            print(f"   Seed entities found: {metadata.get('seed_entities_found', 0)}")
            print(f"   Cross-domain categories: {metadata.get('cross_domain_categories_discovered', 0)}")
            print(f"   Total new discoveries: {metadata.get('total_new_discoveries', 0)}")
            print(f"   Cultural depth enhancement: {metadata.get('cultural_depth_enhancement', 0):.2f}")
            
            # Show explicit interests from Step 1
            explicit_interests = enhanced_profile.get("input_explicit_interests", {})
            print(f"\n   📝 EXPLICIT INTERESTS (from Step 1):")
            for category, items in explicit_interests.items():
                if items:
                    print(f"     {category}: {items}")
            
            # Show cross-domain discoveries
            discoveries = enhanced_profile.get("cross_domain_discoveries", {})
            print(f"\n   🔍 CROSS-DOMAIN DISCOVERIES (new from Step 2):")
            print(f"     🎵 Music discoveries: {len(discoveries.get('music_artists', []))}")
            print(f"     🍽️  Cuisine discoveries: {len(discoveries.get('cuisine_preferences', []))}")
            print(f"     🏃 Activity discoveries: {len(discoveries.get('activity_preferences', []))}")
            print(f"     📚 Book discoveries: {len(discoveries.get('book_genres', []))}")
            print(f"     🎬 Movie discoveries: {len(discoveries.get('movie_preferences', []))}")
            
            # Show confidence scores
            confidence = discoveries.get("discovery_confidence", {})
            if confidence:
                print(f"\n   💯 DISCOVERY CONFIDENCE SCORES:")
                for category, score in confidence.items():
                    if isinstance(score, (int, float)):
                        print(f"     {category}: {score:.2f}")
            
            # Show sample discoveries with names
            print(f"\n   🎯 SAMPLE DISCOVERIES WITH NAMES:")
            
            # Music samples
            music_artists = discoveries.get("music_artists", [])
            if music_artists:
                print(f"     🎵 Music: ", end="")
                music_names = [item.get("name", "Unknown") for item in music_artists[:3]]
                print(f"{', '.join(music_names)}")
            
            # Cuisine samples  
            cuisine = discoveries.get("cuisine_preferences", [])
            if cuisine:
                print(f"     🍽️  Cuisine: ", end="")
                cuisine_names = [item.get("name", "Unknown") for item in cuisine[:3]]
                print(f"{', '.join(cuisine_names)}")
            
            # Activity samples
            activities = discoveries.get("activity_preferences", [])
            if activities:
                print(f"     🏃 Activities: ", end="")
                activity_names = [item.get("name", "Unknown") for item in activities[:3]]
                print(f"{', '.join(activity_names)}")
            
            # Show cultural intelligence
            enriched_cultural = enhanced_profile.get("enriched_cultural_profile", {})
            cultural_intel = enriched_cultural.get("cultural_intelligence", {})
            
            print(f"\n   🧠 CULTURAL INTELLIGENCE:")
            print(f"     Sophistication level: {cultural_intel.get('sophistication_level', 0):.2f}")
            print(f"     Discovery breadth: {cultural_intel.get('discovery_breadth', 0)}")
            print(f"     Cultural depth: {cultural_intel.get('cultural_depth', 0):.2f}")
            print(f"     Personality alignment: {cultural_intel.get('personality_alignment', 'unknown')}")
            
            return enhanced_profile
            
        else:
            print(f"❌ Step 2 failed for {profile_name}: {enhanced_profile.get('error', 'Unknown error')}")
            return enhanced_profile  # Return even failed results for analysis
            
    except Exception as e:
        print(f"❌ Step 2 error for {profile_name}: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_api_connectivity():
    """Test basic API connectivity"""
    print("\n🔌 API Connectivity Tests")
    print("-" * 40)
    
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
            print("   ⚠️  Step 1 may fail without OpenAI key")
        if not qloo_key:
            print("   ⚠️  Step 2 will fail without Qloo key")
            
    except Exception as e:
        print(f"   ❌ API key check failed: {e}")

def main():
    """Run Steps 1-2 test with multiple profile examples"""
    print("Testing STEP 2 FOCUS: Cross-domain cultural enhancement")
    print("Goal: Compare different personality types → cultural discoveries")
    
    # Test API connectivity first
    test_api_connectivity()
    
    # Test Profile 1: Adventure-oriented (Emma)
    print(f"\n" + "🏔️" * 20 + " ADVENTURE PROFILE TEST " + "🏔️" * 20)
    step1_result_adventure = test_step_1_profile_analysis()
    step2_result_adventure = test_step_2_cultural_enhancement(step1_result_adventure, "Adventure Profile")
    
    # Test Profile 2: Creative introvert (Alex)
    print(f"\n" + "🎨" * 20 + " CREATIVE PROFILE TEST " + "🎨" * 20)
    step1_result_creative = test_alternative_profile()
    step2_result_creative = test_step_2_cultural_enhancement(step1_result_creative, "Creative Profile")
    
    # Summary comparison
    print("\n" + "=" * 60)
    print("🏁 PROFILE COMPARISON SUMMARY")
    print("=" * 60)
    
    print("\n🏔️  ADVENTURE PROFILE (Emma - Rock Climbing + Photography):")
    if step1_result_adventure:
        print("✅ Step 1: Profile Analysis - WORKING")
    else:
        print("❌ Step 1: Profile Analysis - FAILED")
    
    if step2_result_adventure and step2_result_adventure.get("success"):
        print("✅ Step 2: Cross-Domain Enhancement - WORKING")
        metadata = step2_result_adventure.get("processing_metadata", {})
        print(f"   🎯 Discoveries: {metadata.get('total_new_discoveries', 0)}")
        print(f"   🧠 Cultural depth: {metadata.get('cultural_depth_enhancement', 0):.2f}")
    else:
        print("❌ Step 2: Cross-Domain Enhancement - FAILED")
    
    print("\n🎨 CREATIVE PROFILE (Alex - Art + Books + Film):")
    if step1_result_creative:
        print("✅ Step 1: Profile Analysis - WORKING")
    else:
        print("❌ Step 1: Profile Analysis - FAILED")
    
    if step2_result_creative and step2_result_creative.get("success"):
        print("✅ Step 2: Cross-Domain Enhancement - WORKING")
        metadata = step2_result_creative.get("processing_metadata", {})
        print(f"   🎯 Discoveries: {metadata.get('total_new_discoveries', 0)}")
        print(f"   🧠 Cultural depth: {metadata.get('cultural_depth_enhancement', 0):.2f}")
    else:
        print("❌ Step 2: Cross-Domain Enhancement - FAILED")
    
    # Overall assessment
    both_working = (
        step2_result_adventure and step2_result_adventure.get("success") and
        step2_result_creative and step2_result_creative.get("success")
    )
    
    if both_working:
        print(f"\n🚀 BOTH PERSONALITY TYPES WORKING!")
        print(f"   Cultural intelligence pipeline handles diverse profiles")
        print(f"   Ready to build Steps 3-5 (Compatibility → Date Plans)")
    else:
        print(f"\n🔧 Need to fix issues before continuing")
    
    print(f"\nNext Phase: Steps 3-5 (Date Plan Generation)")
    print("=" * 60)

if __name__ == "__main__":
    main()