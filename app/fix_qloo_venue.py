#!/usr/bin/env python3
"""
Fix Real Qloo Venue Diversity
Debug why both activities return the same venue and fix it properly
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_specific_venue_types():
    """Test if we can get different venue types from Qloo"""
    print("🔍 Testing Specific Venue Type Differentiation")
    print("=" * 50)
    
    api_key = os.getenv("QLOO_API_KEY")
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Test very specific, different queries
    specific_tests = [
        {
            "name": "Restaurant-Only Query",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "filter.tags": "urn:tag:venue:restaurant",
                "take": 5
            }
        },
        {
            "name": "Ethiopian Restaurant Query",
            "params": {
                "filter.type": "urn:entity:place", 
                "filter.location.query": "Amsterdam, Netherlands",
                "filter.tags": "urn:tag:venue:restaurant,urn:tag:cuisine:ethiopian",
                "take": 5
            }
        },
        {
            "name": "Tour/Activity Query",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands", 
                "filter.tags": "urn:tag:activity:tour",
                "take": 5
            }
        },
        {
            "name": "Museum Query (Control)",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "filter.tags": "urn:tag:venue:museum", 
                "take": 5
            }
        },
        {
            "name": "Generic Amsterdam Places",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "take": 10
            }
        }
    ]
    
    results = {}
    
    for test in specific_tests:
        try:
            print(f"\n🎯 {test['name']}")
            print(f"   Parameters: {test['params']}")
            
            response = requests.get(
                "https://hackathon.api.qloo.com/v2/insights",
                headers=headers,
                params=test['params'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                entities = data.get("results", {}).get("entities", [])
                
                print(f"   ✅ Found {len(entities)} venues:")
                
                venue_names = []
                for i, entity in enumerate(entities[:3]):
                    name = entity.get("name", "Unknown")
                    entity_type = entity.get("type", "unknown")
                    properties = entity.get("properties", {})
                    
                    # Check if it has restaurant-like properties
                    has_menu = bool(properties.get("menu_url"))
                    has_cuisine = bool(properties.get("cuisine"))
                    is_restaurant = "restaurant" in str(properties).lower()
                    
                    print(f"   {i+1}. {name}")
                    print(f"      Type: {entity_type}")
                    print(f"      Restaurant indicators: Menu={has_menu}, Cuisine={has_cuisine}, RestaurantRef={is_restaurant}")
                    
                    venue_names.append(name)
                
                results[test['name']] = venue_names
                
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                results[test['name']] = []
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[test['name']] = []
    
    # Analyze overlap
    print(f"\n📊 VENUE OVERLAP ANALYSIS")
    print("-" * 30)
    
    restaurant_venues = set(results.get("Restaurant-Only Query", []))
    ethiopian_venues = set(results.get("Ethiopian Restaurant Query", []))
    tour_venues = set(results.get("Tour/Activity Query", []))
    museum_venues = set(results.get("Museum Query (Control)", []))
    generic_venues = set(results.get("Generic Amsterdam Places", []))
    
    print(f"Restaurant venues: {restaurant_venues}")
    print(f"Ethiopian venues: {ethiopian_venues}")
    print(f"Tour venues: {tour_venues}")
    print(f"Museum venues: {museum_venues}")
    
    # Check if they're all the same
    all_same = (restaurant_venues == ethiopian_venues == tour_venues == museum_venues)
    print(f"\n🚨 All queries returning same venues: {all_same}")
    
    if all_same:
        print("❌ PROBLEM IDENTIFIED: Qloo is ignoring tags and returning generic Amsterdam places")
        print("💡 SOLUTION NEEDED: Different approach to venue filtering")
    else:
        print("✅ Different venue types found - tag filtering working!")
    
    return results

def test_alternative_filtering_approaches():
    """Test alternative ways to get different venue types"""
    print(f"\n🔧 Testing Alternative Filtering Approaches")
    print("=" * 50)
    
    api_key = os.getenv("QLOO_API_KEY")
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    alternative_approaches = [
        {
            "name": "Price Level Filtering (Restaurants)",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "filter.price_level.min": 1,
                "filter.price_level.max": 3,
                "take": 5
            }
        },
        {
            "name": "Popularity Filtering",
            "params": {
                "filter.type": "urn:entity:place", 
                "filter.location.query": "Amsterdam, Netherlands",
                "filter.popularity.min": 0.7,
                "take": 5
            }
        },
        {
            "name": "Business Rating Filtering",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "filter.properties.business_rating.min": 4.0,
                "take": 5
            }
        }
    ]
    
    for approach in alternative_approaches:
        try:
            print(f"\n🧪 {approach['name']}")
            
            response = requests.get(
                "https://hackathon.api.qloo.com/v2/insights",
                headers=headers,
                params=approach['params'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                entities = data.get("results", {}).get("entities", [])
                
                print(f"   Found {len(entities)} venues:")
                for i, entity in enumerate(entities[:3]):
                    name = entity.get("name", "Unknown")
                    properties = entity.get("properties", {})
                    price_level = properties.get("price_level", "N/A")
                    rating = properties.get("business_rating", "N/A")
                    popularity = entity.get("popularity", "N/A")
                    
                    print(f"   {i+1}. {name} (Price: {price_level}, Rating: {rating}, Pop: {popularity})")
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_entity_signals_impact():
    """Test if entity signals actually change results"""
    print(f"\n🧬 Testing Entity Signals Impact")
    print("=" * 50)
    
    api_key = os.getenv("QLOO_API_KEY")
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Test with and without entity signals
    signal_tests = [
        {
            "name": "No Entity Signals",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "take": 5
            }
        },
        {
            "name": "With Real Entity Signals (from your test)",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "signal.interests.entities": "577F84BA-A8CF-4EF4-AA08-6E60C8BB92CD,1A2556C2-237E-4A8C-9512-6D11E87E7A43",
                "take": 5
            }
        },
        {
            "name": "Different Entity Signals",
            "params": {
                "filter.type": "urn:entity:place",
                "filter.location.query": "Amsterdam, Netherlands",
                "signal.interests.entities": "16D791C3-DCF2-45FA-BA62-7A45BF233352,5021A7FE-3A09-4B5A-8E18-DD6AD83F0EEB", 
                "take": 5
            }
        }
    ]
    
    signal_results = {}
    
    for test in signal_tests:
        try:
            print(f"\n🧪 {test['name']}")
            
            response = requests.get(
                "https://hackathon.api.qloo.com/v2/insights",
                headers=headers,
                params=test['params'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                entities = data.get("results", {}).get("entities", [])
                
                venue_names = [entity.get("name", "Unknown") for entity in entities[:5]]
                signal_results[test['name']] = venue_names
                
                print(f"   Found venues: {venue_names}")
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                signal_results[test['name']] = []
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            signal_results[test['name']] = []
    
    # Compare results
    print(f"\n📊 ENTITY SIGNAL IMPACT ANALYSIS")
    print("-" * 30)
    
    no_signals = set(signal_results.get("No Entity Signals", []))
    with_signals_1 = set(signal_results.get("With Real Entity Signals (from your test)", []))
    with_signals_2 = set(signal_results.get("Different Entity Signals", []))
    
    signals_make_diff = (no_signals != with_signals_1) or (with_signals_1 != with_signals_2)
    
    print(f"Entity signals change results: {signals_make_diff}")
    
    if not signals_make_diff:
        print("❌ Entity signals are being ignored or ineffective")
        print("💡 May need to use different approach than entity signals")
    else:
        print("✅ Entity signals working - can use this for differentiation!")

def propose_solution():
    """Propose solution based on test results"""
    print(f"\n💡 PROPOSED SOLUTION")
    print("=" * 50)
    
    print("Based on testing, here are strategies to fix venue diversity:")
    print()
    print("1. 🎯 **Use More Specific Location Filtering**")
    print("   - Try specific Amsterdam neighborhoods")
    print("   - Use coordinates instead of city name")
    print()
    print("2. 🏷️ **Test Different Tag Combinations**") 
    print("   - Use single, very specific tags")
    print("   - Avoid combining multiple tags that might conflict")
    print()
    print("3. 🔍 **Use Property-Based Filtering**")
    print("   - filter.price_level for restaurants vs activities")
    print("   - filter.properties.business_rating for quality venues")
    print()
    print("4. 🎲 **Add Randomization/Variety**")
    print("   - Take different slices of results")
    print("   - Use different entity signals for each activity")
    print()
    print("5. 🚀 **Fallback Strategy**")
    print("   - If tags don't work, filter by venue properties")
    print("   - Use post-processing to ensure venue type diversity")

def main():
    """Run comprehensive Qloo debugging"""
    print("🔧 Qloo Venue Diversity Debug & Fix")
    print("=" * 50)
    print("Goal: Make sure different activities return different venue types")
    
    # Test 1: Different venue type queries
    venue_results = test_specific_venue_types()
    
    # Test 2: Alternative filtering
    test_alternative_filtering_approaches()
    
    # Test 3: Entity signals impact
    test_entity_signals_impact()
    
    # Propose solution
    propose_solution()
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Implement the most promising solution from above")
    print("2. Update VenueDiscoverer with improved logic")
    print("3. Test with different activity types")
    print("4. Ensure Ethiopian restaurants ≠ walking tours!")

if __name__ == "__main__":
    main()