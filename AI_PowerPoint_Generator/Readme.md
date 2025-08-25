# AI PowerPoint Generator

<div align="center">
  <img src="assets/screenshot.png" alt="AI PowerPoint Generator Demo" width="600"/>
  <br>
  <em>Generate professional PowerPoint presentations with AI-powered content enhancement</em>
</div>

<div align="center">
  
  ![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
  ![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg)
  ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
  
</div>

A Flask web application that generates PowerPoint presentations with AI-enhanced content using Google Gemini.

## Features

- **Simple Web Interface**: Clean, responsive HTML form for creating presentations
- **AI Enhancement**: Use Google Gemini to improve slide content, add speaker notes, and generate additional bullet points
- **Multiple Themes**: Choose from various presentation themes (Default, Dark, Corporate, Modern, Vibrant)
- **Image Support**: Add images via URL upload or get AI-suggested images from Pexels
- **Flexible Content**: Support for multiple slides with customizable titles and bullet points
- **PowerPoint Export**: Generate and download professional .pptx files

## Setup

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key
- (Optional) Pexels API key for image suggestions

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install flask python-pptx google-genai requests python-dotenv pytest
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PEXELS_API_KEY=your_pexels_api_key_here
   SESSION_SECRET=your_session_secret_here
   MAX_UPLOAD_MB=5
   MODEL_NAME=gemini-2.5-pro
   GEMINI_TEMPERATURE=0.4
   ```

4. **Get API Keys**:
   - **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - **Pexels API Key** (optional): Get from [Pexels API](https://www.pexels.com/api/)

## Usage

### Running the Application

```bash
flask --app app run --host 0.0.0.0 --port 5000
```

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Fill in the presentation details:
   - **Title**: Your presentation title
   - **Theme**: Choose from available themes
   - **Slides**: Add slide titles and bullet points
   - **Images**: Add image URLs or use AI-suggested images
3. Click "Generate Presentation" to create your PowerPoint
4. Download the generated .pptx file

## Project Structure

```
AI_PowerPoint_Generator/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── models.py             # Data models
├── routes.py             # Flask routes
├── services/             # Core services
│   ├── gemini.py         # Google Gemini integration
│   ├── ppt_generator.py  # PowerPoint generation
│   ├── images.py         # Image handling
│   ├── themes.py         # Theme management
│   └── validators.py     # Input validation
├── templates/            # HTML templates
├── static/              # CSS and JavaScript
└── tests/               # Test files
```

## API Integration

### Google Gemini
- **Purpose**: Content enhancement and AI-powered suggestions
- **Features**: 
  - Improve slide content
  - Generate additional bullet points
  - Add speaker notes
  - Suggest presentation improvements

### Pexels API (Optional)
- **Purpose**: AI-suggested images for presentations
- **Features**: 
  - Relevant image suggestions based on slide content
  - High-quality stock photos
  - Automatic image integration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Gemini](https://aistudio.google.com/) for AI capabilities
- [Pexels](https://www.pexels.com/) for image suggestions
- [python-pptx](https://python-pptx.readthedocs.io/) for PowerPoint generation
