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

CORE_PROMPT = """Follow the SYSTEM INSTRUCTIONS and SAFETY GUARDRAILS. Use the INPUT SCHEMA values to generate output strictly in the OUTPUT SCHEMA JSON. Do not add commentary.

PRECISE TIMING CALCULATIONS:
- Hindi TTS: 150 words per minute average
- Short (30s): ~75 words | (45s): ~112 words | (60s): ~150 words
- Long (3min): ~450 words | (4min): ~600 words | (5min): ~750 words
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

def generate_hindi_script(input_payload):
    """
    Generate Hindi YouTube script using Gemini API
    """
    try:
        # Construct the complete prompt
        prompt = f"{SYSTEM_INSTRUCTIONS}\n\n{CORE_PROMPT}\n\nINPUT_JSON:\n{json.dumps(input_payload, ensure_ascii=False)}"
        
        # Generate content using Gemini
        response = client.models.generate_content(
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


def humanize_hindi_script(raw_script):
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
        
        # Construct the humanization prompt
        prompt = f"""{humanization_instructions}

{CORE_PROMPT}

Original Raw Script to Humanize:
{raw_script}

Please rewrite this script to sound completely natural and human-like while maintaining the same structure and key information. Focus on making it conversational and authentic."""
        
        # Generate humanized content using Gemini
        response = client.models.generate_content(
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
            
            # Add humanization note
            if "notes" not in result:
                result["notes"] = {}
            result["notes"]["humanized"] = True
            result["notes"]["original_length"] = len(raw_script)
            result["notes"]["processing"] = "Script humanized for natural speech"
            
            return result
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response: {response.text}")
            return {"error": "Invalid JSON response from API"}
        
    except Exception as e:
        logging.error(f"Gemini API error during humanization: {str(e)}")
        return {"error": f"Humanization failed: {str(e)}"}
