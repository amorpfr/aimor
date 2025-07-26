import logging
from typing import Dict, Optional, List, Tuple
from services.profile_analyzer_optimized import ProfileAnalyzer
from services.image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class ProfileProcessor:
    """AI-powered profile processor using OpenAI with intelligent fallbacks"""
    
    def __init__(self):
        self.profile_analyzer = ProfileAnalyzer()
        self.image_processor = ImageProcessor()
    
    def process_profile_with_context(self, text: Optional[str] = None, image_data_list: Optional[List[str]] = None, context: Optional[Dict] = None) -> Dict:
        """Process profile with support for text + multiple images"""
        
        # Step 1: Get combined text from all sources
        profile_text, is_ocr = self._extract_text(text, image_data_list)
        
        if not profile_text:
            return self._empty_profile_response("No text content found")
        
        # Step 2: Use OpenAI with OCR awareness
        analysis = self.profile_analyzer.analyze_profile_with_context(profile_text, context, is_ocr)
        
        if not analysis:
            return self._empty_profile_response("AI analysis failed")
        
        # Step 3: Structure the response
        return {
            "success": True,
            "input_text": profile_text,
            "input_context": context or {},
            "original_context": context,  # ADD THIS LINE
            "input_summary": {
                "text_provided": bool(text),
                "images_provided": len(image_data_list) if image_data_list else 0,
                "combined_sources": len([x for x in [text, image_data_list] if x]),
                "final_text_length": len(profile_text)
            },
            "analysis": analysis,
            "processing_method": f"openai_unified_{'combined' if text and image_data_list else 'multi_ocr' if image_data_list else 'text'}"
        }
        
    def process_profile(self, text: Optional[str] = None, image_data: Optional[str] = None) -> Dict:
        """Process profile without context (for backward compatibility)"""
        return self.process_profile_with_context(text=text, image_data=image_data, context=None)
    
    def _extract_text(self, text: Optional[str], image_data_list: Optional[List[str]] = None) -> tuple[str, bool]:
        """Extract and combine text from all available sources"""
        
        combined_text_parts = []
        has_ocr = False
        
        # Add direct text if provided
        if text and text.strip():
            logger.info("Adding direct text input")
            combined_text_parts.append(text.strip())
        
        # Add OCR text from images (can be 1 or many)
        if image_data_list and len(image_data_list) > 0:
            if len(image_data_list) == 1:
                logger.info("Processing single image with OCR")
                extracted_text = self.image_processor.extract_text_only(image_data_list[0])
            else:
                logger.info(f"Processing {len(image_data_list)} images with OCR")
                extracted_text = self.image_processor.extract_text_from_multiple_images(image_data_list)
            
            if extracted_text and extracted_text.strip():
                combined_text_parts.append(extracted_text.strip())
                has_ocr = True
        
        # Combine all text sources
        if combined_text_parts:
            final_text = " ".join(combined_text_parts)
            logger.info(f"Combined text from {len(combined_text_parts)} sources: {len(final_text)} characters")
            return final_text, has_ocr
        
        logger.warning("No valid input provided")
        return "", False


    def _empty_profile_response(self, error_message: str) -> Dict:
        """Return empty response with error"""
        return {
            "success": False,
            "error": error_message,
            "input_text": "",
            "input_context": {},
            "analysis": {},
            "processing_method": "failed"
        }
    
    def validate_inputs(self, text: Optional[str], image_data: Optional[str]) -> tuple[bool, str]:
        """Validate that at least one input is provided"""
        if not text and not image_data:
            return False, "Either text or image_data must be provided"
        
        if text and len(text.strip()) < 5:
            return False, "Text input too short (minimum 5 characters)"
        
        if image_data and not self.image_processor.validate_image_input(image_data)[0]:
            return False, "Invalid image data format"
        
        return True, "Input validation successful"
    
    def get_processing_summary(self, result: Dict) -> Dict:
        """Get summary of processing results"""
        if not result.get("success"):
            return {
                "status": "failed",
                "error": result.get("error", "Unknown error"),
                "confidence": 0.0
            }
        
        analysis = result.get("analysis", {})
        confidence = analysis.get("processing_confidence", 0.0)
        
        # Extract key insights
        psychological_profile = analysis.get("psychological_profile", {})
        cultural_tags = analysis.get("cultural_preference_tags", {})
        recommended_context = analysis.get("recommended_context", {})
        
        return {
            "status": "success",
            "confidence": confidence,
            "personality_type": self._get_dominant_personality(psychological_profile),
            "key_interests": self._get_top_interests(cultural_tags),
            "recommended_location": recommended_context.get("location", "unknown"),
            "recommended_time": recommended_context.get("time_of_day", "unknown"),
            "processing_method": result.get("processing_method", "unknown")
        }
    
    def _get_dominant_personality(self, psychological_profile: Dict) -> str:
        """Extract dominant personality trait"""
        dating_traits = psychological_profile.get("dating_traits", {})
        if not dating_traits:
            return "balanced"
        
        # Find highest scoring trait
        max_trait = max(dating_traits.items(), key=lambda x: x[1])
        return max_trait[0] if max_trait[1] > 0.6 else "balanced"
    
    def _get_top_interests(self, cultural_tags: Dict) -> list:
        """Extract top interest categories"""
        interests = []
        for category, items in cultural_tags.items():
            if items and len(items) > 0:
                interests.append(category)
        return interests[:3]  # Return top 3 categories