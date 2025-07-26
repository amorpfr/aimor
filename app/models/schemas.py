from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict

class ProfileInput(BaseModel):
    """Input model for profile data"""
    text: Optional[str] = Field(None, description="Text description of the profile")
    image_data: Optional[str] = Field(None, description="Base64 encoded image data")
    
class ContextInput(BaseModel):
    """Input model for date context"""
    location: Optional[str] = Field(None, description="City or location for the date")
    time_of_day: Optional[str] = Field("evening", description="morning, afternoon, evening, night")
    season: Optional[str] = Field(None, description="spring, summer, autumn, winter")
    duration: Optional[str] = Field("3-4 hours", description="Expected duration of the date")
    date_type: Optional[str] = Field("first_date", description="first_date, relationship, anniversary")

class AnalyzeRequest(BaseModel):
    """Request model with automatic image compression"""
    text: Optional[str] = Field(None, description="Direct profile text")
    images: Optional[List[str]] = Field(None, description="Base64 images (auto-compressed)", max_items=5)
    context: Optional[ContextInput] = Field(None, description="Date context")

    # Replace the images validator in schemas.py with this optimized version:

    @validator('images', pre=True)
    def validate_images(cls, v):
        """Validate images with better error messages and performance optimization"""
        if v is None:
            return v
        
        # Convert to list if single string provided
        if isinstance(v, str):
            v = [v]
        
        if not isinstance(v, list):
            raise ValueError("Images must be a list of base64 strings")
        
        # Limit to 2 images for hackathon performance (most users upload 1-2 anyway)
        if len(v) > 2:
            logger.warning(f"Limiting to first 2 images (received {len(v)})")
            v = v[:2]
        
        validated_images = []
        total_size = 0
        
        for i, image_data in enumerate(v):
            try:
                if not image_data or not isinstance(image_data, str):
                    raise ValueError(f"Image {i+1}: Must be a non-empty string")
                
                # Extract base64 part
                if image_data.startswith('data:image'):
                    base64_data = image_data.split(',')[1]
                else:
                    base64_data = image_data
                    # Add proper data URL prefix if missing
                    image_data = f"data:image/jpeg;base64,{base64_data}"
                
                # Validate base64 format
                try:
                    decoded = base64.b64decode(base64_data, validate=True)
                except Exception:
                    raise ValueError(f"Image {i+1}: Invalid base64 format")
                
                # Check if it's actually an image (basic check)
                if len(decoded) < 100:
                    raise ValueError(f"Image {i+1}: File too small to be a valid image")
                
                # Calculate size
                size = len(decoded)
                total_size += size
                
                # Log large images (will be compressed anyway)
                if size > 1_000_000:  # 1MB
                    logger.info(f"Large image detected: Image {i+1} is {size//1024}KB (will be compressed)")
                
                validated_images.append(image_data)
                
            except ValueError:
                raise
            except Exception as e:
                raise ValueError(f"Image {i+1}: Processing error - {str(e)}")
        
        # Check total size (more generous for hackathon)
        if total_size > 10_000_000:  # 10MB total limit
            size_mb = total_size / (1024 * 1024)
            raise ValueError(f"Total image size too large ({size_mb:.1f}MB). Maximum: 10MB.")
        
        return validated_images

    @validator('text')
    def validate_text_length(cls, v):
        """Validate text length"""
        if v and len(v) > 10000:
            raise ValueError("Text too long. Maximum 10,000 characters allowed")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Sarah, 26. Love hiking and outdoor adventures.",
                "images": [
                    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
                ],
                "context": {
                    "location": "amsterdam",
                    "time_of_day": "evening"
                }
            }
        }

class DatePlanRequest(BaseModel):
    """Main request model for date planning"""
    profile_a: ProfileInput = Field(..., description="First person's profile")
    profile_b: ProfileInput = Field(..., description="Second person's profile")
    context: ContextInput = Field(..., description="Date context and preferences")

# Response models remain the same
class VenueRecommendation(BaseModel):
    """Model for venue recommendations"""
    name: str
    type: str  # restaurant, activity, cafe, etc.
    address: str
    description: str
    reasoning: str
    backup_options: List[str] = []

class ConversationTopic(BaseModel):
    """Model for conversation suggestions"""
    topic: str
    context: str
    reasoning: str

class DatePlan(BaseModel):
    """Complete date plan response"""
    plan_id: str
    title: str
    duration: str
    activities: List[VenueRecommendation]
    conversation_topics: List[ConversationTopic]
    contingency_plans: dict
    confidence_score: Optional[float] = None

class DatePlanResponse(BaseModel):
    """Response model for date planning"""
    success: bool
    message: str
    data: Optional[DatePlan] = None
    
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    timestamp: str