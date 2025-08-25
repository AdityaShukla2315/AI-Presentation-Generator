"""PowerPoint presentation themes"""

THEMES = {
    'default': {
        'name': 'Default',
        'font_name': 'Arial',
        'title_color': '#2c3e50',
        'body_color': '#34495e',
        'background_color': '#ffffff',
        'accent_color': '#3498db'
    },
    'dark': {
        'name': 'Dark',
        'font_name': 'Calibri',
        'title_color': '#ecf0f1',
        'body_color': '#bdc3c7',
        'background_color': '#2c3e50',
        'accent_color': '#e74c3c'
    },
    'corporate': {
        'name': 'Corporate',
        'font_name': 'Times New Roman',
        'title_color': '#1a365d',
        'body_color': '#2d3748',
        'background_color': '#f7fafc',
        'accent_color': '#2b6cb0'
    },
    'modern': {
        'name': 'Modern',
        'font_name': 'Segoe UI',
        'title_color': '#1a202c',
        'body_color': '#4a5568',
        'background_color': '#ffffff',
        'accent_color': '#9f7aea'
    },
    'vibrant': {
        'name': 'Vibrant',
        'font_name': 'Arial',
        'title_color': '#742a2a',
        'body_color': '#2d3748',
        'background_color': '#fffaf0',
        'accent_color': '#ed8936'
    }
}

def get_available_themes():
    """Return list of available themes"""
    return [{'key': key, 'name': theme['name']} for key, theme in THEMES.items()]

def get_theme(theme_name: str):
    """Get theme by name, fallback to default"""
    return THEMES.get(theme_name, THEMES['default'])
