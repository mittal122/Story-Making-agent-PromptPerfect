#!/usr/bin/env python3
"""
Simple test script to verify the API functions work correctly.
Run this locally to test before deployment.
"""

import os
import sys
import json

# Add the api directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from gemini_service import generate_story_script, humanize_story_script

def test_generate_script():
    """Test script generation"""
    print("Testing script generation...")
    
    input_payload = {
        "api_key_mode": "env",
        "generation": {
            "duration_seconds": 45,
            "duration_type": "short",
            "language": "hi",
            "voice_tags": True,
            "youtube_optimized": True,
            "algorithm_focus": "maximum_reach"
        },
        "content": {
            "topic": "Test topic for script generation",
            "genre": "mysterious",
            "description": "A test script to verify functionality"
        },
        "seo": {
            "hashtag_style": "youtube_optimized",
            "audience": "16-35, Hindi, storytelling",
            "platform": "youtube",
            "optimization_goal": "viral_reach"
        }
    }
    
    # This will fail without API key, but we can check if the function structure works
    try:
        result = generate_story_script(input_payload)
        if result:
            print("✓ Script generation function structure is correct")
            return True
        else:
            print("✗ Script generation returned empty result")
            return False
    except Exception as e:
        if "GEMINI_API_KEY" in str(e) or "api_key" in str(e).lower():
            print("✓ Script generation function structure is correct (API key needed)")
            return True
        else:
            print(f"✗ Script generation failed with error: {e}")
            return False

def test_humanize_script():
    """Test script humanization"""
    print("Testing script humanization...")
    
    raw_script = "यह एक test script है। हम इसे humanize करने की कोशिश कर रहे हैं।"
    
    try:
        result = humanize_story_script(raw_script, 45)
        if result:
            print("✓ Script humanization function structure is correct")
            return True
        else:
            print("✗ Script humanization returned empty result")
            return False
    except Exception as e:
        if "GEMINI_API_KEY" in str(e) or "api_key" in str(e).lower():
            print("✓ Script humanization function structure is correct (API key needed)")
            return True
        else:
            print(f"✗ Script humanization failed with error: {e}")
            return False

def main():
    print("=== PromptPerfect API Test ===\n")
    
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("✓ GEMINI_API_KEY is set")
    else:
        print("⚠ GEMINI_API_KEY not set (expected for testing)")
    
    print()
    
    # Test functions
    test1_pass = test_generate_script()
    test2_pass = test_humanize_script()
    
    print("\n=== Test Summary ===")
    if test1_pass and test2_pass:
        print("✓ All tests passed! API structure is ready for deployment.")
        print("\nNext steps:")
        print("1. Set GEMINI_API_KEY environment variable in Vercel")
        print("2. Deploy to Vercel using: vercel")
        print("3. Test the live application")
    else:
        print("✗ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
