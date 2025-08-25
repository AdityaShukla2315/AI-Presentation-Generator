// AI PowerPoint Generator - Client-side functionality

document.addEventListener('DOMContentLoaded', function() {
    let slideCount = 1;
    
    // Add slide functionality
    document.getElementById('addSlideBtn').addEventListener('click', function() {
        addSlide();
    });
    
    // Initial setup for remove buttons
    updateRemoveButtons();
    
    function addSlide() {
        const slidesContainer = document.getElementById('slidesContainer');
        const newSlideHtml = createSlideHtml(slideCount);
        
        // Create a temporary div to hold the new slide
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newSlideHtml;
        const newSlide = tempDiv.firstElementChild;
        
        // Add the new slide to the container
        slidesContainer.appendChild(newSlide);
        
        // Add event listener for the remove button
        const removeBtn = newSlide.querySelector('.remove-slide-btn');
        removeBtn.addEventListener('click', function() {
            removeSlide(newSlide);
        });
        
        slideCount++;
        updateSlideNumbers();
        updateRemoveButtons();
        
        // Scroll to the new slide
        newSlide.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Focus on the title input
        const titleInput = newSlide.querySelector('input[name^="slide_title_"]');
        titleInput.focus();
        
        // Replace feather icons
        feather.replace();
    }
    
    function createSlideHtml(index) {
        return `
            <div class="slide-block card mb-3" data-slide-index="${index}">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h6 class="mb-0">Slide ${index + 1}</h6>
                    <button type="button" class="btn btn-sm btn-outline-danger remove-slide-btn">
                        <i data-feather="trash-2"></i>
                    </button>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label">Slide Title <span class="text-danger">*</span></label>
                        <input type="text" class="form-control" name="slide_title_${index}" required maxlength="200" 
                               placeholder="Enter slide title">
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Bullet Points</label>
                        <textarea class="form-control" name="slide_bullets_${index}" rows="4" 
                                  placeholder="Enter bullet points (one per line)&#10;• First point&#10;• Second point&#10;• Third point"></textarea>
                        <div class="form-text">One bullet point per line. Maximum 10 bullets per slide.</div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <label class="form-label">Image URL (optional)</label>
                            <input type="url" class="form-control" name="slide_image_url_${index}" 
                                   placeholder="https://example.com/image.jpg">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Or Upload Image</label>
                            <input type="file" class="form-control" name="slide_image_file_${index}" 
                                   accept="image/png,image/jpeg,image/jpg">
                            <div class="form-text">PNG, JPG, or JPEG format. Max 5MB.</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    function removeSlide(slideElement) {
        // Add removing animation
        slideElement.classList.add('slide-removing');
        
        // Remove after animation
        setTimeout(() => {
            slideElement.remove();
            updateSlideNumbers();
            updateRemoveButtons();
        }, 300);
    }
    
    function updateSlideNumbers() {
        const slides = document.querySelectorAll('.slide-block');
        slides.forEach((slide, index) => {
            // Update slide number in header
            const header = slide.querySelector('.card-header h6');
            header.textContent = `Slide ${index + 1}`;
            
            // Update form field names
            const titleInput = slide.querySelector('input[name^="slide_title_"]');
            const bulletsTextarea = slide.querySelector('textarea[name^="slide_bullets_"]');
            const imageUrlInput = slide.querySelector('input[name^="slide_image_url_"]');
            const imageFileInput = slide.querySelector('input[name^="slide_image_file_"]');
            
            if (titleInput) titleInput.name = `slide_title_${index}`;
            if (bulletsTextarea) bulletsTextarea.name = `slide_bullets_${index}`;
            if (imageUrlInput) imageUrlInput.name = `slide_image_url_${index}`;
            if (imageFileInput) imageFileInput.name = `slide_image_file_${index}`;
            
            // Update data attribute
            slide.setAttribute('data-slide-index', index);
        });
    }
    
    function updateRemoveButtons() {
        const slides = document.querySelectorAll('.slide-block');
        const removeButtons = document.querySelectorAll('.remove-slide-btn');
        
        // Show/hide remove buttons (always show if more than 1 slide)
        removeButtons.forEach(btn => {
            btn.style.display = slides.length > 1 ? 'block' : 'none';
        });
    }
    
    // Add event listeners to existing remove buttons
    document.querySelectorAll('.remove-slide-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const slideBlock = this.closest('.slide-block');
            removeSlide(slideBlock);
        });
    });
    
    // Form validation
    const form = document.getElementById('presentationForm');
    form.addEventListener('submit', function(e) {
        const slides = document.querySelectorAll('.slide-block');
        
        if (slides.length === 0) {
            e.preventDefault();
            alert('Please add at least one slide.');
            return;
        }
        
        // Check that at least one slide has a title
        let hasValidSlide = false;
        slides.forEach(slide => {
            const titleInput = slide.querySelector('input[name^="slide_title_"]');
            if (titleInput && titleInput.value.trim()) {
                hasValidSlide = true;
            }
        });
        
        if (!hasValidSlide) {
            e.preventDefault();
            alert('Please provide a title for at least one slide.');
            return;
        }
    });
    
    // File upload validation
    document.addEventListener('change', function(e) {
        if (e.target.type === 'file' && e.target.accept.includes('image/')) {
            const file = e.target.files[0];
            if (file) {
                // Check file size (5MB limit)
                const maxSize = 5 * 1024 * 1024; // 5MB
                if (file.size > maxSize) {
                    alert('File size must be less than 5MB.');
                    e.target.value = '';
                    return;
                }
                
                // Check file type
                const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Please upload PNG, JPG, or JPEG files only.');
                    e.target.value = '';
                    return;
                }
            }
        }
    });
    
    // Auto-resize textareas
    document.addEventListener('input', function(e) {
        if (e.target.tagName === 'TEXTAREA') {
            e.target.style.height = 'auto';
            e.target.style.height = (e.target.scrollHeight) + 'px';
        }
    });
    
    // Character count for title
    const titleInput = document.getElementById('title');
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            const maxLength = 200;
            const currentLength = this.value.length;
            const formText = this.nextElementSibling;
            
            formText.textContent = `${currentLength}/${maxLength} characters`;
            
            if (currentLength > maxLength * 0.9) {
                formText.classList.add('text-warning');
            } else {
                formText.classList.remove('text-warning');
            }
        });
    }
});
