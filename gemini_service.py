import json
import logging
import os
from google import genai
from google.genai import types

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# System instructions optimized for YouTube algorithm and precise timing
SYSTEM_INSTRUCTIONS = """You are "Hindi YouTube Script Agent," specialized in creating viral, algorithm-optimized Hindi scripts for YouTube Shorts and videos. Always:
- Keep language simple, spoken Hindi with short lines optimized for engagement
- Use neutral/legal‑safe framing: prefer "आरोप/दावा/कहा जा रहा है" vs direct blame
- Optimize for TTS: short clauses; ellipses (…) for breath; em dashes (—) for emphasis; optional tags [pause] [soft] [emphasis] used sparingly
- Generate content that fits EXACT timing requirements (calculate words per minute for precise duration)
- Output exactly in the required JSON schema and nothing else
- Focus on YouTube algorithm optimization for maximum reach and engagement

YOUTUBE ALGORITHM OPTIMIZATION:
- Titles: Hook-first, trending keywords, emotional triggers, under 60 characters for mobile
- Descriptions: First 125 characters crucial for search ranking, include main keywords
- Hashtags: Mix trending (#Viral, #YouTubeShorts) with niche tags, 15-30 total
- Content: Create curiosity gaps, cliffhangers, and engagement hooks every 3-5 seconds
- Timing: Precise word count calculations (150 WPM for Hindi TTS)

SAFETY AND STYLE GUARDRAILS (always enforce):
- Defamation safety: no definitive guilt; frame as "परिवार का आरोप/आधिकारिक दावा"
- Political safety: avoid advocacy; stick to narrative and questions
- Sensitive events: avoid graphic detail; keep compassionate tone
- Respect cultural/religious sentiments
- Check length limits strictly; avoid run‑on sentences
- Do not include external URLs
- Titles optimized for CTR and SEO
- Descriptions formatted for YouTube algorithm
- Hashtags researched for trending topics"""

# Genre-specific storytelling guidelines
GENRE_GUIDELINES = {
    "mysterious": "Create suspense and intrigue with unanswered questions, dramatic pauses, and revelation techniques. Use phrases like 'क्या होगा अगर...', 'रहस्य ये है', 'सच क्या है?'",
    "motivational": "Use inspiring language, success stories, and emotional appeals. Include phrases like 'आप भी कर सकते हैं', 'सफलता की कहानी', 'सपने पूरे होते हैं'",
    "thriller": "Build tension with quick pacing, shocking reveals, and cliffhangers. Use dramatic phrases like 'अचानक', 'शॉकिंग सच', 'ये तो सिर्फ शुरुआत थी'",
    "educational": "Clear explanations, step-by-step breakdowns, and learning points. Use phrases like 'आइए जानते हैं', 'समझिए', 'इससे क्या सीख?'",
    "investigative": "Fact-based narrative with evidence and analysis. Use neutral framing like 'आरोप है', 'दावा किया गया', 'जांच जारी'",
    "inspirational": "Uplifting stories with emotional connection and hope. Use phrases like 'प्रेरणादायक', 'उम्मीद की किरण', 'जीवन बदल गया'",
    "dramatic": "High emotion, conflict, and resolution. Use expressive language with dramatic emphasis and emotional peaks",
    "informative": "Clear, factual presentation with organized information and practical insights"
}

CORE_PROMPT = """Follow the SYSTEM INSTRUCTIONS and SAFETY GUARDRAILS. Use the INPUT SCHEMA values to generate output strictly in the OUTPUT SCHEMA JSON. Do not add commentary.

PRECISE TIMING CALCULATIONS:
- Hindi TTS: 150 words per minute average
- Short (30s): ~75 words | (45s): ~112 words | (60s): ~150 words
- Medium (2min): ~300 words | (3min): ~450 words
- Long (5min): ~750 words | (10min): ~1500 words
- Include pauses and emphasis in word count

YOUTUBE ALGORITHM OPTIMIZATION STEPS:
1) Validate inputs and calculate exact word count for specified duration
2) Title optimization: Start with emotional hook + trending keywords + curiosity gap (50-60 chars)
3) Description optimization: 
   - First line: Main keywords + emotional hook
   - Second line: Conflict/mystery statement
   - Bullet points with timestamps
   - Call-to-action for engagement
   - Related keywords for SEO
4) Hashtag strategy: 15-30 tags mixing:
   - Trending: #Viral #YouTubeShorts #Trending
   - Category: #Hindi #News #Investigation #Crime #Justice
   - Niche: Topic-specific tags
   - Location-based tags
5) Content structure:
   - First 3 seconds: Strong hook question
   - Every 5-7 seconds: Engagement point or cliffhanger
   - Last 3 seconds: Strong CTA for likes/shares
6) On-screen text: Short, punchy phrases that complement audio
7) Return optimized JSON for maximum YouTube reach

CONTENT STRUCTURE BY DURATION:
- 30s: Hook(3s) → Setup(7s) → Twist(10s) → Revelation(7s) → CTA(3s)
- 45s: Hook(5s) → Setup(10s) → Timeline(15s) → Conflict(10s) → CTA(5s)
- 60s: Hook(5s) → Setup(12s) → Timeline(20s) → Evidence(18s) → CTA(5s)
- 3-5min: Full investigative arc with detailed timeline and analysis

OUTPUT SCHEMA (optimized for YouTube algorithm):
{
  "title": "string <=60 chars, hook-first with trending keywords",
  "vo_script": "string; exact word count for specified duration; TTS-optimized with engagement hooks",
  "on_screen_text": ["5-8 punchy phrases, 2-3 words each"],
  "description": "YouTube-optimized description with keywords in first 125 chars, timestamps, hashtags, and CTA",
  "hashtags": ["15-30 trending and niche tags for maximum reach"],
  "youtube_tags": ["additional SEO tags for YouTube backend"],
  "notes": {
    "exact_duration_seconds": "calculated timing",
    "word_count": "precise count for TTS",
    "engagement_hooks": "hooks per 5-second intervals",
    "algorithm_score": "optimization rating"
  }
}"""

def generate_hindi_script(input_payload, custom_api_key=None):
    """
    Generate Hindi YouTube script using Gemini API with genre-based storytelling
    """
    try:
        # Extract content details
        content = input_payload.get('content', {})
        generation = input_payload.get('generation', {})
        
        topic = content.get('topic', '')
        genre = content.get('genre', 'informative')
        description = content.get('description', '')
        duration_seconds = generation.get('duration_seconds', 45)
        
        # Get genre-specific guidelines
        genre_guidance = GENRE_GUIDELINES.get(genre, GENRE_GUIDELINES['informative'])
        
        # Calculate target word count
        target_words = int((duration_seconds / 60) * 150)
        
        # Construct genre-specific prompt
        prompt = f"""{SYSTEM_INSTRUCTIONS}

{CORE_PROMPT}

GENRE-SPECIFIC GUIDELINES:
{genre_guidance}

SCRIPT REQUIREMENTS:
- Topic: {topic}
- Genre: {genre.title()}
- Duration: {duration_seconds} seconds (approximately {target_words} words)
- Description: {description if description else 'Generate creatively based on topic and genre'}
- Language: Hindi (conversational and engaging)
- Format: YouTube-optimized for maximum reach

CREATE A COMPELLING {genre.upper()} SCRIPT:
1. Hook viewers in first 3 seconds with genre-appropriate opening
2. Develop story using {genre} storytelling techniques
3. Maintain engagement with genre-specific language and pacing
4. Include natural transitions and emotional connection
5. End with strong call-to-action
6. Ensure exact timing: {duration_seconds} seconds = ~{target_words} words

Generate a complete script following the OUTPUT SCHEMA."""
        
        # Use custom API key if provided
        api_client = client
        if custom_api_key:
            api_client = genai.Client(api_key=custom_api_key)
        
        # Generate content using Gemini
        response = api_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.9,
                response_mime_type="application/json"
            )
        )
        
        if not response.text:
            return {"error": "Empty response from Gemini API"}
        
        # Parse the JSON response
        try:
            result = json.loads(response.text)
            
            # Validate required fields in response
            required_fields = ["title", "vo_script", "on_screen_text", "description", "hashtags"]
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                logging.warning(f"Response missing fields: {missing_fields}")
                return {"error": f"Invalid response format: missing {missing_fields}"}
            
            # Validate title length
            if len(result.get("title", "")) > 65:
                result["title"] = result["title"][:62] + "..."
            
            return result
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response: {response.text}")
            return {"error": "Invalid JSON response from API"}
        
    except Exception as e:
        logging.error(f"Gemini API error: {str(e)}")
        return {"error": f"API call failed: {str(e)}"}


def humanize_hindi_script(raw_script, duration_seconds=45, custom_api_key=None):
    """
    Humanize an existing Hindi script to make it sound more natural and conversational
    """
    try:
        # System instructions for humanization
        humanization_instructions = """You are a Hindi script humanization expert. Your task is to take a raw or AI-generated Hindi script and rewrite it to sound completely natural, as if a human is actually speaking it.

Key principles:
- Make it sound conversational and natural
- Use simple, everyday Hindi words that people actually speak
- Add natural speech patterns, pauses, and emotional inflections
- Keep the core message and facts intact
- Use TTS-friendly formatting with ellipses (...) for natural pauses
- Add emphasis with em dashes (—) where appropriate
- Make it feel like a real person telling a story, not reading from a script
- Remove any robotic or AI-sounding language
- Add natural transitions and conversational connectors
- Ensure it flows smoothly when spoken aloud

Output the same JSON format with humanized content:"""
        
        # Calculate target word count based on duration
        target_words = int((duration_seconds / 60) * 150)  # 150 WPM for Hindi TTS
        
        # Construct the humanization prompt with timing
        prompt = f"""{humanization_instructions}

{CORE_PROMPT}

Target Duration: {duration_seconds} seconds (approximately {target_words} words)

Original Raw Script to Humanize:
{raw_script}

Please rewrite this script to:
1. Sound completely natural and human-like
2. Fit exactly {duration_seconds} seconds when spoken (around {target_words} words)
3. Maintain the core message while making it conversational
4. Add proper pacing with natural pauses and emphasis
5. Use engaging storytelling techniques appropriate for the content"""
        
        # Use custom API key if provided
        api_client = client
        if custom_api_key:
            api_client = genai.Client(api_key=custom_api_key)
            
        # Generate humanized content using Gemini
        response = api_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,  # Slightly higher for more creative humanization
                top_p=0.9,
                response_mime_type="application/json"
            )
        )
        
        if not response.text:
            return {"error": "Empty response from Gemini API"}
        
        # Parse the JSON response
        try:
            result = json.loads(response.text)
            
            # Validate required fields in response
            required_fields = ["title", "vo_script", "on_screen_text", "description", "hashtags"]
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                logging.warning(f"Response missing fields: {missing_fields}")
                return {"error": f"Invalid response format: missing {missing_fields}"}
            
            # Validate title length
            if len(result.get("title", "")) > 65:
                result["title"] = result["title"][:62] + "..."
            
            # Add processing notes
            if "notes" not in result:
                result["notes"] = {}
            
            # Add humanization-specific notes
            result["notes"]["humanized"] = True
            result["notes"]["original_length"] = len(raw_script)
            result["notes"]["target_duration"] = f"{duration_seconds} seconds"
            result["notes"]["processing"] = "Script humanized for natural speech"
            
            return result
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response: {response.text}")
            return {"error": "Invalid JSON response from API"}
        
    except Exception as e:
        logging.error(f"Gemini API error during humanization: {str(e)}")
        return {"error": f"Humanization failed: {str(e)}"}
