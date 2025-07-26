#!/usr/bin/env python3
"""
Test basic Qloo API connectivity
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_qloo_api():
    print("🔍 Testing Qloo API Basic Connectivity")
    print("=" * 50)
    
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        print("❌ No Qloo API key found")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    base_url = "https://hackathon.api.qloo.com"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Test 1: Basic root endpoint
    print("\n🌐 Test 1: Root endpoint")
    try:
        response = requests.get(f"{base_url}/", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Try insights endpoint with proper signals
    print("\n🎯 Test 2: Insights with valid signal")
    try:
        params = {
            "filter.type": "urn:entity:place",
            "signal.location.query": "amsterdam",  # Add required signal
            "take": 5
        }
        response = requests.get(f"{base_url}/v2/insights", headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('results', {}).get('entities', []))} entities")
        else:
            print(f"❌ Failed: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Try search endpoint with 'query' parameter
    print("\n🔍 Test 3: Search with 'query' parameter")
    try:
        params = {
            "query": "restaurant amsterdam",  # Try 'query' instead of 'q'
            "limit": 3
        }
        response = requests.get(f"{base_url}/search", headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('results', []))} results")
            # Show first result
            if data.get('results'):
                first = data['results'][0]
                print(f"   Sample: {first.get('name', 'Unknown')} ({first.get('entity_id', 'No ID')})")
        else:
            print(f"❌ Failed: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
        
    # Test 3b: Try with filter parameter instead
    print("\n🔍 Test 3b: Search with filter parameter")
    try:
        params = {
            "filter.query": "restaurant amsterdam",  # Try filter.query
            "limit": 3
        }
        response = requests.get(f"{base_url}/search", headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('results', []))} results")
        else:
            print(f"❌ Failed: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Try tags endpoint with filter.query
    print("\n🏷️  Test 4: Tags with filter.query")
    try:
        params = {
            "filter.query": "restaurant",
            "limit": 3
        }
        response = requests.get(f"{base_url}/v2/tags", headers=headers, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('results', []))} tags")
            # Show first result
            if data.get('results'):
                first = data['results'][0]
                print(f"   Sample: {first.get('name', 'Unknown')} ({first.get('tag_id', 'No ID')})")
        else:
            print(f"❌ Failed: {response.text[:200]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_qloo_api()