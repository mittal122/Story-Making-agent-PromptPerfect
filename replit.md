# Overview

This project is a Hindi YouTube Script Generator web application that creates conversational-investigative Hindi scripts for YouTube content. The application specializes in generating scripts for both Shorts (45-60 seconds) and long-form videos (3-5 minutes) with a focus on sensitive topics like legal cases, using neutral and legally-safe language framing. It integrates with Google's Gemini AI to generate structured content including titles, voice-over scripts, on-screen text, descriptions, and hashtags optimized for text-to-speech and YouTube SEO.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-side rendered architecture with Bootstrap for responsive UI components. The frontend consists of:
- **Template System**: Jinja2 templating with Flask, using a base template layout with Bootstrap dark theme
- **Form-based Interface**: Single-page form for inputting script generation parameters including topic, location, victim role, duration, timeline, and keywords
- **Real-time Feedback**: JavaScript-powered form validation, character counting, and copy-to-clipboard functionality
- **Responsive Design**: Bootstrap-based responsive layout optimized for both desktop and mobile usage

## Backend Architecture
The backend follows a simple Flask-based MVC pattern:
- **Flask Application**: Lightweight web framework with ProxyFix middleware for deployment compatibility
- **Route Handling**: Centralized route management in `routes.py` with JSON and form data support
- **Service Layer**: Dedicated `gemini_service.py` for AI integration and content generation logic
- **Error Handling**: Comprehensive validation for required fields and JSON parsing with graceful fallbacks

## AI Integration Architecture
The application integrates with Google's Gemini AI service through a structured approach:
- **System Instructions**: Pre-defined prompt engineering with safety guardrails for defamation protection and cultural sensitivity
- **Structured Output**: JSON schema enforcement for consistent response formatting
- **Content Safety**: Built-in legal-safe framing using neutral language ("आरोप/दावा" instead of direct accusations)
- **TTS Optimization**: Script formatting optimized for text-to-speech with breath markers and emphasis tags

## Content Generation Pipeline
The system follows a multi-step content generation process:
1. **Input Validation**: Server-side validation of required fields with intelligent parsing of timeline and keyword data
2. **Prompt Construction**: Dynamic prompt building based on duration (short vs long) with specific structural requirements
3. **AI Processing**: Gemini API calls with temperature and safety settings configured for creative yet safe content
4. **Output Formatting**: Structured JSON response containing title, script, on-screen text, description, and hashtags
5. **Client Rendering**: Real-time display of generated content with copy functionality

# External Dependencies

## AI Services
- **Google Gemini API**: Primary AI service for content generation using the `google.genai` client library
- **Model Configuration**: Uses Gemini 2.5 Flash model with specific temperature (0.7) and top_p (0.9) settings for balanced creativity and consistency

## Frontend Libraries
- **Bootstrap 5.3.0**: UI framework with dark theme variant from Replit CDN for consistent styling
- **Font Awesome 6.0.0**: Icon library for enhanced user interface elements
- **Google Fonts**: Noto Sans Devanagari font family for proper Hindi text rendering and readability

## Python Dependencies
- **Flask**: Web application framework for routing and template rendering
- **Werkzeug ProxyFix**: Middleware for handling proxy headers in deployment environments
- **Python Logging**: Built-in logging configuration for debugging and monitoring

## Environment Configuration
- **API Key Management**: Environment variable-based configuration for Gemini API key (`GEMINI_API_KEY`)
- **Session Management**: Configurable session secret key with development fallback
- **Debug Mode**: Development-friendly configuration with detailed error reporting