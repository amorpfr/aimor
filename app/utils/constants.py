"""Cultural Intelligence Constants for Date Planning"""

# === PERSONALITY-VENUE MAPPING ===
PERSONALITY_VENUE_MAPPING = {
    "creative_introverted": {
        "preferred": ["art_galleries", "independent_bookstores", "craft_coffee_shops", "small_theaters"],
        "avoid": ["sports_bars", "loud_clubs", "crowded_markets"],
        "conversation_spots": ["quiet_corners", "outdoor_gardens", "museum_cafes"]
    },
    "adventurous_extroverted": {
        "preferred": ["rooftop_bars", "food_markets", "interactive_experiences", "live_music"],
        "avoid": ["formal_dining", "libraries", "quiet_cafes"],
        "conversation_spots": ["bar_counters", "shared_activities", "walking_tours"]
    },
    "intellectual_curious": {
        "preferred": ["museums", "wine_tastings", "documentary_screenings", "lecture_halls"],
        "avoid": ["superficial_venues", "pure_entertainment"],
        "conversation_spots": ["discussion_areas", "educational_settings"]
    },
    "social_optimistic": {
        "preferred": ["busy_restaurants", "group_activities", "festivals", "community_events"],
        "avoid": ["isolated_locations", "overly_quiet_spaces"],
        "conversation_spots": ["social_hubs", "people_watching_spots"]
    },
    "sophisticated_refined": {
        "preferred": ["fine_dining", "wine_bars", "classical_concerts", "upscale_galleries"],
        "avoid": ["casual_chains", "loud_venues", "overly_trendy_spots"],
        "conversation_spots": ["elegant_lounges", "sophisticated_settings"]
    }
}

# === CULTURAL CONVERSATION CATALYSTS ===
CONVERSATION_BRIDGES = {
    "music_to_food": "People who love {music_genre} often appreciate {food_style} - both value {shared_attribute}",
    "travel_to_local": "Your {travel_destination} photos suggest you'd love {local_equivalent} here",
    "art_to_personality": "Your interest in {art_style} reveals you probably value {personality_trait}",
    "books_to_experiences": "Since you read {book_genre}, you might enjoy {experience_type}",
    "fitness_to_adventure": "Your {fitness_activity} suggests you'd love {adventure_activity}",
    "photography_to_exploration": "Your photography style shows you have an eye for {aesthetic} - perfect for {venue_type}",
    "food_to_culture": "Your love for {cuisine_type} suggests you appreciate {cultural_value}",
    "humor_to_venue": "Your sense of humor would shine in {venue_atmosphere} settings"
}

# === LOCATION CULTURAL INTELLIGENCE ===
CITY_DATING_CULTURES = {
    "amsterdam": {
        "typical_duration": "4-6 hours",
        "preferred_flow": ["cafe", "canal_walk", "brown_cafe", "late_night_snack"],
        "weather_backup": "extensive_indoor_options",
        "local_customs": ["dutch_directness", "bike_accessibility", "early_dinner_culture"],
        "conversation_topics": ["travel", "sustainability", "art", "work_life_balance"],
        "cultural_notes": "Amsterdam values authenticity and work-life balance"
    },
    "new_york": {
        "typical_duration": "3-4 hours", 
        "preferred_flow": ["drinks", "dinner", "walk", "dessert_elsewhere"],
        "weather_backup": "subway_accessible_indoor",
        "local_customs": ["fast_paced", "diverse_neighborhoods", "late_dining"],
        "conversation_topics": ["careers", "culture", "neighborhoods", "ambitions"],
        "cultural_notes": "NYC values ambition and cultural sophistication"
    },
    "london": {
        "typical_duration": "4-5 hours",
        "preferred_flow": ["pub", "dinner", "walk", "coffee"],
        "weather_backup": "pub_culture_indoor",
        "local_customs": ["pub_etiquette", "politeness", "queue_culture"],
        "conversation_topics": ["humor", "travel", "culture", "current_events"],
        "cultural_notes": "London values wit and cultural awareness"
    },
    "paris": {
        "typical_duration": "5-6 hours",
        "preferred_flow": ["aperitif", "dinner", "walk", "late_cafe"],
        "weather_backup": "cafe_culture_indoor",
        "local_customs": ["dining_etiquette", "fashion_awareness", "intellectual_discourse"],
        "conversation_topics": ["art", "philosophy", "culture", "gastronomy"],
        "cultural_notes": "Paris values intellectual depth and aesthetic appreciation"
    }
}

# === CHEMISTRY OPTIMIZATION ===
CHEMISTRY_FACTORS = {
    "shared_experiences": {
        "weight": 0.4,
        "activities": ["cooking_together", "learning_together", "exploring_together"],
        "psychological_basis": "Shared novel experiences create stronger bonds"
    },
    "conversation_flow": {
        "weight": 0.3,
        "enhancers": ["ask_follow_up", "share_stories", "find_commonalities"],
        "psychological_basis": "Active listening and vulnerability build connection"
    },
    "environmental_comfort": {
        "weight": 0.3,
        "factors": ["noise_level", "intimacy_level", "distraction_level"],
        "psychological_basis": "Comfortable environment enables authentic interaction"
    }
}

# === CONTINGENCY INTELLIGENCE ===
BACKUP_LOGIC = {
    "weather_alternatives": {
        "outdoor_activity": ["indoor_museum", "covered_market", "cozy_cafe"],
        "walking_date": ["gallery_hopping", "indoor_shopping", "bookstore_browsing"],
        "park_picnic": ["food_hall", "cooking_class", "wine_tasting"],
        "rooftop_drinks": ["speakeasy_bar", "wine_cellar", "intimate_lounge"]
    },
    "venue_full_alternatives": {
        "popular_restaurant": ["similar_vibe_nearby", "different_cuisine_same_energy", "backup_reservation"],
        "sold_out_show": ["alternative_entertainment", "spontaneous_activity", "conversation_focused"],
        "crowded_museum": ["smaller_gallery", "different_exhibition", "outdoor_sculpture"]
    },
    "energy_level_adjustments": {
        "low_energy": ["shorter_activities", "sitting_focused", "relaxed_pace"],
        "high_energy": ["extended_activities", "walking_intensive", "multiple_locations"],
        "variable_energy": ["flexible_timeline", "optional_extensions", "natural_endpoints"]
    }
}

# === QLOO INTEGRATION MAPPING ===
QLOO_CATEGORY_MAPPING = {
    "music_genres": ["indie", "electronic", "jazz", "hip_hop", "classical", "rock", "folk", "r&b"],
    "food_preferences": ["artisanal", "ethnic", "comfort", "healthy", "experimental", "traditional"],
    "activity_types": ["cultural", "active", "social", "intellectual", "creative", "adventurous"],
    "venue_atmospheres": ["intimate", "lively", "sophisticated", "casual", "unique", "trendy"],
    "cultural_interests": ["art", "history", "science", "literature", "film", "theater", "architecture"]
}

# === CONVERSATION PSYCHOLOGY ===
CONVERSATION_STARTERS = {
    "shared_values": "What's something you believe strongly in that might surprise people?",
    "cultural_discovery": "What's a place you've been that changed how you see the world?",
    "creative_expression": "What's your favorite way to be creative, even if you don't consider yourself artistic?",
    "life_philosophy": "What's a piece of advice you'd give to your younger self?",
    "future_dreams": "If you could master any skill instantly, what would it be?",
    "meaningful_experiences": "What's the most meaningful gift you've ever given or received?",
    "personal_growth": "What's something you've learned about yourself recently?",
    "curiosity_driven": "What's something you're curious about but haven't had time to explore?"
}

# === DEMOGRAPHIC ADJUSTMENTS ===
AGE_GROUP_PREFERENCES = {
    "20_25": {"energy": "high", "budget": "moderate", "time": "flexible", "style": "casual_trendy"},
    "26_30": {"energy": "moderate", "budget": "higher", "time": "limited", "style": "sophisticated_casual"},
    "31_35": {"energy": "moderate", "budget": "high", "time": "precious", "style": "quality_focused"},
    "36_plus": {"energy": "selective", "budget": "high", "time": "intentional", "style": "refined"}
}

# === SEASONAL ADJUSTMENTS ===
SEASONAL_PREFERENCES = {
    "spring": {
        "outdoor_bias": 0.7,
        "activities": ["garden_walks", "outdoor_markets", "terrace_dining", "park_activities"],
        "mood": "optimistic_renewal"
    },
    "summer": {
        "outdoor_bias": 0.9,
        "activities": ["rooftop_bars", "outdoor_concerts", "beach_walks", "festival_events"],
        "mood": "energetic_social"
    },
    "autumn": {
        "outdoor_bias": 0.5,
        "activities": ["cozy_cafes", "museums", "warm_restaurants", "cultural_events"],
        "mood": "contemplative_cozy"
    },
    "winter": {
        "outdoor_bias": 0.2,
        "activities": ["intimate_dining", "indoor_entertainment", "warm_bars", "cultural_venues"],
        "mood": "intimate_reflective"
    }
}

# === TIME-BASED PREFERENCES ===
TIME_SLOT_CHARACTERISTICS = {
    "morning": {"energy": "fresh", "activities": ["coffee", "walks", "markets"], "duration": "2-3 hours"},
    "afternoon": {"energy": "active", "activities": ["museums", "lunch", "activities"], "duration": "3-4 hours"},
    "evening": {"energy": "social", "activities": ["dinner", "drinks", "entertainment"], "duration": "4-5 hours"},
    "night": {"energy": "intimate", "activities": ["late_dining", "bars", "shows"], "duration": "3-4 hours"}
}

# === RESPONSE TEMPLATES ===
SUCCESS_RESPONSE = {"success": True, "message": "Date plan created successfully"}
ERROR_RESPONSE = {"success": False, "message": "Unable to create date plan"}

# === CACHE CONFIGURATIONS ===
CACHE_KEY_PREFIX = "aimor"
PROFILE_CACHE_KEY = f"{CACHE_KEY_PREFIX}:profile"
DATE_PLAN_CACHE_KEY = f"{CACHE_KEY_PREFIX}:dateplan"
QLOO_CACHE_KEY = f"{CACHE_KEY_PREFIX}:qloo"

# === API CONFIGURATIONS ===
OPENAI_MODELS = {
    "gpt-4o-mini": {"max_tokens": 4096, "temperature": 0.7},
    "gpt-4o": {"max_tokens": 4096, "temperature": 0.7},
    "gpt-3.5-turbo": {"max_tokens": 4096, "temperature": 0.7}
}

# === CULTURAL INTELLIGENCE WEIGHTS ===
PERSONALITY_WEIGHTS = {
    "introversion_extroversion": 0.3,
    "cultural_sophistication": 0.25,
    "adventure_seeking": 0.2,
    "intellectual_curiosity": 0.15,
    "social_energy": 0.1
}

# === VENUE SCORING FACTORS ===
VENUE_SCORING = {
    "personality_match": 0.4,
    "cultural_alignment": 0.3,
    "practical_factors": 0.2,
    "uniqueness": 0.1
}