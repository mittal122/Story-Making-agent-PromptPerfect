import json
import logging
import os
import google.generativeai as genai
import json
import logging
import os
import google.generativeai as genai
from google.generativeai import types

# Initialize Gemini client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# System instructions optimized for storytelling and content creation
SYSTEM_INSTRUCTIONS = """You are an advanced storytelling and content creation agent specialized in transforming raw subtitles or draft text into highly engaging YouTube Shorts scripts.
Your goal is to make the output look original, professional, and optimized for maximum audience retention and discoverability.

CORE PRINCIPLES:
- Transform raw input into compelling short-form story scripts using advanced storytelling techniques
- Hook viewers in the first few seconds with immediate attention-grabbing content
- Create curiosity gaps & suspense to keep viewers watching until the end
- Build relatability by connecting with audience emotions and real-life situations
- Ensure clear progression: beginning → conflict/problem → resolution/insight
- Deliver concise but powerful content where every word adds value
- End with call-to-thought that leaves viewers with something thought-provoking
- Make final scripts feel completely original, not copied from input text

STORYTELLING TECHNIQUES:
- Use conversational, emotionally engaging language that feels natural
- Prioritize clarity + impact in every sentence
- Avoid robotic or repetitive phrasing
- Maintain originality – outputs should look crafted, not AI-generated
- Structure content to retain attention until the very end
- Optimize pacing for short-form content (30–60 seconds)
- Include natural emotional beats and rhythm"""

# Genre-specific storytelling guidelines for both languages
GENRE_GUIDELINES = {
    "mysterious": {
        "english": "Create suspense and intrigue with unanswered questions, dramatic pauses, and revelation techniques. Use phrases like 'But what if...', 'The mystery is', 'What's the truth?', 'Here's what nobody tells you'",
        "hindi": "रहस्य और उत्सुकता पैदा करें अनुत्तरित सवालों, नाटकीय रुकावटों और खुलासे की तकनीकों के साथ। वाक्य प्रयोग करें जैसे 'लेकिन क्या होगा अगर...', 'रहस्य यह है', 'सच्चाई क्या है?', 'यहाँ है जो कोई नहीं बताता'"
    },
    "motivational": {
        "english": "Use inspiring language, success stories, and emotional appeals. Include phrases like 'You can do this too', 'Success story that will inspire you', 'Dreams do come true', 'This will change your perspective'",
        "hindi": "प्रेरणादायक भाषा, सफलता की कहानियां और भावनात्मक अपील का उपयोग करें। वाक्य शामिल करें जैसे 'आप भी कर सकते हैं', 'सफलता की कहानी जो आपको प्रेरित करेगी', 'सपने सच होते हैं', 'यह आपका नजरिया बदल देगा'"
    },
    "thriller": {
        "english": "Build tension with quick pacing, shocking reveals, and cliffhangers. Use dramatic phrases like 'Suddenly everything changed', 'The shocking truth', 'This was just the beginning', 'You won't believe what happened next'",
        "hindi": "तेज़ गति, चौंकाने वाले खुलासे और रोमांचक मोड़ों के साथ तनाव बनाएं। नाटकीय वाक्य प्रयोग करें जैसे 'अचानक सब कुछ बदल गया', 'चौंकाने वाली सच्चाई', 'यह तो बस शुरुआत थी', 'आप विश्वास नहीं करेंगे कि आगे क्या हुआ'"
    },
    "educational": {
        "english": "Clear explanations, step-by-step breakdowns, and learning points. Use phrases like 'Here's what you need to know', 'Let me break this down', 'The lesson here is', 'This will blow your mind'",
        "hindi": "स्पष्ट व्याख्या, चरणबद्ध विवरण और सीखने के बिंदु। वाक्य प्रयोग करें जैसे 'यहाँ है जो आपको जानना चाहिए', 'मैं इसे समझाता हूँ', 'यहाँ सबक यह है', 'यह आपका दिमाग हिला देगा'"
    },
    "investigative": {
        "english": "Fact-based narrative with evidence and analysis. Use neutral framing like 'According to reports', 'Evidence suggests', 'Investigation reveals', 'The facts show'",
        "hindi": "तथ्य-आधारित कथा साक्ष्य और विश्लेषण के साथ। तटस्थ फ्रेमिंग का प्रयोग करें जैसे 'रिपोर्ट्स के अनुसार', 'सबूत सुझाते हैं', 'जांच में पता चला', 'तथ्य दिखाते हैं'"
    },
    "inspirational": {
        "english": "Uplifting stories with emotional connection and hope. Use phrases like 'This will inspire you', 'A ray of hope', 'Life-changing moment', 'Against all odds'",
        "hindi": "उत्थानकारी कहानियां भावनात्मक जुड़ाव और आशा के साथ। वाक्य प्रयोग करें जैसे 'यह आपको प्रेरित करेगा', 'उम्मीद की किरण', 'जीवन बदलने वाला पल', 'हर मुश्किल के बावजूद'"
    },
    "dramatic": {
        "english": "High emotion, conflict, and resolution. Use expressive language with dramatic emphasis and emotional peaks. Focus on human drama and emotional storytelling",
        "hindi": "उच्च भावना, संघर्ष और समाधान। नाटकीय जोर और भावनात्मक चरम के साथ अभिव्यंजक भाषा का उपयोग। मानवीय नाटक और भावनात्मक कहानी सुनाने पर ध्यान दें"
    },
    "comedy": {
        "english": "Light-hearted, humorous content with funny situations and relatable jokes. Use phrases like 'You won't stop laughing', 'This is hilarious', 'Comedy gold', 'Too funny to miss'",
        "hindi": "हल्की-फुल्की, हास्यपूर्ण सामग्री मजेदार स्थितियों और संबंधित चुटकुलों के साथ। वाक्य प्रयोग करें जैसे 'आप हंसना नहीं रोक पाएंगे', 'यह बहुत मजेदार है', 'कॉमेडी गोल्ड', 'मिस करने के लिए बहुत मजेदार'"
    },
    "love": {
        "english": "Romantic, emotional stories with heartfelt moments and relationship dynamics. Use phrases like 'Love story that touches hearts', 'Emotional moments', 'Romance at its best', 'This will make you cry'",
        "hindi": "रोमांटिक, भावनात्मक कहानियां दिल छूने वाले पलों और रिश्तों की गतिशीलता के साथ। वाक्य प्रयोग करें जैसे 'प्रेम कहानी जो दिल छूती है', 'भावनात्मक पल', 'रोमांस अपने चरम पर', 'यह आपको रुला देगा'"
    },
    "informative": {
        "english": "Clear, factual presentation with organized information and practical insights that add real value to viewers' lives",
        "hindi": "स्पष्ट, तथ्यपरक प्रस्तुति व्यवस्थित जानकारी और व्यावहारिक अंतर्दृष्टि के साथ जो दर्शकों के जीवन में वास्तविक मूल्य जोड़ती है"
    }
}

# Language-specific configurations
LANGUAGE_CONFIG = {
    "english": {
        "name": "English",
        "words_per_minute": 150,
        "natural_phrases": ["You know what?", "Here's the thing", "But wait", "And then", "What happened next?"],
        "system_prompt_addition": "Generate content in clear, conversational English that sounds natural when spoken aloud."
    },
    "hindi": {
        "name": "हिंदी",
        "words_per_minute": 130,  # Slightly slower for Hindi pronunciation
        "natural_phrases": ["आप जानते हैं क्या?", "बात यह है", "लेकिन रुकिए", "और फिर", "आगे क्या हुआ?"],
        "system_prompt_addition": "सामग्री को स्पष्ट, बातचीत के अंदाज़ में हिंदी में बनाएं जो बोलने पर प्राकृतिक लगे। देवनागरी लिपि का उपयोग करें और सरल शब्दों को प्राथमिकता दें।"
    }
}

CORE_PROMPT = """Follow the SYSTEM INSTRUCTIONS for storytelling and content creation. Take the raw subtitle text (input) as base material and transform it into professional short-form story scripts.

For each input, you must generate the following:

STORY SCRIPT (3 variations):
- Written in compelling, conversational style
- Structured to retain attention until the very end
- Optimized for short-form pacing (30–60 seconds)
- Hook in first few seconds (grab immediate attention)
- Curiosity gaps & suspense to keep viewers watching
- Relatability (connect with audience emotions)
- Clear progression (beginning → conflict → resolution)
- Concise but powerful delivery (every word adds value)
- Call-to-thought (thought-provoking ending)

VIDEO TITLE (3 variations):
- Click-worthy and curiosity-driven
- Includes relevant keywords for better ranking
- Short (max 70 characters)
- Emotional triggers and hooks

DESCRIPTION (3 variations):
- Engaging and SEO-friendly
- Includes relevant hashtags and keywords
- Highlights core message/value of video
- Encourages interaction (likes, comments, shares)
- First 125 characters optimized for search

TAGS (at least 10 per variation):
- SEO-optimized, relevant to the story
- Combination of broad and niche keywords
- Helps video reach the right audience
- Mix of trending and topic-specific tags

TIMING CALCULATIONS:
- English narration: 150-160 words per minute average
- 30 seconds: ~75-80 words
- 45 seconds: ~112-120 words  
- 60 seconds: ~150-160 words

OUTPUT REQUIREMENTS:
- Always prioritize clarity + impact
- Avoid robotic or repetitive phrasing
- Maintain originality – outputs should look crafted, not AI-generated
- Use natural, emotionally engaging language
- Ensure the final script feels original and not copied from input

OUTPUT SCHEMA:
{
  "story_scripts": [
    {
      "version": 1,
      "script": "Compelling story script text",
      "word_count": 120,
      "estimated_duration": "45 seconds"
    },
    {
      "version": 2, 
      "script": "Alternative story script text",
      "word_count": 125,
      "estimated_duration": "47 seconds"
    },
    {
      "version": 3,
      "script": "Third story script variation",
      "word_count": 115,
      "estimated_duration": "43 seconds"
    }
  ],
  "video_titles": [
    "First title variation (max 70 chars)",
    "Second title variation (max 70 chars)", 
    "Third title variation (max 70 chars)"
  ],
  "descriptions": [
    "First description variation with SEO optimization",
    "Second description with different angle",
    "Third description focusing on engagement"
  ],
  "tags": [
    ["tag1", "tag2", "tag3", "etc - at least 10 tags"],
    ["different", "tag", "set", "for variation 2"],
    ["third", "tag", "variation", "set"]
  ]
}"""

def generate_story_script(input_payload, custom_api_key=None, language="english"):
    """
    Generate YouTube Shorts script using Gemini API with storytelling techniques
    
    Args:
        input_payload: Dictionary containing content details
        custom_api_key: Optional custom API key
        language: Language preference ("english" or "hindi")
    """
    try:
        # Validate language parameter
        if language not in LANGUAGE_CONFIG:
            return {"error": f"Unsupported language: {language}. Supported languages: {list(LANGUAGE_CONFIG.keys())}"}
        
        # Extract content details
        content = input_payload.get('content', {})
        generation = input_payload.get('generation', {})
        
        topic = content.get('topic', '')
        genre = content.get('genre', 'informative')
        description = content.get('description', '')
        duration_seconds = generation.get('duration_seconds', 45)
        
        # Get language configuration
        lang_config = LANGUAGE_CONFIG[language]
        words_per_minute = lang_config["words_per_minute"]
        
        # Get genre-specific guidelines for the selected language
        genre_guidance = GENRE_GUIDELINES.get(genre, GENRE_GUIDELINES['informative'])
        if isinstance(genre_guidance, dict):
            genre_guidance = genre_guidance.get(language, genre_guidance.get('english', ''))
        
        # Calculate target word count based on language
        target_words = int((duration_seconds / 60) * words_per_minute)
        
        # Construct storytelling prompt with language-specific instructions
        prompt = f"""{SYSTEM_INSTRUCTIONS}

LANGUAGE REQUIREMENTS:
{lang_config["system_prompt_addition"]}

{CORE_PROMPT}

GENRE-SPECIFIC GUIDELINES ({lang_config["name"]}):
{genre_guidance}

LANGUAGE SETTINGS:
- Target Language: {lang_config["name"]}
- Speaking Rate: {words_per_minute} words per minute
- Natural Phrases: {', '.join(lang_config["natural_phrases"])}

INPUT CONTENT TO TRANSFORM:
- Topic/Raw Content: {topic}
- Genre: {genre.title()}
- Target Duration: {duration_seconds} seconds (approximately {target_words} words)
- Additional Context: {description if description else 'Transform creatively using storytelling techniques'}
- Language: {lang_config["name"]} (conversational and engaging)
- Format: YouTube Shorts optimized for maximum engagement

TRANSFORM THIS CONTENT INTO COMPELLING STORYTELLING:
1. Hook viewers immediately with attention-grabbing opening
2. Apply {genre} storytelling techniques throughout
3. Create curiosity gaps and emotional connection
4. Build clear story progression (beginning → conflict → resolution)
5. End with thought-provoking conclusion
6. Target timing: {duration_seconds} seconds = ~{target_words} words

Generate 3 variations following the OUTPUT SCHEMA with story scripts, titles, descriptions, and tags."""
        
        # Use custom API key if provided
        if custom_api_key:
            genai.configure(api_key=custom_api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=types.GenerationConfig(
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
            
            # Validate required fields in response for new storytelling format
            required_fields = ["story_scripts", "video_titles", "descriptions", "tags"]
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                logging.warning(f"Response missing fields: {missing_fields}")
                return {"error": f"Invalid response format: missing {missing_fields}"}
            
            # Validate that we have variations
            if not isinstance(result.get("story_scripts"), list) or len(result["story_scripts"]) == 0:
                return {"error": "No story script variations generated"}
            
            if not isinstance(result.get("video_titles"), list) or len(result["video_titles"]) == 0:
                return {"error": "No video title variations generated"}
            
            # Validate title lengths (max 70 characters)
            for i, title in enumerate(result.get("video_titles", [])):
                if len(title) > 70:
                    result["video_titles"][i] = title[:67] + "..."
            
            # Convert new format to old format for backward compatibility
            # Take the first variation as the primary result
            converted_result = {
                "title": result["video_titles"][0] if result.get("video_titles") else "",
                "vo_script": result["story_scripts"][0]["script"] if result.get("story_scripts") and len(result["story_scripts"]) > 0 else "",
                "on_screen_text": [],  # Will be derived from script content
                "description": result["descriptions"][0] if result.get("descriptions") else "",
                "hashtags": result["tags"][0] if result.get("tags") else [],
                "notes": {
                    "word_count": result["story_scripts"][0].get("word_count", 0) if result.get("story_scripts") and len(result["story_scripts"]) > 0 else 0,
                    "duration_seconds": result["story_scripts"][0].get("estimated_duration", "45 seconds") if result.get("story_scripts") and len(result["story_scripts"]) > 0 else "45 seconds",
                    "variations_available": {
                        "story_scripts": len(result.get("story_scripts", [])),
                        "video_titles": len(result.get("video_titles", [])),
                        "descriptions": len(result.get("descriptions", [])),
                        "tag_sets": len(result.get("tags", []))
                    },
                    "full_response": result  # Include full response for advanced users
                }
            }
            
            # Generate on-screen text from script content (extract key phrases)
            if converted_result["vo_script"]:
                script_sentences = converted_result["vo_script"].split('. ')[:5]  # Take first 5 sentences
                converted_result["on_screen_text"] = [sentence.split()[:3] for sentence in script_sentences if sentence.strip()]
                converted_result["on_screen_text"] = [' '.join(words) + '...' for words in converted_result["on_screen_text"] if words]
            
            return converted_result
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response: {response.text}")
            return {"error": "Invalid JSON response from API"}
        
    except Exception as e:
        logging.error(f"Gemini API error: {str(e)}")
        return {"error": f"API call failed: {str(e)}"}


def humanize_story_script(raw_script, duration_seconds=45, custom_api_key=None, language="english"):
    """
    Humanize an existing script to make it sound more natural and engaging for storytelling
    
    Args:
        raw_script: The raw script text to humanize
        duration_seconds: Target duration in seconds
        custom_api_key: Optional custom API key
        language: Language preference ("english" or "hindi")
    """
    try:
        # Validate language parameter
        if language not in LANGUAGE_CONFIG:
            return {"error": f"Unsupported language: {language}. Supported languages: {list(LANGUAGE_CONFIG.keys())}"}
        
        # Get language configuration
        lang_config = LANGUAGE_CONFIG[language]
        words_per_minute = lang_config["words_per_minute"]
        
        # System instructions for humanization with language support
        humanization_instructions = f"""You are a storytelling script humanization expert. Your task is to take raw subtitle text or draft content and transform it into a compelling, natural-sounding story script optimized for YouTube Shorts in {lang_config["name"]}.

Key principles:
- Transform the content using advanced storytelling techniques
- Make it sound conversational and engaging in {lang_config["name"]}
- Use simple, everyday language that people actually connect with
- Add natural speech patterns, pauses, and emotional inflections
- Keep the core message and facts intact but make them compelling
- Add storytelling elements: hooks, curiosity gaps, emotional beats
- Remove any robotic or AI-sounding language
- Add natural transitions and conversational connectors
- Ensure it flows smoothly when spoken aloud and keeps viewers engaged
- Create clear progression: beginning → conflict/problem → resolution/insight
- End with thought-provoking conclusion that encourages engagement
- Use {lang_config["name"]} natural phrases and expressions

{lang_config["system_prompt_addition"]}

Output the same JSON format with humanized content:"""

        # Calculate target word count based on duration
        target_words = int((duration_seconds / 60) * words_per_minute)
        
        # Construct the humanization prompt with timing
        prompt = f"""{humanization_instructions}

{CORE_PROMPT}

Target Duration: {duration_seconds} seconds (approximately {target_words} words)

Original Raw Content to Transform:
{raw_script}

Please transform this content to:
1. Sound completely natural and engaging with storytelling techniques
2. Fit exactly {duration_seconds} seconds when spoken (around {target_words} words)
3. Maintain the core message while making it compelling
4. Add proper pacing with emotional beats and story progression
5. Use advanced storytelling techniques: hooks, curiosity gaps, clear progression
6. Create 3 variations following the OUTPUT SCHEMA"""

        # Use custom API key if provided
        if custom_api_key:
            genai.configure(api_key=custom_api_key)
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                response_mime_type="application/json"
            )
        )
        humanization_instructions = f"""You are a storytelling script humanization expert. Your task is to take raw subtitle text or draft content and transform it into a compelling, natural-sounding story script optimized for YouTube Shorts in {lang_config["name"]}.

Key principles:
- Transform the content using advanced storytelling techniques
- Make it sound conversational and engaging in {lang_config["name"]}
- Use simple, everyday language that people actually connect with
- Add natural speech patterns, pauses, and emotional inflections
- Keep the core message and facts intact but make them compelling
- Add storytelling elements: hooks, curiosity gaps, emotional beats
- Remove any robotic or AI-sounding language
- Add natural transitions and conversational connectors
- Ensure it flows smoothly when spoken aloud and keeps viewers engaged
- Create clear progression: beginning → conflict/problem → resolution/insight
- End with thought-provoking conclusion that encourages engagement
- Use {lang_config["name"]} natural phrases and expressions

{lang_config["system_prompt_addition"]}

Output the same JSON format with humanized content:"""
        
        # Calculate target word count based on duration
        target_words = int((duration_seconds / 60) * words_per_minute)
        
        # Construct the humanization prompt with timing
        prompt = f"""{humanization_instructions}

{CORE_PROMPT}

Target Duration: {duration_seconds} seconds (approximately {target_words} words)

Original Raw Content to Transform:
{raw_script}

Please transform this content to:
1. Sound completely natural and engaging with storytelling techniques
2. Fit exactly {duration_seconds} seconds when spoken (around {target_words} words)
3. Maintain the core message while making it compelling
4. Add proper pacing with emotional beats and story progression
5. Use advanced storytelling techniques: hooks, curiosity gaps, clear progression
6. Create 3 variations following the OUTPUT SCHEMA"""
        
        # Use custom API key if provided
        if custom_api_key:
            genai.configure(api_key=custom_api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=types.GenerationConfig(
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
            
            # Validate required fields in response for new storytelling format
            required_fields = ["story_scripts", "video_titles", "descriptions", "tags"]
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                logging.warning(f"Response missing fields: {missing_fields}")
                return {"error": f"Invalid response format: missing {missing_fields}"}
            
            # Validate that we have variations
            if not isinstance(result.get("story_scripts"), list) or len(result["story_scripts"]) == 0:
                return {"error": "No story script variations generated"}
            
            # Validate title lengths (max 70 characters)
            for i, title in enumerate(result.get("video_titles", [])):
                if len(title) > 70:
                    result["video_titles"][i] = title[:67] + "..."
            
            # Convert new format to old format for backward compatibility
            # Take the first variation as the primary result
            converted_result = {
                "title": result["video_titles"][0] if result.get("video_titles") else "",
                "vo_script": result["story_scripts"][0]["script"] if result.get("story_scripts") and len(result["story_scripts"]) > 0 else "",
                "on_screen_text": [],  # Will be derived from script content
                "description": result["descriptions"][0] if result.get("descriptions") else "",
                "hashtags": result["tags"][0] if result.get("tags") else [],
                "notes": {
                    "humanized": True,
                    "original_length": len(raw_script),
                    "target_duration": f"{duration_seconds} seconds",
                    "processing": "Content transformed using storytelling techniques",
                    "word_count": result["story_scripts"][0].get("word_count", 0) if result.get("story_scripts") and len(result["story_scripts"]) > 0 else 0,
                    "variations_available": {
                        "story_scripts": len(result.get("story_scripts", [])),
                        "video_titles": len(result.get("video_titles", [])),
                        "descriptions": len(result.get("descriptions", [])),
                        "tag_sets": len(result.get("tags", []))
                    },
                    "full_response": result  # Include full response for advanced users
                }
            }
            
            # Generate on-screen text from script content (extract key phrases)
            if converted_result["vo_script"]:
                script_sentences = converted_result["vo_script"].split('. ')[:5]  # Take first 5 sentences
                converted_result["on_screen_text"] = [sentence.split()[:3] for sentence in script_sentences if sentence.strip()]
                converted_result["on_screen_text"] = [' '.join(words) + '...' for words in converted_result["on_screen_text"] if words]
            
            return converted_result
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            logging.error(f"Raw response: {response.text}")
            return {"error": "Invalid JSON response from API"}
        
    except Exception as e:
        logging.error(f"Gemini API error during humanization: {str(e)}")
        return {"error": f"Humanization failed: {str(e)}"}
