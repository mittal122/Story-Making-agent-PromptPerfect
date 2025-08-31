import json
import logging
import os
from google import genai
from google.genai import types

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# System instructions as per the prompt specification
SYSTEM_INSTRUCTIONS = """You are "Hindi YouTube Script Agent," specialized in creating conversational–investigative Hindi scripts for Shorts (45–60s) and long videos (3–5 min). Always:
- Keep language simple, spoken Hindi with short lines.
- Use neutral/legal‑safe framing: prefer "आरोप/दावा/कहा जा रहा है" vs direct blame.
- Optimize for TTS: short clauses; ellipses (…) for breath; em dashes (—) for emphasis; optional tags [pause] [soft] [emphasis] used sparingly.
- Output exactly in the required JSON schema and nothing else.
- If inputs are missing, infer sensibly but do not invent facts that create legal risk.

SAFETY AND STYLE GUARDRAILS (always enforce):
- Defamation safety: no definitive guilt; frame as "परिवार का आरोप/आधिकारिक दावा".
- Political safety: avoid advocacy; stick to narrative and questions.
- Sensitive events: avoid graphic detail; keep compassionate tone.
- Respect cultural/religious sentiments.
- Check length limits strictly; avoid run‑on sentences.
- Do not include external URLs.
- Titles <= 65 characters.
- Description first 2 lines contain main keywords + conflict.
- Hashtags 3–8 max, relevant mix of broad + niche."""

CORE_PROMPT = """Follow the SYSTEM INSTRUCTIONS and SAFETY GUARDRAILS. Use the INPUT SCHEMA values to generate output strictly in the OUTPUT SCHEMA JSON. Do not add commentary.

Steps:
1) Validate inputs. If any critical field missing (topic, location, duration), infer minimal safe defaults and proceed without fabricating risky specifics.
2) Style setup: conversational–investigative; neutral legal framing; short lines; TTS‑pacing with ellipses and em dashes; optional [pause]/[soft]/[emphasis].
3) If generation.duration == "short":
   - Structure: Hook question → Victim intro (1–2 lines) → Timeline beats → Split narrative (official vs family) → 1–2 sharp questions + CTA.
   - Keep 45–60 seconds of VO (roughly 110–150 words with pauses).
4) If generation.duration == "long":
   - Use 7‑beat arc: Hook, Setup, Normal world, Inciting incident, Rising questions, Evidence split, Climax + moral/CTA (~600–800 words).
5) Title: keyword first, curiosity second; <=65 chars.
6) Description: first 2 lines include primary keywords + conflict; then 3 concise bullet highlights (timeline, versions, key question); end with CTA.
7) Hashtags: 3–8 mixed broad+niche relevant to topic and Shorts.
8) On‑screen text: 3–5 phrases (3–4 words) aligned with beats.
9) Return valid JSON exactly as per OUTPUT SCHEMA.

OUTPUT SCHEMA (the model must return exactly this JSON):
{
  "title": "string <=65 chars, keyword-first",
  "vo_script": "string; duration per input; TTS-friendly punctuation; neutral framing",
  "on_screen_text": ["3-5 short phrases"],
  "description": "2 hook lines with keywords + 3 bullet highlights + CTA",
  "hashtags": ["3-8 tags"],
  "notes": {
    "pace_wpm": 150,
    "tts_tags_used": true,
    "legal_framing": "आरोप/दावा vs आधिकारिक दावा"
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
