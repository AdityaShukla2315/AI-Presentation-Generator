import pytest
import os
import tempfile
from services.ppt_generator import generate_ppt
from services.themes import get_theme

def test_generate_basic_ppt():
    """Test basic PowerPoint generation"""
    title = "Test Presentation"
    slides = [
        {
            'title': 'Introduction',
            'bullets': ['First point', 'Second point', 'Third point']
        },
        {
            'title': 'Conclusion',
            'bullets': ['Summary', 'Next steps']
        }
    ]
    theme = get_theme('default')
    
    # Generate presentation
    ppt_path = generate_ppt(title, slides, theme)
    
    # Verify file was created
    assert os.path.exists(ppt_path)
    
    # Verify file size (should be > 0)
    assert os.path.getsize(ppt_path) > 0
    
    # Clean up
    os.remove(ppt_path)

def test_generate_ppt_with_speaker_notes():
    """Test PowerPoint generation with speaker notes"""
    title = "Test Presentation with Notes"
    slides = [
        {
            'title': 'Introduction',
            'bullets': ['First point'],
            'speaker_notes': 'This is a speaker note for the introduction slide.'
        }
    ]
    theme = get_theme('dark')
    
    # Generate presentation
    ppt_path = generate_ppt(title, slides, theme)
    
    # Verify file was created
    assert os.path.exists(ppt_path)
    assert os.path.getsize(ppt_path) > 0
    
    # Clean up
    os.remove(ppt_path)

def test_generate_empty_slides():
    """Test handling of empty slides"""
    title = "Test Empty"
    slides = []
    theme = get_theme('default')
    
    # Should create presentation with just title slide
    ppt_path = generate_ppt(title, slides, theme)
    
    assert os.path.exists(ppt_path)
    assert os.path.getsize(ppt_path) > 0
    
    # Clean up
    os.remove(ppt_path)

def test_all_themes():
    """Test all available themes"""
    from services.themes import get_available_themes
    
    title = "Theme Test"
    slides = [{'title': 'Test Slide', 'bullets': ['Test bullet']}]
    
    themes = get_available_themes()
    
    for theme_info in themes:
        theme = get_theme(theme_info['key'])
        ppt_path = generate_ppt(title, slides, theme)
        
        assert os.path.exists(ppt_path)
        assert os.path.getsize(ppt_path) > 0
        
        # Clean up
        os.remove(ppt_path)
