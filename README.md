# PromptPerfect - Hindi Script Generator

A full-stack web application that generates and humanizes Hindi scripts for YouTube content using AI. Built with Flask (Python) backend and React frontend, optimized for deployment on Vercel.

## Features

- **Script Generation**: Create new Hindi scripts based on topics and genres
- **Script Humanization**: Transform existing scripts into natural, human-like narration
- **YouTube Optimization**: Scripts are optimized for YouTube algorithm and engagement
- **Multiple Genres**: Support for mysterious, thriller, investigative, motivational, and more
- **Flexible Duration**: Generate scripts for 30 seconds to 10 minutes
- **Custom API Keys**: Support for custom Gemini API keys

## Tech Stack

- **Backend**: Flask (Python), Google Gemini AI API
- **Frontend**: React, Bootstrap, Font Awesome
- **Deployment**: Vercel (Serverless Functions)

## Project Structure

```
PromptPerfect/
├── api/
│   ├── index.py              # Main Flask API endpoint
│   ├── gemini_service.py     # Gemini AI service functions
│   └── requirements.txt      # Python dependencies
├── frontend/frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styles
│   │   └── main.jsx         # Entry point
│   ├── index.html           # HTML template
│   └── package.json         # Node.js dependencies
├── vercel.json              # Vercel configuration
└── README.md               # This file
```

## Deployment on Vercel

### Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Gemini API Key**: Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Step 1: Clone and Setup

```bash
# Clone your repository
git clone <your-repo-url>
cd PromptPerfect

# Install frontend dependencies
cd frontend/frontend
npm install
cd ../..
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No
# - Project name: promptperfect (or your choice)
# - In which directory is your code? ./
# - Auto-detected settings? Yes
```

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your Git repository
4. Vercel will auto-detect the settings from `vercel.json`
5. Click "Deploy"

### Step 3: Environment Variables

After deployment, add environment variables in Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```
GEMINI_API_KEY=your_gemini_api_key_here
SESSION_SECRET=your_random_session_secret_here
```

### Step 4: Update Domain (Optional)

1. Go to your project settings
2. Navigate to "Domains"
3. Add your custom domain if desired

## Local Development

### Backend Setup

```bash
# Install Python dependencies
cd api
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_gemini_api_key
export SESSION_SECRET=your_session_secret

# Run Flask development server
python index.py
```

### Frontend Setup

```bash
# Install and run React development server
cd frontend/frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and will proxy API requests to the backend.

## API Endpoints

### POST /api/generate

Generates or humanizes Hindi scripts.

**Request Body:**
```json
{
  "mode": "generate",  // or "humanize"
  "topic": "Your topic here",
  "genre": "mysterious",
  "description": "Optional description",
  "duration_seconds": 45,
  "api_key": "optional_custom_api_key"
}
```

**Response:**
```json
{
  "title": "Generated title",
  "vo_script": "Hindi script content",
  "on_screen_text": ["Text", "overlays"],
  "description": "YouTube description",
  "hashtags": ["#tag1", "#tag2"],
  "notes": {
    "word_count": 112,
    "duration_seconds": 45
  }
}
```

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "PromptPerfect API is running"
}
```

## Configuration Files

### vercel.json

Configures Vercel deployment:
- Python serverless functions for API
- Static build for React frontend
- Route configuration
- Build settings

### package.json (Frontend)

React application with Vite build tool:
- Development server with HMR
- Production build optimization
- ESLint for code quality

### requirements.txt (API)

Python dependencies:
- Flask for web framework
- google-generativeai for AI integration

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI generation | Yes |
| `SESSION_SECRET` | Secret key for Flask sessions | Yes |

## Troubleshooting

### Common Issues

1. **API Errors**: Ensure `GEMINI_API_KEY` is set correctly
2. **Build Failures**: Check that all dependencies are listed in `requirements.txt` and `package.json`
3. **CORS Issues**: API routes are configured to accept requests from the frontend domain
4. **Function Timeout**: Large scripts may take time to generate; consider increasing timeout in Vercel settings

### Logs

View deployment and runtime logs in the Vercel dashboard under the "Functions" tab.

## Support

For issues and questions:
1. Check the Vercel deployment logs
2. Verify environment variables are set correctly
3. Ensure your Gemini API key has sufficient quota
4. Check that the API endpoints are responding at `/api/health`

## License

This project is open source and available under the MIT License.
