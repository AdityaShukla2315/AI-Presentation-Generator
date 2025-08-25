import json
import logging
import os
from typing import Dict, List, Optional, Literal
from google import genai
from google.genai import types
from pydantic import BaseModel

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class SlideData(BaseModel):
    title: str
    bullets: List[str]
    speaker_notes: Optional[str] = None
    image_keywords: Optional[List[str]] = None

class EnhancedPresentation(BaseModel):
    title: str
    slides: List[SlideData]

def enhance_presentation(
    presentation_data: Dict, 
    mode: Literal["polish", "expand", "notes"], 
    max_new_bullets: int = 3, 
    tone: str = "professional"
) -> Optional[Dict]:
    """
    Enhance presentation content using Gemini AI
    
    Args:
        presentation_data: Original presentation data
        mode: Enhancement mode (polish, expand, notes)
        max_new_bullets: Maximum new bullets to add in expand mode
        tone: Tone for enhancement (professional, friendly, concise)
    
    Returns:
        Enhanced presentation data or None if failed
    """
    try:
        # Build prompt based on mode
        system_prompt = build_system_prompt(mode, max_new_bullets, tone)
        user_prompt = build_user_prompt(presentation_data)
        
        logging.info(f"Sending prompt to Gemini with mode: {mode}")
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=EnhancedPresentation,
                temperature=float(os.environ.get("GEMINI_TEMPERATURE", "0.4"))
            ),
        )
        
        if not response.text:
            logging.error("Empty response from Gemini")
            return None
        
        # Parse JSON response
        try:
            enhanced_data = json.loads(response.text)
            logging.info("Successfully parsed Gemini response")
            
            # Convert back to expected format
            result = {
                'title': enhanced_data.get('title', presentation_data['title']),
                'slides': []
            }
            
            for slide_data in enhanced_data.get('slides', []):
                slide = {
                    'title': slide_data.get('title', ''),
                    'bullets': slide_data.get('bullets', []),
                }
                
                # Add optional fields if present
                if 'speaker_notes' in slide_data and slide_data['speaker_notes']:
                    slide['speaker_notes'] = slide_data['speaker_notes']
                
                if 'image_keywords' in slide_data and slide_data['image_keywords']:
                    slide['image_keywords'] = slide_data['image_keywords']
                
                # Preserve original image data if no new suggestions
                original_slide = None
                if len(presentation_data['slides']) > len(result['slides']):
                    original_slide = presentation_data['slides'][len(result['slides'])]
                
                if original_slide:
                    if 'image_url' in original_slide:
                        slide['image_url'] = original_slide['image_url']
                    if 'image_path' in original_slide:
                        slide['image_path'] = original_slide['image_path']
                
                result['slides'].append(slide)
            
            return result
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Gemini JSON response: {e}")
            return None
            
    except Exception as e:
        logging.error(f"Error enhancing presentation with Gemini: {e}")
        return None

def build_system_prompt(mode: str, max_new_bullets: int, tone: str) -> str:
    """Build system prompt based on enhancement mode"""
    
    base_prompt = f"""You are an expert presentation consultant. Your task is to enhance presentation content with a {tone} tone.

IMPORTANT RULES:
1. Preserve all factual information and technical terms
2. Do not invent or fabricate specific facts, statistics, or data
3. Keep domain-specific terminology intact
4. Maintain the original meaning while improving clarity
5. Respond with valid JSON only, no additional text
6. Follow the exact schema provided"""
    
    if mode == "polish":
        specific_instructions = """
Your task: Polish and improve existing content for clarity and impact.
- Rewrite slide titles to be more engaging and clear
- Improve bullet points for better flow and readability
- Maintain all original facts and technical details
- Keep the same number of bullet points"""
        
    elif mode == "expand":
        specific_instructions = f"""
Your task: Expand content with additional relevant points.
- Improve existing titles and bullets
- Add up to {max_new_bullets} new bullet points per slide that complement existing content
- New bullets should be logical extensions, not repetitions
- Suggest 2-3 relevant image keywords per slide for visual enhancement"""
        
    elif mode == "notes":
        specific_instructions = """
Your task: Generate speaker notes and polish content.
- Improve titles and bullet points for presentation delivery
- Generate detailed speaker notes (2-3 sentences) for each slide
- Speaker notes should provide context and talking points
- Suggest relevant image keywords for visual appeal"""
    
    return f"{base_prompt}\n\n{specific_instructions}"

def build_user_prompt(presentation_data: Dict) -> str:
    """Build user prompt with presentation data"""
    
    slides_text = ""
    for i, slide in enumerate(presentation_data['slides'], 1):
        bullets_text = "\n".join([f"  - {bullet}" for bullet in slide.get('bullets', [])])
        slides_text += f"""
Slide {i}:
  Title: {slide.get('title', '')}
  Bullets:
{bullets_text}
"""
    
    return f"""Please enhance this presentation:

Title: {presentation_data['title']}
Theme: {presentation_data.get('theme', 'default')}
Tone: {presentation_data.get('tone', 'professional')}

Slides:{slides_text}

Respond with JSON following the exact schema with enhanced content."""
