import os
import logging
import tempfile
import requests
from typing import List, Optional

def get_image_suggestions(keywords: List[str]) -> Optional[str]:
    """
    Get image suggestions from Pexels API based on keywords
    
    Args:
        keywords: List of keywords to search for
        
    Returns:
        Image URL or None if not found
    """
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        logging.warning("Pexels API key not provided, skipping image suggestions")
        return None
    
    if not keywords:
        return None
    
    # Use first few keywords for search
    search_query = " ".join(keywords[:3])
    
    try:
        headers = {
            "Authorization": api_key
        }
        
        params = {
            "query": search_query,
            "per_page": 1,
            "orientation": "landscape"
        }
        
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            
            if photos:
                # Get medium size image URL
                photo = photos[0]
                return photo.get("src", {}).get("medium", photo.get("src", {}).get("original"))
        
        logging.warning(f"Pexels API returned status {response.status_code}")
        return None
        
    except Exception as e:
        logging.error(f"Error fetching image from Pexels: {e}")
        return None

def download_image(image_url: str) -> Optional[str]:
    """
    Download image from URL to temporary file
    
    Args:
        image_url: URL of the image to download
        
    Returns:
        Path to downloaded file or None if failed
    """
    try:
        response = requests.get(image_url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            logging.error(f"Invalid content type: {content_type}")
            return None
        
        # Determine file extension
        if 'jpeg' in content_type or 'jpg' in content_type:
            extension = '.jpg'
        elif 'png' in content_type:
            extension = '.png'
        elif 'gif' in content_type:
            extension = '.gif'
        else:
            extension = '.jpg'  # Default fallback
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
        
        # Download in chunks
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                temp_file.write(chunk)
        
        temp_file.close()
        
        # Verify file size (max 10MB)
        file_size = os.path.getsize(temp_file.name)
        if file_size > 10 * 1024 * 1024:
            os.remove(temp_file.name)
            logging.error("Downloaded image too large")
            return None
        
        return temp_file.name
        
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return None

def validate_image_url(url: str) -> bool:
    """
    Validate if URL points to a valid image
    
    Args:
        url: Image URL to validate
        
    Returns:
        True if valid image URL, False otherwise
    """
    try:
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return False
        
        # Check if URL ends with image extension
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        url_lower = url.lower()
        
        # Check extension or make HEAD request
        if any(url_lower.endswith(ext) for ext in image_extensions):
            return True
        
        # Make HEAD request to check content type
        response = requests.head(url, timeout=10)
        content_type = response.headers.get('content-type', '')
        
        return content_type.startswith('image/')
        
    except Exception:
        return False
