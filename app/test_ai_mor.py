#!/usr/bin/env python3
"""
AI-MOR.ME Testing Script
Test all current functionality before Qloo integration
"""

import requests
import json
import base64
from PIL import Image
import io

# Configuration
API_BASE = "http://localhost:8000"

def test_health_endpoint():
    """Test health check and API key validation"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health")
        data = response.json()
        print(f"✅ Health Status: {data['status']}")
        print(f"✅ API Keys Valid: {data['api_keys_valid']}")
        if not data['api_keys_valid']:
            print(f"❌ Missing Keys: {data['missing_keys']}")
        return data['api_keys_valid']
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_demo_endpoint():
    """Test the demo endpoint with sample data"""
    print("\n🎯 Testing Demo Endpoint...")
    try:
        response = requests.get(f"{API_BASE}/demo")
        if response.status_code == 200:
            data = response.json()
            print("✅ Demo endpoint working")
            print(f"✅ Sample analysis completed: {data['result']['success']}")
            if data['result']['success']:
                analysis = data['result']['analysis']
                print(f"✅ Confidence: {analysis.get('processing_confidence', 0):.2f}")
                print(f"✅ Psychology extracted: {'advanced_psychological_profile' in analysis}")
                print(f"✅ Qloo entities ready: {'qloo_optimized_entities' in analysis}")
            return True
        else:
            print(f"❌ Demo failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Demo test failed: {e}")
        return False

def test_text_analysis():
    """Test direct text analysis"""
    print("\n📝 Testing Text Analysis...")
    
    test_profiles = [
        {
            "name": "Adventure Seeker",
            "text": "Emma, 28, Amsterdam local. Passionate rock climber and photographer. Love discovering hidden speakeasies and trying Ethiopian cuisine. Currently learning Portuguese. Work in sustainable fashion. Weekend warrior seeking authentic connections over pretentious small talk.",
            "context": {"location": "amsterdam", "time_of_day": "evening", "season": "autumn"}
        },
        {
            "name": "Creative Introvert", 
            "text": "Alex, 25, graphic designer from Rotterdam. Bookworm obsessed with magical realism novels. Spend weekends at art house cinemas and vintage record shops. Love intimate jazz bars and hate crowded clubs. Looking for deep conversations about life, art, and dreams.",
            "context": {"location": "amsterdam", "time_of_day": "afternoon", "season": "winter"}
        }
    ]
    
    for profile in test_profiles:
        print(f"\n  Testing: {profile['name']}")
        try:
            response = requests.post(f"{API_BASE}/analyze", json={
                "text": profile["text"],
                "context": profile["context"]
            })
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    analysis = data['analysis']
                    print(f"  ✅ Analysis successful (confidence: {analysis.get('processing_confidence', 0):.2f})")
                    
                    # Check key components
                    psych = analysis.get('advanced_psychological_profile', {})
                    entities = analysis.get('qloo_optimized_entities', {})
                    insights = analysis.get('experience_optimization_insights', {})
                    
                    print(f"  ✅ Big Five extracted: {len(psych.get('big_five_detailed', {})) == 5}")
                    print(f"  ✅ Qloo entities: {len(entities.get('explicitly_mentioned', {}))}")
                    print(f"  ✅ Conversation topics: {len(insights.get('conversation_psychology', {}).get('energizing_topics', []))}")
                else:
                    print(f"  ❌ Analysis failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"  ❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Test failed: {e}")

def create_test_image():
    """Create a sample profile image for OCR testing"""
    # Create a simple test image with profile text
    img = Image.new('RGB', (400, 300), color='white')
    
    # This would normally have text, but for testing we'll create a simple colored image
    # In real testing, you'd use an actual screenshot or text image
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_data = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_data}"

def test_image_processing():
    """Test image OCR functionality"""
    print("\n🖼️  Testing Image Processing...")
    
    # Note: This creates a blank image for testing structure
    # For real testing, use actual Tinder screenshots with text
    test_image = create_test_image()
    
    try:
        response = requests.post(f"{API_BASE}/analyze", json={
            "images": [test_image],
            "context": {"location": "amsterdam", "time_of_day": "evening"}
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image processing endpoint working: {data['success']}")
            if not data['success']:
                print(f"⚠️  Expected: OCR extraction returned minimal text (test image blank)")
        else:
            print(f"❌ Image processing failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")

def test_compression_info():
    """Test image compression info endpoint"""
    print("\n📏 Testing Compression Info...")
    try:
        response = requests.get(f"{API_BASE}/compression-info")
        if response.status_code == 200:
            data = response.json()
            print("✅ Compression info available:")
            settings = data.get('compression_settings', {})
            print(f"  - Max dimensions: {settings.get('max_dimensions', 'N/A')}")
            print(f"  - JPEG quality: {settings.get('jpeg_quality', 'N/A')}")
            print(f"  - Max images: {settings.get('max_images', 'N/A')}")
        else:
            print(f"❌ Compression info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Compression info test failed: {e}")

def test_validation_errors():
    """Test error handling and validation"""
    print("\n🚨 Testing Error Handling...")
    
    # Test empty request
    try:
        response = requests.post(f"{API_BASE}/analyze", json={})
        if response.status_code == 400:
            print("✅ Empty request properly rejected")
        else:
            print(f"⚠️  Unexpected status for empty request: {response.status_code}")
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
    
    # Test invalid image data
    try:
        response = requests.post(f"{API_BASE}/analyze", json={
            "images": ["not_base64_data"]
        })
        if response.status_code == 422:
            print("✅ Invalid image data properly rejected")
        else:
            print(f"⚠️  Unexpected status for invalid image: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid image test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 AI-MOR.ME Testing Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"✅ Server running at {API_BASE}")
    except:
        print(f"❌ Server not running at {API_BASE}")
        print("Please start the server with: uvicorn main:app --reload")
        return
    
    # Run tests
    health_ok = test_health_endpoint()
    if not health_ok:
        print("\n❌ API keys not configured properly. Set OPENAI_API_KEY in .env file")
        return
    
    test_demo_endpoint()
    test_text_analysis()
    test_image_processing()
    test_compression_info()
    test_validation_errors()
    
    print("\n" + "=" * 50)
    print("🏁 Testing Complete!")
    print("\nNext Steps:")
    print("1. If all tests pass ✅ - Ready for Qloo integration!")
    print("2. If any tests fail ❌ - Fix issues before proceeding")
    print("3. Test with real Tinder screenshots for OCR validation")

if __name__ == "__main__":
    main()