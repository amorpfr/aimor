#!/usr/bin/env python3
"""
Debug what the tags endpoint actually returns
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def debug_tags_api():
    print("🔍 Debugging Tags API Response")
    print("=" * 40)
    
    api_key = os.getenv("QLOO_API_KEY")
    base_url = "https://hackathon.api.qloo.com"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Test with a simple query
    params = {
        "filter.query": "restaurant",
        "limit": 1
    }
    
    print(f"Request URL: {base_url}/v2/tags")
    print(f"Request params: {params}")
    print(f"Request headers: {headers}")
    
    try:
        response = requests.get(f"{base_url}/v2/tags", headers=headers, params=params, timeout=10)
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response text type: {type(response.text)}")
        print(f"Response text length: {len(response.text)}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\nJSON parsed successfully!")
                print(f"Data type: {type(data)}")
                print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                if isinstance(data, dict) and 'results' in data:
                    results = data['results']
                    print(f"Results type: {type(results)}")
                    print(f"Results length: {len(results)}")
                    
                    if results:
                        first_result = results[0]
                        print(f"First result type: {type(first_result)}")
                        print(f"First result: {json.dumps(first_result, indent=2)}")
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
            except Exception as e:
                print(f"Error processing response: {e}")
        else:
            print(f"Request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    debug_tags_api()