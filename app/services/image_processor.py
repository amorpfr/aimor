import logging
import base64
import io
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from typing import List, Optional, Dict, Tuple
import re

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Advanced OCR processor with automatic image compression"""
    
    def __init__(self):
        self.supported_formats = ['JPEG', 'PNG', 'JPG', 'WEBP']
        self.max_image_size = (1024, 768)  # Compress to reasonable size
        self.max_images = 5
        self.compression_quality = 85  # JPEG quality (85 = good quality, smaller size)
        
    def extract_text_from_multiple_images(self, image_data_list: List[str]) -> str:
        """Extract and consolidate text from multiple profile images with compression"""
        if not image_data_list:
            logger.warning("No image data provided")
            return ""
        
        # Limit number of images
        if len(image_data_list) > self.max_images:
            logger.warning(f"Too many images ({len(image_data_list)}), processing first {self.max_images}")
            image_data_list = image_data_list[:self.max_images]
        
        extracted_texts = []
        
        for i, image_data in enumerate(image_data_list):
            try:
                logger.info(f"Processing image {i+1} of {len(image_data_list)}")
                
                # Extract text with automatic compression
                text = self.extract_text_only(image_data)
                
                if text and len(text.strip()) > 3:
                    extracted_texts.append({
                        'image_index': i + 1,
                        'text': text,
                        'length': len(text)
                    })
                    logger.info(f"Image {i+1}: Extracted {len(text)} characters")
                else:
                    logger.warning(f"Image {i+1}: No meaningful text extracted")
                    
            except Exception as e:
                logger.error(f"Failed to process image {i+1}: {str(e)}")
                continue
        
        if not extracted_texts:
            logger.error("No text extracted from any images")
            return ""
        
        # Consolidate all extracted text
        consolidated_text = self._consolidate_extracted_texts(extracted_texts)
        
        logger.info(f"Successfully consolidated text from {len(extracted_texts)} images")
        return consolidated_text
    
    def extract_text_only(self, image_data: str) -> str:
        """Extract text from single image with automatic compression"""
        try:
            # Step 1: Decode and compress image
            compressed_image = self._decode_and_compress_image(image_data)
            if compressed_image is None:
                return ""
            
            # Step 2: Preprocess for better OCR
            processed_image = self._preprocess_for_ocr(compressed_image)
            
            # Step 3: Extract text with multiple OCR attempts
            raw_text = self._extract_raw_text_with_fallbacks(processed_image)
            
            # Step 4: Clean the text
            cleaned_text = self._basic_text_cleaning(raw_text)
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return ""
    
    def _decode_and_compress_image(self, image_data: str) -> Optional[Image.Image]:
        """Decode base64 image and automatically compress it"""
        try:
            # Remove data URL prefix if present
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            # Calculate original size
            original_size = len(image_data) * 3 // 4  # Approximate base64 to bytes conversion
            logger.info(f"Original image size: ~{original_size // 1024}KB")
            
            # Decode image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Validate format
            if image.format not in self.supported_formats:
                logger.warning(f"Unsupported image format: {image.format}")
                return None
            
            # Compress the image
            compressed_image = self._compress_image(image)
            
            return compressed_image
            
        except Exception as e:
            logger.error(f"Image decoding/compression failed: {str(e)}")
            return None
    
    def _compress_image(self, image: Image.Image) -> Image.Image:
        """Compress image to reduce size while maintaining OCR quality"""
        try:
            # Convert to RGB if needed (for JPEG compression)
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            
            # Get original dimensions
            original_width, original_height = image.size
            logger.info(f"Original dimensions: {original_width}x{original_height}")
            
            # Resize if too large
            if original_width > self.max_image_size[0] or original_height > self.max_image_size[1]:
                # Calculate new size maintaining aspect ratio
                ratio = min(
                    self.max_image_size[0] / original_width,
                    self.max_image_size[1] / original_height
                )
                
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                
                # Resize with high-quality resampling
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"Resized to: {new_width}x{new_height} (ratio: {ratio:.2f})")
            
            # Compress by saving as JPEG with quality setting
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=self.compression_quality, optimize=True)
            
            # Calculate compressed size
            compressed_size = len(output_buffer.getvalue())
            logger.info(f"Compressed size: ~{compressed_size // 1024}KB (quality: {self.compression_quality})")
            
            # Load compressed image for processing
            output_buffer.seek(0)
            compressed_image = Image.open(output_buffer)
            
            return compressed_image
            
        except Exception as e:
            logger.error(f"Image compression failed: {str(e)}")
            return image  # Return original if compression fails
    
    def _preprocess_for_ocr(self, image: Image.Image) -> Image.Image:
        """Preprocess compressed image for better OCR results"""
        try:
            # Ensure RGB mode
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance contrast (important after compression)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)  # Slightly higher contrast after compression
            
            # Enhance sharpness (to counter compression softening)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.2)
            
            return image
            
        except Exception:
            return image
    
    def _extract_raw_text_with_fallbacks(self, image: Image.Image) -> str:
        """Extract text with multiple OCR configurations"""
        try:
            configs = [
                r'--oem 3 --psm 6',  # Uniform block of text
                r'--oem 3 --psm 8',  # Single word
                r'--oem 3 --psm 13', # Raw line
                r'--oem 3 --psm 11', # Sparse text
                r'--oem 3 --psm 4',  # Single column
            ]
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(image, config=config)
                    if text and len(text.strip()) > 5:
                        logger.info(f"OCR successful with config: {config}")
                        return text
                except Exception as e:
                    logger.warning(f"OCR config {config} failed: {e}")
                    continue
            
            # Last resort - basic OCR
            logger.info("Using basic OCR as fallback")
            return pytesseract.image_to_string(image)
            
        except Exception as e:
            logger.error(f"All OCR attempts failed: {str(e)}")
            return ""
    
    def _basic_text_cleaning(self, text: str) -> str:
        """Clean OCR text artifacts"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common OCR artifacts
        text = text.replace('|', 'I')
        text = text.replace('\\', '')
        text = text.replace('~', '')
        
        # Remove lines that are just numbers or single characters
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if len(line) > 2 and not line.isdigit():
                cleaned_lines.append(line)
        
        # Join and clean up
        result = ' '.join(cleaned_lines).strip()
        
        # Remove excessive punctuation
        result = re.sub(r'[.]{3,}', '...', result)
        result = re.sub(r'[!]{2,}', '!', result)
        
        return result
    
    def _consolidate_extracted_texts(self, extracted_texts: List[Dict]) -> str:
        """Consolidate text from multiple images"""
        if not extracted_texts:
            return ""
        
        if len(extracted_texts) == 1:
            return extracted_texts[0]['text']
        
        # Sort by text length (longer texts often have more complete info)
        sorted_texts = sorted(extracted_texts, key=lambda x: x['length'], reverse=True)
        
        consolidated_parts = []
        seen_content = set()
        
        for text_info in sorted_texts:
            text = text_info['text']
            
            # Split into sentences for deduplication
            sentences = re.split(r'[.!?]+', text)
            unique_sentences = []
            
            for sentence in sentences:
                sentence_key = re.sub(r'[^\w\s]', '', sentence.lower()).strip()
                if sentence_key and sentence_key not in seen_content and len(sentence.strip()) > 5:
                    unique_sentences.append(sentence.strip())
                    seen_content.add(sentence_key)
            
            if unique_sentences:
                consolidated_parts.extend(unique_sentences)
        
        # Join all unique content
        final_text = '. '.join(consolidated_parts)
        
        # Final cleanup
        final_text = re.sub(r'\s+', ' ', final_text).strip()
        
        return final_text
    
    def validate_image_inputs(self, image_data_list: List[str]) -> Tuple[bool, str]:
        """Validate multiple image inputs with size checking"""
        if not image_data_list:
            return False, "No image data provided"
        
        if len(image_data_list) > self.max_images:
            return False, f"Too many images (max {self.max_images})"
        
        total_size = 0
        valid_count = 0
        
        for i, image_data in enumerate(image_data_list):
            try:
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                
                # Check if valid base64
                base64.b64decode(image_data)
                
                # Estimate size
                estimated_size = len(image_data) * 3 // 4
                total_size += estimated_size
                valid_count += 1
                
                # Warn about large individual images
                if estimated_size > 2_000_000:  # 2MB
                    logger.warning(f"Image {i+1} is large ({estimated_size // 1024}KB) - will be compressed")
                    
            except Exception:
                logger.warning(f"Image {i+1} has invalid base64 data")
        
        if valid_count == 0:
            return False, "No valid image data found"
        
        # Check total size
        if total_size > 10_000_000:  # 10MB total limit
            return False, f"Total image size too large ({total_size // 1024 // 1024}MB). Limit: 10MB"
        
        return True, f"Valid: {valid_count}/{len(image_data_list)} images (~{total_size // 1024}KB total)"
    
    def get_compression_info(self) -> Dict:
        """Get compression configuration info"""
        return {
            "max_dimensions": f"{self.max_image_size[0]}x{self.max_image_size[1]}",
            "jpeg_quality": self.compression_quality,
            "max_images": self.max_images,
            "compression_enabled": True
        }