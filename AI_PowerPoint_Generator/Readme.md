# AI PowerPoint Generator

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
