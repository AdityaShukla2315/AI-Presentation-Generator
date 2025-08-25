import re
import logging
from typing import List, Dict

def validate_presentation_data(title: str, slides: List[Dict]) -> List[str]:
    """
    Validate presentation input data
    
    Args:
        title: Presentation title
        slides: List of slide data
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate title
    if not title.strip():
        errors.append("Presentation title is required")
    elif len(title) > 200:
        errors.append("Presentation title must be 200 characters or less")
    
    # Validate slides
    if not slides:
        errors.append("At least one slide is required")
    else:
        for i, slide in enumerate(slides, 1):
            slide_errors = validate_slide_data(slide, i)
            errors.extend(slide_errors)
    
    return errors

def validate_slide_data(slide: Dict, slide_number: int) -> List[str]:
    """
    Validate individual slide data
    
    Args:
        slide: Slide data dictionary
        slide_number: Slide number for error messages
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Validate slide title
    title = slide.get('title', '').strip()
    if not title:
        errors.append(f"Slide {slide_number}: Title is required")
    elif len(title) > 200:
        errors.append(f"Slide {slide_number}: Title must be 200 characters or less")
    
    # Validate bullets
    bullets = slide.get('bullets', [])
    if len(bullets) > 10:
        errors.append(f"Slide {slide_number}: Maximum 10 bullet points allowed")
    
    # Check for empty bullets
    non_empty_bullets = [b for b in bullets if b.strip()]
    if len(bullets) != len(non_empty_bullets):
        logging.warning(f"Slide {slide_number}: Empty bullet points will be removed")
    
    return errors

def slugify_title(title: str) -> str:
    """
    Convert title to safe filename
    
    Args:
        title: Original title
        
    Returns:
        Safe filename slug
    """
    # Remove or replace special characters
    slug = re.sub(r'[^\w\s-]', '', title.strip())
    
    # Replace spaces and multiple dashes with single dash
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # Convert to lowercase and limit length
    slug = slug.lower()[:50]
    
    # Remove leading/trailing dashes
    slug = slug.strip('-')
    
    # Fallback if empty
    if not slug:
        slug = "presentation"
    
    return slug

def validate_file_upload(file) -> List[str]:
    """
    Validate uploaded file
    
    Args:
        file: Flask uploaded file object
        
    Returns:
        List of validation errors
    """
    errors = []
    
    if not file:
        return errors
    
    if not file.filename:
        errors.append("No file selected")
        return errors
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    
    if file_ext not in allowed_extensions:
        errors.append(f"File type '{file_ext}' not allowed. Use: {', '.join(allowed_extensions)}")
    
    return errors

def validate_enhancement_options(mode: str, max_bullets: int, tone: str) -> List[str]:
    """
    Validate AI enhancement options
    
    Args:
        mode: Enhancement mode
        max_bullets: Maximum bullets to add
        tone: Enhancement tone
        
    Returns:
        List of validation errors
    """
    errors = []
    
    valid_modes = ['polish', 'expand', 'notes']
    if mode not in valid_modes:
        errors.append(f"Invalid enhancement mode. Use: {', '.join(valid_modes)}")
    
    if not (1 <= max_bullets <= 5):
        errors.append("Maximum bullets must be between 1 and 5")
    
    valid_tones = ['professional', 'friendly', 'concise', 'formal', 'casual']
    if tone not in valid_tones:
        errors.append(f"Invalid tone. Use: {', '.join(valid_tones)}")
    
    return errors
