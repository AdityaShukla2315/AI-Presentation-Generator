import os
import logging
import tempfile
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
from services.ppt_generator import generate_ppt
from services.themes import get_available_themes, get_theme
from services.gemini import enhance_presentation
from services.validators import validate_presentation_data, slugify_title
from services.images import get_image_suggestions, download_image

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    """Main page with presentation creation form"""
    themes = get_available_themes()
    return render_template('index.html', themes=themes)

@main_bp.route('/generate', methods=['POST'])
def generate():
    """Generate PowerPoint presentation"""
    try:
        # Extract form data
        title = request.form.get('title', '').strip()
        theme_name = request.form.get('theme', 'default')
        enhance_ai = 'enhance_ai' in request.form
        enhancement_mode = request.form.get('enhancement_mode', 'polish')
            # Validate enhancement mode
        valid_modes = ['polish', 'expand', 'notes']
        if enhancement_mode not in valid_modes:
            enhancement_mode = 'polish'
        tone = request.form.get('tone', 'professional')
        max_bullets = int(request.form.get('max_bullets', 3))
        
        # Extract slides data
        slides = []
        slide_count = 0
        while f'slide_title_{slide_count}' in request.form:
            slide_title = request.form.get(f'slide_title_{slide_count}', '').strip()
            slide_bullets = request.form.get(f'slide_bullets_{slide_count}', '').strip()
            slide_image_url = request.form.get(f'slide_image_url_{slide_count}', '').strip()
            
            # Handle file upload
            slide_image_path = None
            if f'slide_image_file_{slide_count}' in request.files:
                file = request.files[f'slide_image_file_{slide_count}']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join('temp_uploads', filename)
                    file.save(filepath)
                    slide_image_path = filepath
            
            slides.append({
                'title': slide_title,
                'bullets': [bullet.strip() for bullet in slide_bullets.split('\n') if bullet.strip()],
                'image_url': slide_image_url,
                'image_path': slide_image_path
            })
            slide_count += 1
        
        # Validate input data
        errors = validate_presentation_data(title, slides)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('error.html', 
                                 title="Validation Error", 
                                 message="Please fix the errors and try again.",
                                 errors=errors)
        
        # Get theme
        theme = get_theme(theme_name)
        
        # Prepare presentation data
        presentation_data = {
            'title': title,
            'slides': slides,
            'theme': theme_name,
            'tone': tone
        }
        
        # Enhance with AI if requested
        if enhance_ai:
            try:
                logging.info(f"Enhancing presentation with mode: {enhancement_mode}")
                enhanced_data = enhance_presentation(
                    presentation_data, 
                    enhancement_mode, 
                    max_bullets, 
                    tone
                )
                if enhanced_data:
                    presentation_data = enhanced_data
                    logging.info("AI enhancement completed successfully")
                else:
                    flash("AI enhancement failed, using original content", 'warning')
            except Exception as e:
                logging.error(f"AI enhancement error: {e}")
                flash(f"AI enhancement failed: {str(e)}", 'warning')
        
        # Handle image suggestions if AI enhancement was used
        for slide in presentation_data['slides']:
            if not slide.get('image_url') and not slide.get('image_path'):
                if 'image_keywords' in slide and slide['image_keywords']:
                    try:
                        image_url = get_image_suggestions(slide['image_keywords'])
                        if image_url:
                            slide['image_url'] = image_url
                    except Exception as e:
                        logging.warning(f"Failed to get image suggestions: {e}")
        
        # Generate PowerPoint
        logging.info("Generating PowerPoint presentation")
        ppt_path = generate_ppt(presentation_data['title'], presentation_data['slides'], theme)
        
        # Generate filename
        filename = f"{slugify_title(title)}.pptx"
        
        # Send file and clean up
        def remove_file(response):
            try:
                os.remove(ppt_path)
                # Clean up uploaded images
                for slide in slides:
                    if slide.get('image_path') and os.path.exists(slide['image_path']):
                        os.remove(slide['image_path'])
            except Exception as e:
                logging.error(f"Error cleaning up files: {e}")
            return response
        
        return send_file(
            ppt_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
    except Exception as e:
        logging.error(f"Error generating presentation: {e}")
        return render_template('error.html', 
                             title="Generation Error", 
                             message=f"Failed to generate presentation: {str(e)}")

@main_bp.errorhandler(413)
def too_large(e):
    return render_template('error.html', 
                         title="File Too Large", 
                         message="The uploaded file is too large. Please use a smaller file."), 413

@main_bp.errorhandler(500)
def internal_error(e):
    logging.error(f"Internal server error: {e}")
    return render_template('error.html', 
                         title="Internal Error", 
                         message="An internal error occurred. Please try again."), 500
