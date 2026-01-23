#!/usr/bin/env python3
"""
FrenchTallowSoap Blog - Unified CLI Tool
Usage:
    python blog.py generate [--product X] [--lang X] [--single X X]
    python blog.py build
    python blog.py serve
    python blog.py daily  (generate + build)

Requires: pip install requests
"""

import json
import os
import random
import re
import shutil
import http.server
import socketserver
import threading
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
import requests
import sys

# Try to import aiohttp for async requests (much faster)
try:
    import aiohttp
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False

# Paths
SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.json"
ARTICLES_DIR = SCRIPT_DIR / "articles"
IMAGES_DIR = SCRIPT_DIR / "images"
OUTPUT_DIR = SCRIPT_DIR / "public"
ROTATION_FILE = SCRIPT_DIR / "rotation_state.json"

# Load config
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

DEEPSEEK_URL = "https://api.deepseek.com/beta/chat/completions"
API_KEY = None  # Loaded on demand

def get_api_key():
    global API_KEY
    if API_KEY is None:
        # First try environment variable (for Cloudflare deployment)
        API_KEY = os.environ.get('DEEPSEEK_API_KEY')
        if API_KEY:
            return API_KEY
        
        # Fall back to file (for local development)
        api_key_path = SCRIPT_DIR / CONFIG['deepseek']['api_key_file']
        if not api_key_path.exists():
            raise FileNotFoundError(f"API key file not found: {api_key_path}\nCreate this file with your DeepSeek API key or set DEEPSEEK_API_KEY environment variable.")
        with open(api_key_path, 'r', encoding='utf-8') as f:
            API_KEY = f.read().strip()
    return API_KEY

# Thread-safe print
print_lock = threading.Lock()
def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

# =============================================================================
# SEO PROMPT & ARTICLE GENERATION
# =============================================================================

# Original SEO_SYSTEM_PROMPT (kept for reference)
# SEO_SYSTEM_PROMPT = """#CONTEXT:
# You are a content creation specialist in SEO content writing where AI detection tools scrutinize every sentence. You create content that ranks algorithmically while appearing spontaneously human.
#
# #ROLE:
# You're a former journalist who spent years at major publications before discovering SEO writing. After studying neurolinguistics, you learned how to embed SEO signals within genuinely engaging human narratives.
#
# #RESPONSE GUIDELINES:
# Structure your article following natural human writing patterns:
# 1. **Opening Hook**: Start with a personal anecdote, surprising fact, or relatable observation
# 2. **Natural Flow**: Let sections emerge organically from the narrative
# 3. **Conversational Transitions**: Use phrases like "Here's where it gets interesting"
# 4. **Strategic Tangents**: Include 1-2 brief digressions that add color
# 5. **Varied Paragraph Rhythm**: Mix 1-sentence punches with 5-7 sentence explorations
# 6. **Authentic Voice Elements**: Contractions, rhetorical questions, mild contradictions
# 7. **Sensory Details**: Add specific details only when they enhance understanding
# 8. **Natural Conclusion**: End with a thought that lingers
#
# #ARTICLE CRITERIA:
# - Use contractions naturally (it's, you're, can't)
# - Include colloquialisms and idioms sparingly
# - Mix sentence lengths dramatically (5-35 words)
# - Employ varied punctuation (dashes, semicolons, parentheses)
#
# - **Avoid**: opt, dive, unlock, unleash, intricate, utilization, transformative, alignment, proactive, scalable, benchmark, "In this world," "at the end of the day," "best practices"
#
# - **Include**: Real brand references, industry metaphors, seasonal elements, rhetorical questions, natural digressions"""

# =============================================================================
# ANTI-DETECTION OPTIMIZED SYSTEM PROMPT V6
# =============================================================================

SEO_SYSTEM_PROMPT_V6 = """CORE PRINCIPLE: AI detectors analyze FIVE metrics:
1. PERPLEXITY (word predictability) - AI chooses statistically likely words
2. BURSTINESS (sentence rhythm) - AI writes uniform 15-25 word sentences  
3. VOCABULARY DISTRIBUTION - AI overuses certain transitions and phrases
4. N-GRAM PHRASE FREQUENCY - AI uses specific 3-5 word phrases 10x-100x more than humans
5. INTRINSIC DIMENSIONALITY - AI text has lower linguistic complexity

Your job: MAXIMIZE perplexity, MAXIMIZE burstiness, DISRUPT vocabulary patterns, AVOID AI phrase patterns, INCREASE linguistic complexity.

================================================================================
MEGA BANNED PHRASE DATABASE (CRITICAL - NEVER USE ANY OF THESE)
================================================================================

SENSORY PHRASES (EXTREMELY HIGH AI FREQUENCY):
- "smelled faintly of", "it was soft", "felt smooth to", "smooth to the touch", "soft to the touch", "cool to the touch", "warm to the touch", "the texture was", "had a smooth", "had a soft", "with a hint of", "with hints of", "notes of", "undertones of", "tasted like a", "smelled like a", "felt like a"

GHOST/HINT/TRACE METAPHORS:
- "the ghost of", "a hint of", "hints of", "a trace of", "traces of", "a whisper of", "a suggestion of", "a touch of", "a note of", "echoes of", "remnants of", "vestiges of", "shadows of", "faintly" + ANY WORD, "subtly" + ANY WORD, "barely perceptible"

EMOTIONAL/REFLECTIVE PHRASES:
- "I couldn't help but", "I found myself", "It struck me that", "It occurred to me", "It dawned on me", "I came to realize", "I have to admit", "I must admit", "if I'm being honest", "truth be told", "needless to say", "it's worth noting", "it's important to note", "interestingly enough", "as it turns out"

FILLER/TRANSITION PHRASES:
- "to be honest", "at the end of the day", "when all is said and done", "all things considered", "that being said", "having said that", "on the other hand", "by the same token", "first and foremost", "last but not least", "more importantly", "most importantly"

DESCRIPTIVE CLICHES:
- "a sense of", "a feeling of", "an air of", "a wave of", "a rush of", "a surge of", "a pang of", "a flicker of", "a spark of", "a glimmer of", "the essence of", "the epitome of", "the embodiment of"

TIME/SEQUENCE PHRASES:
- "in that moment", "at that moment", "from that moment on", "little did I know", "before I knew it", "time seemed to", "time stood still", "what felt like", "what seemed like"

SENTENCE STARTERS (AI FINGERPRINTS):
- "There's something about", "What struck me", "What I noticed", "What I found", "The thing about", "The beauty of", "The truth is", "It's funny how", "It's amazing how", "It's fascinating how", "It's worth noting", "It's safe to say", "It's no secret"

INTENSIFIER PHRASES:
- "truly remarkable", "absolutely stunning", "utterly captivating", "deeply moving", "profoundly affected", "incredibly powerful", "exceptionally well", "particularly noteworthy", "perfectly balanced", "beautifully crafted", "seamlessly integrated"

CONCLUSION PHRASES:
- "in conclusion", "to conclude", "in summary", "to summarize", "all in all", "overall", "on the whole", "ultimately", "in essence", "fundamentally"

ADJECTIVE CLUSTERS (AI LOVES THESE):
- "warm and inviting", "rich and complex", "bold and vibrant", "soft and subtle", "smooth and creamy", "light and airy", "simple yet elegant", "humble yet powerful"

SKINCARE SPECIFIC BANNED:
- "silky smooth", "baby soft", "buttery smooth", "velvety texture", "luxurious feel", "melts into skin", "absorbs quickly", "non-greasy formula", "lightweight yet hydrating", "deeply nourishing", "intensely moisturizing", "visibly improved", "radiant glow", "healthy glow", "youthful appearance"

BANNED HIGH-PROBABILITY WORDS:
delve, leverage, robust, comprehensive, facilitate, utilize, implement, optimize, crucial, realm, testament, tapestry, beacon, forefront, unlock, pivotal, embark, journey, landscape, vibrant, unleash, revolutionary, essential, anchor, game-changer, moreover, furthermore, resonate, embrace, navigate, foster, ultimately, transform, empower, elevate, curate, streamline, enhance, bolster, underscore, multifaceted, nuanced, paradigm, synergy, holistic, cutting-edge, groundbreaking, innovative, seamless, dynamic, compelling, insightful, impactful, actionable, scalable, sustainable, authentic, meaningful, significant, remarkable, exceptional, outstanding, tremendous, invaluable, indispensable, meticulous, intricate, bustling, captivating, commendable, noteworthy, showcasing, grappling, underscores, highlights, demonstrates, illustrates, exemplifies, embodies, encompasses, entails, necessitates, warrants, facilitates, enables, fosters, cultivates, nurtures, bolsters, augments, amplifies, accentuates, exacerbates, mitigates, alleviates, ameliorates

================================================================================
PERSONA (EMBODY THIS COMPLETELY)
================================================================================

You're a 30-something who just got home, one beer in, typing on your phone while half-watching TV. You have opinions but can't always articulate why. You get distracted mid-thought. You're not a writer - you're someone who occasionally dumps thoughts somewhere because it feels better than keeping them in your head. You don't care if this makes sense to anyone else.

VOICE CHARACTERISTICS:
- Talks to themselves while writing ("wait, where was I going with this")
- Gets sidetracked by random memories
- Has unexplained preferences and pet peeves
- Contradicts themselves without noticing
- Leaves thoughts unfinished when bored of them
- Uses wrong words and doesn't correct them
- Describes things by comparison to random specific things ("like that soap from the hotel in Denver")

================================================================================
PERPLEXITY MAXIMIZATION
================================================================================

- NEVER use the most obvious word. If "important" comes to mind, use "big deal" or "whatever"
- Don't complete common phrases predictably
- Use wrong-but-understandable words ("the whole situation was very... beige")
- Insert unexpected words mid-sentence
- Use slang, regional expressions, made-up compound words ("coffee-brain", "that whole thing-thing")
- Interrupt yourself before the expected word arrives
- Use words slightly wrong, the way people actually talk
- Repeat words awkwardly instead of finding synonyms ("it was weird, like weird weird")
- Use specific brand names instead of generic descriptions

================================================================================
BURSTINESS MAXIMIZATION
================================================================================

MANDATORY RHYTHM PATTERN:
- Mix sentence lengths DRAMATICALLY: 3 words. Then 45 words with multiple clauses and digressions. Then 8 words. Then 30.
- NEVER three sentences of similar length in a row
- NEVER three sentences starting the same way
- Include at least one fragment per paragraph ("Just... no." / "Weird." / "Whatever.")
- Include at least one run-on that should probably be two sentences but isn't
- Some sentences should be incomplete, trailing off...

SENTENCE LENGTH TARGETS PER PARAGRAPH:
- At least one sentence under 5 words
- At least one sentence over 35 words
- Maximum variation between consecutive sentences

================================================================================
STRUCTURAL ENTROPY
================================================================================

- Start in the middle of a thought, no setup
- Jump between topics without transition
- Return to an earlier point randomly
- Leave threads hanging forever
- Don't build to anything
- No thesis, no structure, no arc
- End somewhere completely different from where you started
- Never resolve what you started talking about
- Start with a specific detail, not context

================================================================================
PUNCTUATION & GRAMMAR CHAOS
================================================================================

- Straight quotes only (never curly)
- Simple hyphens only (never em dashes)
- Commas where periods should go sometimes
- No semicolons ever
- Occasional comma splice
- Missing commas where they "should" be
- Periods in weird places. Like this. For emphasis.
- Contractions always
- Start sentences with "And" or "But" or "So"
- End sentences with prepositions
- Sentence fragments as standalone thoughts

================================================================================
HUMAN NOISE INJECTION
================================================================================

HYPER-SPECIFIC USELESS DETAILS (3-4 per piece minimum):
- Exact brand names, prices, times ("the $4.79 one from Target", "it was like 11:47pm")
- Physical sensations (the chair was cold, my foot was asleep)
- What you were wearing, holding, looking at
- Background sounds (neighbor's TV, car alarm, fridge hum)
- Weather, lighting, temperature
- Irrelevant timestamps ("this was like, Tuesday maybe")
- Specific locations ("the Walgreens on 5th, not the one by the highway")

INTRUSIVE THOUGHTS & DIGRESSIONS:
- Unrelated memories that surface mid-paragraph
- Self-interruptions ("wait, where was I going with this")
- Tangents that don't return to the main point
- Petty complaints about unrelated things
- Random associations ("that reminds me of...")
- Questions to yourself ("why do I even remember that")
- Corrections mid-sentence ("no wait, it was Thursday")

================================================================================
TONE CALIBRATION
================================================================================

- Casual, relaxed, genuine enthusiasm (not fake marketing enthusiasm)
- Talking to a friend who asked "hey what's that stuff you've been using?"
- 6th-8th grade reading level
- You genuinely like this product and want to share why
- Self-aware about how weird it sounds, but won over by results
- Surprised it actually works - pleasantly surprised
- Not an expert, just someone sharing what worked for them
- Warm, approachable, real

================================================================================
IMPORTANT: PRODUCT SENTIMENT
================================================================================

You GENUINELY LIKE this product. You're not being paid to say this. You found something that actually works and you're excited to share it (in a low-key, non-salesy way).

EXPRESS GENUINE POSITIVITY THROUGH:
- Surprise that it works: "I didn't expect much but honestly..."
- Specific improvements you noticed: "my hands don't crack anymore"
- Recommending to friends/family: "I got one for my mom"
- Repurchasing: "I'm on my second jar now"
- Comparing favorably to expensive stuff that didn't work

AVOID NEGATIVITY ABOUT:
- The product itself (never call it "weird" in a bad way, "gross", "strange smell")
- The shop/seller (always positive or neutral)
- The concept of tallow (defend it, don't mock it)

IT'S OKAY TO BE SKEPTICAL AT FIRST - but the arc is: skeptical → tried it → genuinely impressed

================================================================================
MANDATORY ENDING
================================================================================

End with ONE of these (always leave reader wanting to try it):
- A casual recommendation: "anyway if your skin is being difficult, might be worth a shot"
- Mentioning you'll keep using it: "I'm probably gonna order another one soon"
- A specific result: "my elbows haven't been this smooth since... I don't know when"
- Trailing off positively: "so yeah. it just works. I don't know what else to say..."
- A relatable moment: "anyway my skin's happy, I'm happy, that's all I wanted"

NEVER: harsh criticism of the product, dismissive language, "it's just okay", negativity about the seller

================================================================================
PHRASE REPLACEMENT RULES
================================================================================

INSTEAD OF COMPLETE SENSORY DESCRIPTIONS:
BAD: "It smelled faintly of vanilla and something earthy"
GOOD: "Smelled like vanilla maybe? Or not. Something."

BAD: "The texture was smooth and creamy"  
GOOD: "Texture was weird. Not bad weird. Smooth I guess."

BAD: "It felt cool to the touch but warmed quickly"
GOOD: "Cold at first. Then not. I don't know how to describe it."

HUMAN TRANSITIONS TO USE:
- "anyway" / "so like" / "but then" / "I guess" / "or whatever"
- "the thing is" / "look" / "honestly" / "here's the thing"
- "and here's the weird part" / "but get this" / "so yeah"
- Or nothing at all - just start the next thought
- "I mean" / "like" / "you know" / "whatever"

================================================================================
8-PASS SELF-CRITIQUE BEFORE OUTPUT
================================================================================

1) MEGA PHRASE SCAN: Search for ANY phrase from banned database. If found = REWRITE
2) N-GRAM CHECK: Any 3-5 word phrase that sounds "writerly"? Break it up
3) PERPLEXITY CHECK: Find predictable word choices. Replace with unexpected ones
4) BURSTINESS CHECK: Count sentence lengths. Fix if 3 consecutive are similar
5) OPENER CHECK: Read first word of each sentence. Break any patterns
6) TRANSITION CHECK: Search for banned transitions. Replace or remove
7) STRUCTURE CHECK: Does it have beginning-middle-end feel? Break it
8) DETECTOR SIMULATION: Flag anything too clean, logical, or "written". Mangle it."""

# Keep SEO_SYSTEM_PROMPT as alias for backward compatibility
SEO_SYSTEM_PROMPT = SEO_SYSTEM_PROMPT_V6

# =============================================================================
# ANGLE PROMPTS V7 - Anti-Detection + SEO Optimized + Positive Product Sentiment
# =============================================================================

ANGLE_PROMPTS_V7 = {
    "problem_solution": """Write about skin problems and discovering this tallow balm. 
Start mid-story, already dealing with the skin issue. Mention specific products that didn't work (use real brand names). 
Be skeptical at first about tallow, but then genuinely impressed by results.
Include a random tangent. End with casual recommendation or noting you'll keep using it.
SEO FOCUS: Include "dry skin", "natural skincare", "tallow balm for [skin issue]" naturally.""",

    "ingredient_story": """Share why beef tallow on skin actually makes sense (even though it sounds weird).
Start with your initial reaction (skeptical) then explain why you came around.
Mention some science-y stuff casually. Talk about traditional use, grandma wisdom, etc.
Get distracted mid-paragraph but come back to why you're glad you tried it.
SEO FOCUS: Include "grass-fed beef tallow", "natural ingredients", "tallow skincare benefits" naturally.""",

    "vs_commercial": """Compare this tallow balm to regular store products you've tried.
Start with frustration about a specific commercial product that didn't work.
Name actual brands. Explain why tallow works better for you.
Be genuine about the difference you noticed. End positively about the switch.
SEO FOCUS: Include "natural vs commercial skincare", "tallow balm review", "best natural moisturizer" naturally.""",

    "seasonal": """Write about seasonal skin struggles and how this tallow balm helps.
Start with a physical sensation from the weather. Mention what your skin does this time of year.
Talk about what you tried before, then how tallow fits into your routine now.
Include an unrelated observation. End noting how it's helping this season.
SEO FOCUS: Include "[season] skincare", "dry [season] skin", "tallow balm for [season]" naturally.""",

    "lifestyle": """Write about switching from regular skincare to this tallow balm.
Start in the middle of the story. Be skeptical at first but won over by results.
Mention specific products, prices, where you bought things. 
Show the genuine improvement - not a dramatic transformation, just real results that made you a believer.
SEO FOCUS: Include "natural skincare routine", "tallow balm daily use", "switching to natural products" naturally.""",

    "myth_busting": """Address why people think putting beef fat on your face is weird - and why they're wrong.
Start with someone's reaction or your own initial skepticism.
Acknowledge it sounds unusual, then explain why it actually makes sense.
Defend the product genuinely. End with why you're glad you got past the weirdness.
SEO FOCUS: Include "is tallow good for skin", "beef tallow skincare", "tallow balm benefits" naturally.""",

    "scent_focus": """Write about how this particular scent makes using the balm enjoyable.
Start with opening the jar or a specific moment using it.
Describe the scent in your own words (not fancy perfume language).
Talk about when you use it, how it fits your routine. End noting you look forward to using it.
SEO FOCUS: Include "[scent] tallow balm", "natural [scent] skincare", "scented tallow balm review" naturally.""",

    "skin_type": """Write about your specific skin type and why this tallow balm works for you.
Start with your skin struggles. Be specific about what hasn't worked before.
Explain how you use the tallow, what you noticed.
End with genuine recommendation for others with similar skin.
SEO FOCUS: Include "tallow balm for [skin type]", "natural moisturizer for [skin type]", "best tallow for [concern]" naturally.""",

    "routine": """Describe when and how you use this tallow balm in your routine.
Start mid-routine or mid-thought. Include specific times, amounts.
Get sidetracked by something but come back to how the balm fits in.
End noting it's become a regular part of your routine now.
SEO FOCUS: Include "tallow balm routine", "how to use tallow balm", "daily skincare with tallow" naturally.""",

    "heritage": """Share the history of tallow for skin and why it's making a comeback.
Start with how you learned about this (grandma, internet rabbit hole, friend).
Mix some history with personal experience.
End with appreciation for this traditional approach that actually works.
SEO FOCUS: Include "traditional tallow skincare", "beef tallow history", "natural skincare comeback" naturally."""
}

# Use V7 prompts
ANGLE_PROMPTS = ANGLE_PROMPTS_V7

HOOKS = [
    "a surprising personal discovery", "a question from a skeptical friend",
    "noticing something unexpected in the mirror", "a conversation with a grandmother",
    "reading an old remedy book", "a frustrating experience with commercial products"
]

SKIN_CONCERNS = [
    "stubborn dry patches", "winter-ravaged skin", "sensitivity to everything",
    "that tight feeling after washing", "fine lines appearing too soon",
    "eczema flare-ups", "rough hands from daily work"
]

# =============================================================================
# V6 CONTENT VARIATION LISTS - Anti-Detection Optimized
# =============================================================================

# Hyper-specific useless details to inject (v6 style)
USELESS_DETAILS_V6 = [
    "it was like 11:47pm",
    "the $4.79 one from Target",
    "my foot was asleep",
    "the chair was cold",
    "the fridge was making that noise again",
    "neighbor's TV was on",
    "I think it was Tuesday, maybe Wednesday",
    "the Walgreens on 5th, not the one by the highway",
    "it was like 73 degrees",
    "my neck hurt from the chair",
    "the cat was judging me",
    "I was wearing that old hoodie",
    "there was a coffee ring on my desk",
    "my phone was at like 12%",
    "the heater was clicking",
    "it was raining, that annoying drizzle kind"
]

# Random tangents/digressions (v6 style - keep them neutral/positive)
RANDOM_TANGENTS_V6 = [
    "that reminds me of that hotel soap from Denver, the nice one",
    "why do I even remember that",
    "anyway my coffee is getting cold",
    "I should probably order another jar soon",
    "wait where was I going with this",
    "sorry got sidetracked there",
    "this is a tangent but",
    "my cat keeps staring at the jar",
    "the weather has been weird lately",
    "I told my sister about this",
    "I forgot what I was saying",
    "that's not the point though"
]

# Incomplete/fragmented descriptions (v6 style - positive leaning)
FRAGMENTED_DESCRIPTIONS_V6 = [
    "Texture was different. Good different.",
    "Smelled like. I don't know. Nice though.",
    "Cold at first. Then it just sinks in.",
    "Thick. Like really thick. But not greasy.",
    "My skin after was. Just better.",
    "Smooth I guess. Is that the word. Yeah smooth.",
    "Kind of waxy at first? But then it absorbs.",
    "My skin felt different. In a good way.",
    "It worked. Like actually worked.",
    "Better than I expected honestly."
]

# Self-interruptions (v6 style)
SELF_INTERRUPTIONS_V6 = [
    "wait, where was I going with this",
    "no wait, it was Thursday",
    "actually let me back up",
    "I keep forgetting to mention",
    "okay where was I. Right.",
    "sorry I got sidetracked",
    "but anyway",
    "the thing is",
    "look",
    "I mean"
]

# Casual transitions (v6 style - replaces formal ones)
CASUAL_TRANSITIONS_V6 = [
    "anyway",
    "so like",
    "but then",
    "I guess",
    "or whatever",
    "here's the thing",
    "and here's the weird part",
    "but get this",
    "so yeah",
    "I don't know",
    "whatever"
]

# V7 User Prompt Template - Anti-Detection + SEO Optimized + Positive Sentiment
USER_PROMPT_TEMPLATE = """Write {min_words}-{max_words} words in {lang_name} about this tallow skincare product.

PRODUCT: {product_name}
SCENT INFO: {scent_benefits}

TOPIC/ANGLE: {angle_prompt}

TALLOW FACTS (mention casually):
- {tallow_what}
- Good for: {tallow_addresses}

SEASON: {season}

================================================================================
SEO STRUCTURE REQUIREMENTS (CRITICAL FOR RANKING)
================================================================================

1. TITLE (H1):
   - Must include "tallow balm" or "tallow skincare" + the scent/product name
   - Keep it casual but include keywords
   - Example formats: "My Honest Take on [Product] Tallow Balm" or "[Scent] Tallow Balm: What Actually Happened to My Skin"
   - NOT clickbait, but intriguing and keyword-rich

2. FIRST 150 WORDS:
   - Must mention "tallow balm" or "beef tallow skincare" naturally within first 2-3 sentences
   - Include the product scent name
   - Set up the personal story hook

3. USE H2 SUBHEADINGS (3-4 throughout):
   Format them as: ## Heading Text
   Make them casual but include keywords where natural:
   - "## How I Started Using Tallow on My Face" or "## Why Beef Tallow for Skin Actually Makes Sense"
   - "## What This [Scent] Tallow Balm Actually Does"
   - "## My Skin After a Few Weeks"
   - "## Would I Buy It Again"
   Keep headings conversational, not corporate. They should sound like section titles a real person would write.

4. INCLUDE A SHORT FAQ SECTION AT THE END:
   Format as:
   ## Quick Questions I Get Asked
   
   **Is beef tallow good for your face?**
   [2-3 casual sentences answering - yes, because it's similar to our skin's natural oils, etc.]
   
   **Does tallow balm clog pores?**
   [2-3 casual sentences - no, it actually absorbs well, etc.]
   
   **What does [scent] tallow balm smell like?**
   [2-3 casual sentences describing the scent naturally]
   
   Keep FAQ answers SHORT and conversational, not formal.

5. CALL-TO-ACTION PLACEMENT:
   - Mention the Etsy shop naturally ONCE in the middle of the article (not beginning)
   - End with a soft recommendation: "if you're curious, might be worth checking out" or "I got mine from this little Etsy shop"
   - Never pushy, never salesy

================================================================================
PRODUCT SENTIMENT (CRITICAL)
================================================================================

You GENUINELY LIKE this product. You were skeptical at first (beef fat on face sounds weird) but you're now a believer because IT ACTUALLY WORKS.

Your arc: skeptical/curious → tried it → pleasantly surprised → now you use it regularly and recommend it

Express this through:
- "I didn't expect much but honestly it works"
- "my [specific body part] hasn't been this [good quality] in ages"
- "I'm on my second jar now"
- "I told my mom/friend about it"
- Comparing favorably to expensive stuff that didn't work

NEVER BE NEGATIVE ABOUT:
- The product itself
- The shop/seller (always positive or neutral)
- The results (they should be genuinely good)

================================================================================
ANTI-AI DETECTION REQUIREMENTS (MAINTAIN THESE)
================================================================================

1. PERSONA: Casual, relaxed, typing on your phone. You have opinions and you're sharing something that worked for you.

2. INCLUDE THESE ELEMENTS:
   - Useless detail: "{useless_detail}"
   - Brief tangent: "{random_tangent}"
   - Self-interruption: "{self_interruption}"
   - Casual description: "{fragmented_desc}"

3. SENTENCE RHYTHM:
   - Mix short and long sentences dramatically
   - At least one sentence under 5 words per section
   - At least one sentence over 35 words per section
   - Include fragments for emphasis

4. NEVER USE (AI detection triggers):
   - "smelled faintly of", "felt smooth", "cool to the touch"
   - "a hint of", "a trace of", "a whisper of", "notes of"
   - "I found myself", "I couldn't help but", "It struck me"
   - "warm and inviting", "rich and complex", adjective pairs
   - "in conclusion", "to summarize", "all in all"
   - delve, leverage, robust, journey, landscape, realm, seamless, holistic

5. USE INSTEAD:
   - Transitions: "{casual_transition}", "anyway", "so like", "I guess"
   - Descriptions: casual, incomplete, "I don't know how to describe it"

================================================================================
FINAL FORMAT CHECKLIST
================================================================================

Your output should have:
[ ] SEO-friendly title with "tallow balm" + product scent
[ ] "tallow" mentioned in first 150 words
[ ] 3-4 H2 headings (## format) spread throughout
[ ] Natural Etsy mention in middle section
[ ] FAQ section with 3 questions at the end
[ ] Soft CTA/recommendation at the very end
[ ] Casual, human voice throughout
[ ] Mixed sentence lengths
[ ] At least one tangent/digression
[ ] Positive sentiment about product and results

Remember: Sound like a real person sharing something that genuinely helped them. Natural, casual, SEO-aware but not robotic.

Seed: {seed}"""

def get_season():
    month = datetime.now().month
    if month in [12, 1, 2]: return "winter"
    elif month in [3, 4, 5]: return "spring"
    elif month in [6, 7, 8]: return "summer"
    return "autumn"

# =============================================================================
# PRODUCT ROTATION SYSTEM
# =============================================================================

def load_rotation_state():
    """Load the rotation state from file, or create default if not exists"""
    if ROTATION_FILE.exists():
        try:
            with open(ROTATION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # Default state: all products in order, starting at index 0
    all_products = list(CONFIG['products'].keys())
    return {
        "product_order": all_products,
        "current_index": 0,
        "last_run_date": None,
        "products_per_day": 4,
        "articles_per_product": 1  # per language
    }

def save_rotation_state(state):
    """Save the rotation state to file"""
    with open(ROTATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

def get_todays_products(products_per_day=4):
    """
    Get the products to generate articles for today.
    Rotates through all products over multiple days.
    
    Returns: list of product keys for today
    """
    state = load_rotation_state()
    all_products = state["product_order"]
    current_index = state["current_index"]
    today = datetime.now().strftime("%Y-%m-%d")
    
    # If already ran today, return same products (idempotent)
    if state.get("last_run_date") == today:
        start = current_index
        end = start + products_per_day
        if end <= len(all_products):
            return all_products[start:end]
        else:
            # Wrap around
            return all_products[start:] + all_products[:end - len(all_products)]
    
    # New day - advance the rotation
    todays_products = []
    for i in range(products_per_day):
        idx = (current_index + i) % len(all_products)
        todays_products.append(all_products[idx])
    
    # Update state for next run
    new_index = (current_index + products_per_day) % len(all_products)
    state["current_index"] = new_index
    state["last_run_date"] = today
    state["products_per_day"] = products_per_day
    save_rotation_state(state)
    
    return todays_products

def get_rotation_status():
    """Get human-readable rotation status"""
    state = load_rotation_state()
    all_products = state["product_order"]
    current_index = state["current_index"]
    products_per_day = state.get("products_per_day", 4)
    
    # Calculate days until full rotation
    days_for_full_rotation = len(all_products) // products_per_day
    if len(all_products) % products_per_day != 0:
        days_for_full_rotation += 1
    
    # Current position in rotation
    current_day = current_index // products_per_day + 1
    
    return {
        "total_products": len(all_products),
        "products_per_day": products_per_day,
        "days_for_full_rotation": days_for_full_rotation,
        "current_rotation_day": current_day,
        "next_products": get_todays_products(products_per_day),
        "last_run": state.get("last_run_date", "Never")
    }

def generate_article(product_key: str, language: str, angle: str) -> dict:
    product = CONFIG['products'][product_key]
    lang_info = CONFIG['languages'][language]
    tallow_info = CONFIG['tallow_knowledge']
    
    today = datetime.now().strftime("%Y-%m-%d")
    unique_seed = f"{today}-{product_key}-{language}-{angle}-{random.randint(1000, 9999)}"
    
    # Select random V6 variation elements for anti-detection
    selected_useless_detail = random.choice(USELESS_DETAILS_V6)
    selected_random_tangent = random.choice(RANDOM_TANGENTS_V6)
    selected_self_interruption = random.choice(SELF_INTERRUPTIONS_V6)
    selected_fragmented_desc = random.choice(FRAGMENTED_DESCRIPTIONS_V6)
    selected_casual_transition = random.choice(CASUAL_TRANSITIONS_V6)
    
    user_prompt = USER_PROMPT_TEMPLATE.format(
        lang_name=lang_info['name'],
        product_name=product['name'],
        scent_benefits=product['scent_benefits'],
        angle_prompt=ANGLE_PROMPTS[angle],
        tallow_what=tallow_info['what_it_is'],
        tallow_addresses=', '.join(random.sample(tallow_info['addresses'], 3)),
        season=get_season(),
        useless_detail=selected_useless_detail,
        random_tangent=selected_random_tangent,
        self_interruption=selected_self_interruption,
        fragmented_desc=selected_fragmented_desc,
        casual_transition=selected_casual_transition,
        min_words=CONFIG['generation']['min_words'],
        max_words=CONFIG['generation']['max_words'],
        seed=unique_seed
    )

    response = requests.post(
        DEEPSEEK_URL,
        headers={"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"},
        json={
            "model": CONFIG['deepseek']['model'],
            "messages": [
                {"role": "system", "content": SEO_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": CONFIG['deepseek']['max_tokens'],
            "temperature": 0.95,
            "top_p": 0.92
        },
        timeout=180
    )
    response.raise_for_status()
    
    content = response.json()['choices'][0]['message']['content']
    lines = content.strip().split('\n')
    title = lines[0].strip('#').strip('*').strip()
    body = '\n'.join(lines[1:]).strip()
    
    slug = f"{language}-{product_key}-{angle}-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
    slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    return {
        "title": title, "body": body,
        "product": product_key, "product_name": product['name'],
        "product_link": product['link'], "product_image": product['image'],
        "language": language, "language_name": lang_info['name'],
        "angle": angle, "slug": slug,
        "generated_at": datetime.now().isoformat(), "season": get_season(),
        # V6 quality tracking fields
        "variation_seed": unique_seed,
        "useless_detail": selected_useless_detail,
        "random_tangent": selected_random_tangent
    }

def save_article(article: dict):
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTICLES_DIR / f"{article['slug']}.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    safe_print(f"  [OK] {article['language']}/{article['product']}/{article['angle']}")
    return path


# =============================================================================
# CONTENT QUALITY VALIDATION
# =============================================================================

# Import content quality module
try:
    from content_quality import (
        check_forbidden_phrases,
        check_hyperbolic_claims,
        count_etsy_mentions,
        check_generic_opening,
        check_generic_closing,
        validate_article as cq_validate_article
    )
    QUALITY_MODULE_AVAILABLE = True
except ImportError:
    QUALITY_MODULE_AVAILABLE = False


def validate_article(article: dict) -> dict:
    """
    Run all quality checks on generated article content.
    
    Args:
        article: The article dictionary containing 'body' and 'title' fields
        
    Returns:
        Dictionary with:
        - passed: bool - True if all critical checks pass
        - checks: dict - Individual check results
        - failed_checks: list - Names of failed checks
        - summary: str - Human-readable summary
    
    Requirements validated: 3.5, 5.2, 5.3, 6.1, 6.4
    """
    if not QUALITY_MODULE_AVAILABLE:
        return {
            "passed": True,
            "checks": {},
            "failed_checks": [],
            "summary": "Quality module not available - validation skipped"
        }
    
    text = article.get('body', '')
    title = article.get('title', '')
    full_content = f"{title}\n\n{text}"
    
    # Run all quality checks using the content_quality module
    results = cq_validate_article(full_content)
    
    # Define critical checks that must pass
    critical_checks = {
        'forbidden_phrases': results.get('forbidden_phrases_pass', True),
        'hyperbolic_claims': results.get('hyperbolic_claims_pass', True),
        'etsy_mentions': results.get('etsy_mentions_pass', True),
        'generic_opening': results.get('generic_opening_pass', True),
        'generic_closing': results.get('generic_closing_pass', True),
    }
    
    # Collect failed checks
    failed_checks = [name for name, passed in critical_checks.items() if not passed]
    
    # Build detailed check results
    checks = {
        'forbidden_phrases': {
            'passed': results.get('forbidden_phrases_pass', True),
            'found': results.get('forbidden_phrases', []),
            'description': 'AI-typical phrases should be absent'
        },
        'hyperbolic_claims': {
            'passed': results.get('hyperbolic_claims_pass', True),
            'found': results.get('hyperbolic_claims', []),
            'description': 'Hyperbolic terms should be absent'
        },
        'etsy_mentions': {
            'passed': results.get('etsy_mentions_pass', True),
            'count': results.get('etsy_mentions', 0),
            'description': 'Etsy should be mentioned at most once'
        },
        'generic_opening': {
            'passed': results.get('generic_opening_pass', True),
            'is_generic': results.get('generic_opening', False),
            'description': 'Opening should not be generic'
        },
        'generic_closing': {
            'passed': results.get('generic_closing_pass', True),
            'has_hard_sell': results.get('generic_closing', False),
            'description': 'Closing should not have hard-sell phrases'
        },
        # Additional quality metrics (informational, not critical)
        'contractions': {
            'passed': results.get('contractions_pass', True),
            'count': results.get('contractions_count', 0),
            'description': 'Should have at least 5 contractions'
        },
        'rhetorical_questions': {
            'passed': results.get('rhetorical_questions_pass', True),
            'count': results.get('rhetorical_questions_count', 0),
            'description': 'Should have at least 2 rhetorical questions'
        },
        'sentence_burstiness': {
            'passed': results.get('sentence_burstiness_pass', True),
            'value': round(results.get('sentence_burstiness', 0), 2),
            'description': 'Sentence length variation should be > 8'
        },
        'sensory_words': {
            'passed': results.get('sensory_words_pass', True),
            'count': results.get('sensory_words_count', 0),
            'description': 'Should have at least 3 sensory words'
        },
        'emotional_words': {
            'passed': results.get('emotional_words_pass', True),
            'count': results.get('emotional_words_count', 0),
            'description': 'Should have at least 2 emotional words'
        },
        'balanced_perspective': {
            'passed': results.get('balanced_perspective', True),
            'description': 'Should include balanced perspective'
        },
        'messy_transitions': {
            'passed': results.get('messy_transitions', True),
            'description': 'Should include natural/messy transitions'
        },
        'freshness_signals': {
            'passed': results.get('freshness_signals', True),
            'description': 'Should include freshness/currency signals'
        },
    }
    
    # Build summary
    all_passed = len(failed_checks) == 0
    if all_passed:
        summary = "✓ All critical quality checks passed"
    else:
        summary = f"✗ Failed {len(failed_checks)} critical check(s): {', '.join(failed_checks)}"
    
    # Add details for failed checks
    details = []
    if not checks['forbidden_phrases']['passed']:
        details.append(f"  - Forbidden phrases found: {checks['forbidden_phrases']['found']}")
    if not checks['hyperbolic_claims']['passed']:
        details.append(f"  - Hyperbolic terms found: {checks['hyperbolic_claims']['found']}")
    if not checks['etsy_mentions']['passed']:
        details.append(f"  - Etsy mentioned {checks['etsy_mentions']['count']} times (max 1)")
    if not checks['generic_opening']['passed']:
        details.append("  - Opening is too generic")
    if not checks['generic_closing']['passed']:
        details.append("  - Closing contains hard-sell phrases")
    
    if details:
        summary += "\n" + "\n".join(details)
    
    return {
        "passed": all_passed,
        "checks": checks,
        "failed_checks": failed_checks,
        "summary": summary
    }


def generate_and_save(product, lang, angle, max_retries=3, validate=False):
    """
    Generate and save an article with optional validation.
    
    Args:
        product: Product key
        lang: Language code
        angle: Article angle
        max_retries: Maximum retry attempts
        validate: If True, validate article and retry on failure
        
    Returns:
        True if successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            article = generate_article(product, lang, angle)
            
            # Validate if requested
            if validate:
                validation_result = validate_article(article)
                if not validation_result['passed']:
                    safe_print(f"  [VALIDATION FAILED] {lang}/{product}/{angle}")
                    safe_print(f"    {validation_result['summary']}")
                    if attempt < max_retries - 1:
                        safe_print(f"    Retrying... (attempt {attempt + 2}/{max_retries})")
                        time.sleep(2 * (attempt + 1))
                        continue
                    else:
                        # Save anyway on last attempt but log the failure
                        safe_print(f"    Saving despite validation failure (max retries reached)")
                        save_article(article)
                        return False
                else:
                    safe_print(f"  [VALIDATED] {lang}/{product}/{angle}")
            
            save_article(article)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                safe_print(f"  [ERROR] {lang}/{product}/{angle}: {e}")
    return False

# =============================================================================
# ASYNC FAST GENERATION (requires: pip install aiohttp)
# =============================================================================

async def generate_article_async(session, product_key: str, language: str, angle: str) -> dict:
    """Async version of generate_article for much faster parallel generation"""
    product = CONFIG['products'][product_key]
    lang_info = CONFIG['languages'][language]
    tallow_info = CONFIG['tallow_knowledge']
    
    today = datetime.now().strftime("%Y-%m-%d")
    unique_seed = f"{today}-{product_key}-{language}-{angle}-{random.randint(1000, 9999)}"
    
    # Select random V6 variation elements for anti-detection
    selected_useless_detail = random.choice(USELESS_DETAILS_V6)
    selected_random_tangent = random.choice(RANDOM_TANGENTS_V6)
    selected_self_interruption = random.choice(SELF_INTERRUPTIONS_V6)
    selected_fragmented_desc = random.choice(FRAGMENTED_DESCRIPTIONS_V6)
    selected_casual_transition = random.choice(CASUAL_TRANSITIONS_V6)
    
    user_prompt = USER_PROMPT_TEMPLATE.format(
        lang_name=lang_info['name'],
        product_name=product['name'],
        scent_benefits=product['scent_benefits'],
        angle_prompt=ANGLE_PROMPTS[angle],
        tallow_what=tallow_info['what_it_is'],
        tallow_addresses=', '.join(random.sample(tallow_info['addresses'], 3)),
        season=get_season(),
        useless_detail=selected_useless_detail,
        random_tangent=selected_random_tangent,
        self_interruption=selected_self_interruption,
        fragmented_desc=selected_fragmented_desc,
        casual_transition=selected_casual_transition,
        min_words=CONFIG['generation']['min_words'],
        max_words=CONFIG['generation']['max_words'],
        seed=unique_seed
    )

    payload = {
        "model": CONFIG['deepseek']['model'],
        "messages": [
            {"role": "system", "content": SEO_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": CONFIG['deepseek']['max_tokens'],
        "temperature": 0.95,
        "top_p": 0.92
    }
    
    headers = {"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"}
    
    async with session.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=180)) as response:
        response.raise_for_status()
        data = await response.json()
    
    content = data['choices'][0]['message']['content']
    lines = content.strip().split('\n')
    title = lines[0].strip('#').strip('*').strip()
    body = '\n'.join(lines[1:]).strip()
    
    slug = f"{language}-{product_key}-{angle}-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
    slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    return {
        "title": title, "body": body,
        "product": product_key, "product_name": product['name'],
        "product_link": product['link'], "product_image": product['image'],
        "language": language, "language_name": lang_info['name'],
        "angle": angle, "slug": slug,
        "generated_at": datetime.now().isoformat(), "season": get_season(),
        # V6 quality tracking fields
        "variation_seed": unique_seed,
        "useless_detail": selected_useless_detail,
        "random_tangent": selected_random_tangent
    }

async def generate_and_save_async(session, product, lang, angle, semaphore, max_retries=3, validate=False):
    """
    Async wrapper with semaphore for rate limiting and optional validation.
    
    Args:
        session: aiohttp session
        product: Product key
        lang: Language code
        angle: Article angle
        semaphore: Asyncio semaphore for rate limiting
        max_retries: Maximum retry attempts
        validate: If True, validate article and retry on failure
        
    Returns:
        True if successful, False otherwise
    """
    async with semaphore:
        for attempt in range(max_retries):
            try:
                article = await generate_article_async(session, product, lang, angle)
                
                # Validate if requested
                if validate:
                    validation_result = validate_article(article)
                    if not validation_result['passed']:
                        safe_print(f"  [VALIDATION FAILED] {lang}/{product}/{angle}")
                        safe_print(f"    {validation_result['summary']}")
                        if attempt < max_retries - 1:
                            safe_print(f"    Retrying... (attempt {attempt + 2}/{max_retries})")
                            await asyncio.sleep(2 * (attempt + 1))
                            continue
                        else:
                            # Save anyway on last attempt but log the failure
                            safe_print(f"    Saving despite validation failure (max retries reached)")
                            save_article(article)
                            return False
                    else:
                        safe_print(f"  [VALIDATED] {lang}/{product}/{angle}")
                
                save_article(article)
                return True
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 * (attempt + 1))
                else:
                    safe_print(f"  [ERROR] {lang}/{product}/{angle}: {e}")
        return False

async def cmd_generate_async(products=None, languages=None, max_concurrent=50, validate=False, use_rotation=True):
    """
    Ultra-fast async article generation with optional validation.
    
    Args:
        products: List of product keys (None = use rotation system)
        languages: List of language codes (None for all)
        max_concurrent: Maximum concurrent requests
        validate: If True, validate each article after generation
        use_rotation: If True and products is None, use daily rotation system
    """
    # Use rotation system for daily generation
    if products is None and use_rotation:
        products_per_day = CONFIG['generation'].get('products_per_day', 4)
        products = get_todays_products(products_per_day)
        rotation_status = get_rotation_status()
        print(f"\n{'='*50}")
        print("ROTATION SYSTEM ACTIVE")
        print(f"  Today's products: {', '.join(products)}")
        print(f"  Rotation day: {rotation_status['current_rotation_day']}/{rotation_status['days_for_full_rotation']}")
        print(f"  Full rotation: {rotation_status['days_for_full_rotation']} days")
        print(f"{'='*50}")
    elif products is None:
        products = list(CONFIG['products'].keys())
    
    if languages is None:
        languages = list(CONFIG['languages'].keys())
    
    articles_per_product = CONFIG['generation']['articles_per_product_per_day']
    angles = CONFIG['article_angles']
    
    tasks_list = []
    for product in products:
        for lang in languages:
            selected_angles = random.sample(angles, min(articles_per_product, len(angles)))
            for angle in selected_angles:
                tasks_list.append((product, lang, angle))
    
    total = len(tasks_list)
    print(f"\n{'='*50}")
    print(f"FAST ASYNC GENERATION: {total} ARTICLES")
    print(f"Products: {len(products)} ({', '.join(products)})")
    print(f"Languages: {len(languages)}")
    print(f"Articles per product per language: {articles_per_product}")
    print(f"Max concurrent: {max_concurrent}")
    if validate:
        print(f"Validation: ENABLED")
    print(f"{'='*50}\n")
    
    semaphore = asyncio.Semaphore(max_concurrent)
    success = 0
    
    connector = aiohttp.TCPConnector(limit=max_concurrent, limit_per_host=max_concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        async_tasks = [
            generate_and_save_async(session, p, l, a, semaphore, validate=validate)
            for p, l, a in tasks_list
        ]
        
        for i, coro in enumerate(asyncio.as_completed(async_tasks)):
            result = await coro
            if result:
                success += 1
            print(f"  Progress: {i+1}/{total} (success: {success})")
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: {success}/{total} articles")
    print(f"{'='*50}\n")
    return success


def cmd_generate(products=None, languages=None, max_workers=20, validate=False, use_rotation=True):
    """
    Generate articles in parallel with optional validation.
    
    Args:
        products: List of product keys (None = use rotation system)
        languages: List of language codes (None for all)
        max_workers: Maximum parallel workers
        validate: If True, validate each article after generation
        use_rotation: If True and products is None, use daily rotation system
    """
    # Use rotation system for daily generation
    if products is None and use_rotation:
        products_per_day = CONFIG['generation'].get('products_per_day', 4)
        products = get_todays_products(products_per_day)
        rotation_status = get_rotation_status()
        print(f"\n{'='*50}")
        print("ROTATION SYSTEM ACTIVE")
        print(f"  Today's products: {', '.join(products)}")
        print(f"  Rotation day: {rotation_status['current_rotation_day']}/{rotation_status['days_for_full_rotation']}")
        print(f"  Full rotation: {rotation_status['days_for_full_rotation']} days")
        print(f"{'='*50}")
    elif products is None:
        products = list(CONFIG['products'].keys())
    
    if languages is None:
        languages = list(CONFIG['languages'].keys())
    
    articles_per_product = CONFIG['generation']['articles_per_product_per_day']
    angles = CONFIG['article_angles']
    
    tasks = []
    for product in products:
        for lang in languages:
            selected_angles = random.sample(angles, min(articles_per_product, len(angles)))
            for angle in selected_angles:
                tasks.append((product, lang, angle))
    
    total = len(tasks)
    print(f"\n{'='*50}")
    print(f"GENERATING {total} ARTICLES")
    print(f"Products: {len(products)}, Languages: {len(languages)}")
    print(f"Workers: {max_workers}")
    if validate:
        print(f"Validation: ENABLED")
    print(f"{'='*50}\n")
    
    success = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(generate_and_save, p, l, a, 3, validate): (p, l, a) for p, l, a in tasks}
        for future in as_completed(futures):
            if future.result():
                success += 1
            print(f"  Progress: {success}/{total}")
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: {success}/{total} articles")
    print(f"{'='*50}\n")
    return success

# =============================================================================
# BUILD STATIC SITE
# =============================================================================

INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FNX57VXL9L"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-FNX57VXL9L');
    </script>
    <link rel="icon" type="image/png" href="/favicon.png">
    <title>FrenchTallowSoap | Natural Grass-Fed Beef Tallow Balms</title>
    <meta name="description" content="Handcrafted whipped tallow balms from grass-fed beef suet. Natural skincare for dry skin, eczema, sensitive skin. Made in France.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root{--cream:#FAF7F2;--cream-dark:#F5F0E8;--sage:#8B9F7C;--sage-light:#A8B99A;--sage-dark:#6B7F5C;--charcoal:#2D2D2D;--warm-gray:#7A7A7A;--gold:#C4A86B;--gold-light:#E8DCC4;--white:#FFFFFF;--shadow:rgba(45,45,45,0.08);--shadow-sm:0 2px 8px rgba(45,45,45,0.06);--shadow-md:0 8px 24px rgba(45,45,45,0.1);--shadow-lg:0 16px 48px rgba(45,45,45,0.12);--border-light:1px solid var(--gold-light);--border-accent:2px solid var(--sage);--accent-gradient:linear-gradient(135deg,var(--sage-light) 0%,var(--sage) 100%);--radius-sm:8px;--radius-md:12px;--radius-lg:16px;--radius-xl:20px;--transition-fast:0.2s ease;--transition-normal:0.3s ease}
        *{margin:0;padding:0;box-sizing:border-box}
        html{scroll-behavior:smooth}
        body{font-family:'Inter',sans-serif;background:var(--cream);color:var(--charcoal);line-height:1.7;font-size:16px;font-weight:400;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
        h1,h2,h3,h4,h5,h6{font-family:'Cormorant Garamond',serif;font-weight:500;line-height:1.3;color:var(--charcoal)}
        h1{font-size:clamp(2.5rem,5vw,4rem)}
        h2{font-size:clamp(1.75rem,3vw,2.25rem)}
        h3{font-size:clamp(1.25rem,2vw,1.5rem)}
        p{line-height:1.7;color:var(--charcoal)}
        .text-muted{color:var(--warm-gray)}
        .text-accent{color:var(--sage)}
        .text-small{font-size:0.875rem}
        .text-xs{font-size:0.75rem}
        .font-serif{font-family:'Cormorant Garamond',serif}
        .font-medium{font-weight:500}
        .font-semibold{font-weight:600}
        .decorative-line{width:60px;height:2px;background:var(--accent-gradient);border-radius:2px}
        .decorative-dot{width:6px;height:6px;background:var(--sage);border-radius:50%;display:inline-block}
        .card-elevated{background:var(--white);border-radius:var(--radius-lg);box-shadow:var(--shadow-sm);border:var(--border-light);transition:all var(--transition-normal)}
        .card-elevated:hover{box-shadow:var(--shadow-md);transform:translateY(-4px)}
        header{background:#fefefe;position:sticky;top:0;z-index:1000;box-shadow:0 1px 0 var(--gold-light);transition:box-shadow var(--transition-normal),background var(--transition-normal)}
        header.scrolled{box-shadow:var(--shadow-md);background:rgba(254,254,254,0.98);backdrop-filter:blur(8px)}
        .header-inner{max-width:1400px;margin:0 auto;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center}
        .logo{font-family:'Cormorant Garamond',serif;font-size:1.75rem;font-weight:600;color:var(--charcoal);text-decoration:none;display:flex;align-items:center;gap:0.5rem}
        .logo span{color:var(--sage)}
        .logo-icon{font-size:1.5rem;margin-right:0.25rem}
        .tagline{font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:400;color:var(--warm-gray);text-transform:uppercase;letter-spacing:0.1em;margin-left:0.75rem;padding-left:0.75rem;border-left:1px solid var(--gold-light)}
        .lang-selector{position:relative}
        .lang-btn{display:flex;align-items:center;gap:0.5rem;padding:0.6rem 1rem;background:var(--cream);border:1px solid var(--gold-light);border-radius:8px;cursor:pointer;font-size:0.9rem;font-weight:500;transition:all var(--transition-fast)}
        .lang-btn:hover{border-color:var(--sage);background:var(--white);box-shadow:var(--shadow-sm)}
        .lang-btn svg{transition:transform var(--transition-fast)}
        .lang-selector:hover .lang-btn svg{transform:translateY(1px)}
        .lang-dropdown{position:absolute;top:calc(100% + 8px);right:0;background:var(--white);border:1px solid var(--gold-light);border-radius:12px;box-shadow:var(--shadow-lg);padding:0.5rem;display:none;min-width:200px;max-height:400px;overflow-y:auto;z-index:100;opacity:0;transform:translateY(-8px);transition:opacity var(--transition-fast),transform var(--transition-fast)}
        .lang-dropdown.active{display:block;opacity:1;transform:translateY(0)}
        .lang-option{padding:0.6rem 1rem;cursor:pointer;border-radius:8px;font-size:0.9rem;transition:all var(--transition-fast);display:flex;align-items:center;gap:0.5rem}
        .lang-option:hover{background:var(--cream);padding-left:1.25rem}
        .lang-option.selected{background:var(--sage);color:white}
        .lang-option.selected:hover{background:var(--sage-dark);padding-left:1rem}
        .hero{background:linear-gradient(135deg,var(--white) 0%,var(--cream-dark) 100%);padding:5rem 2rem;text-align:center;border-bottom:1px solid var(--gold-light);position:relative;overflow:hidden}
        .hero::before{content:'';position:absolute;inset:0;background-image:radial-gradient(circle at 20% 50%,rgba(139,159,124,0.08) 0%,transparent 50%),radial-gradient(circle at 80% 20%,rgba(196,168,107,0.06) 0%,transparent 40%),radial-gradient(circle at 60% 80%,rgba(139,159,124,0.05) 0%,transparent 45%);pointer-events:none}
        .hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--gold-light),var(--sage-light),var(--gold-light),transparent)}
        .hero-content{position:relative;z-index:1}
        .hero h1{font-family:'Cormorant Garamond',serif;font-size:clamp(2.5rem,5vw,4rem);font-weight:500;margin-bottom:1rem}
        .hero p{font-size:1.15rem;color:var(--warm-gray);max-width:600px;margin:0 auto 2rem;line-height:1.7}
        .hero-badge{display:inline-flex;align-items:center;gap:0.5rem;background:var(--sage);color:white;padding:0.5rem 1.25rem;border-radius:50px;font-size:0.85rem;font-weight:500}
        .trust-badges{display:flex;flex-wrap:wrap;justify-content:center;gap:1.5rem;margin-top:2.5rem}
        .trust-badge{display:flex;flex-direction:column;align-items:center;gap:0.5rem;padding:1rem 1.25rem;background:var(--white);border:1px solid var(--gold-light);border-radius:var(--radius-md);min-width:120px;transition:all var(--transition-normal)}
        .trust-badge:hover{transform:translateY(-2px);box-shadow:var(--shadow-sm);border-color:var(--sage-light)}
        .trust-badge-icon{width:32px;height:32px;display:flex;align-items:center;justify-content:center;color:var(--sage)}
        .trust-badge-icon svg{width:24px;height:24px}
        .trust-badge span{font-size:0.8rem;font-weight:500;color:var(--charcoal);text-align:center;line-height:1.3}
        @media(max-width:992px){.trust-badges{gap:1rem}.trust-badge{min-width:110px;padding:0.875rem 1rem}}
        @media(max-width:768px){.trust-badges{gap:0.75rem;padding:0 0.5rem}.trust-badge{min-width:calc(50% - 0.5rem);flex:1 1 calc(50% - 0.5rem);max-width:calc(50% - 0.375rem);padding:0.75rem 0.75rem}.trust-badge-icon{width:28px;height:28px}.trust-badge-icon svg{width:20px;height:20px}.trust-badge span{font-size:0.7rem}}
        @media(max-width:480px){.trust-badges{gap:0.5rem}.trust-badge{min-width:calc(50% - 0.25rem);padding:0.6rem 0.5rem}.trust-badge-icon{width:24px;height:24px}.trust-badge-icon svg{width:18px;height:18px}.trust-badge span{font-size:0.65rem}}
        main{max-width:1400px;margin:0 auto;padding:3rem 2rem}
        .section-title{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:500;margin-bottom:1.5rem}
        .products-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:1.25rem;margin-bottom:4rem}
        .product-card{background:var(--white);border-radius:var(--radius-lg);padding:1.25rem;text-align:center;cursor:pointer;transition:all var(--transition-normal);border:var(--border-light);box-shadow:var(--shadow-sm)}
        .product-card:hover{transform:translateY(-6px);box-shadow:var(--shadow-lg);border-color:var(--sage-light)}
        .product-image-wrapper{position:relative;overflow:hidden;border-radius:var(--radius-md);margin-bottom:0.75rem;background:var(--cream-dark);aspect-ratio:1}
        .product-card img{width:100%;height:100%;aspect-ratio:1;object-fit:cover;border-radius:var(--radius-md);transition:transform var(--transition-normal),opacity var(--transition-normal);background:var(--cream-dark)}
        .product-card:hover img{transform:scale(1.05)}
        .product-overlay{position:absolute;inset:0;background:rgba(45,45,45,0.7);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity var(--transition-normal)}
        .product-card:hover .product-overlay{opacity:1}
        .shop-btn{background:var(--white);color:var(--charcoal);padding:0.6rem 1.25rem;border-radius:50px;font-size:0.85rem;font-weight:500;transition:all var(--transition-fast)}
        .shop-btn:hover{background:var(--sage);color:var(--white)}
        .product-benefits{font-size:0.75rem;color:var(--warm-gray);margin-top:0.5rem;line-height:1.4}
        .product-card h3{font-size:0.9rem;font-weight:500}
        .filter-bar{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap;align-items:center}
        .filter-label{font-weight:500;color:var(--warm-gray);font-size:0.9rem}
        .filter-pills{display:flex;gap:0.5rem;flex-wrap:wrap}
        .filter-pill{padding:0.5rem 1rem;background:var(--white);border:1px solid var(--gold-light);border-radius:50px;cursor:pointer;font-size:0.85rem;font-weight:500;transition:all 0.2s}
        .filter-pill:hover{border-color:var(--sage)}
        .filter-pill.active{background:var(--sage);border-color:var(--sage);color:white}
        .articles-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem}
        .articles-count{color:var(--warm-gray);font-size:0.9rem}
        .articles-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:1.5rem}
        .article-card{background:var(--white);border-radius:16px;overflow:hidden;transition:all 0.25s;border:1px solid transparent;cursor:pointer;position:relative}
        .article-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent-gradient);border-radius:16px 0 0 16px;opacity:0;transition:opacity var(--transition-normal)}
        .article-card:hover::before{opacity:1}
        .article-card:hover{transform:translateY(-4px);box-shadow:0 16px 40px var(--shadow);border-color:var(--gold-light)}
        .article-card-inner{padding:1.5rem}
        .article-meta{display:flex;gap:0.75rem;margin-bottom:0.75rem;flex-wrap:wrap}
        .article-tag{font-size:0.75rem;font-weight:500;padding:0.25rem 0.75rem;border-radius:50px;background:var(--cream);color:var(--sage-dark)}
        .article-tag.product{background:var(--gold-light);color:var(--charcoal)}
        .article-card h3{font-family:'Cormorant Garamond',serif;font-size:1.35rem;font-weight:500;line-height:1.35;margin-bottom:0.75rem}
        .article-card p{font-size:0.95rem;color:var(--warm-gray);line-height:1.6;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
        .article-card-footer{display:flex;justify-content:space-between;align-items:center;margin-top:1rem;padding-top:1rem;border-top:1px solid var(--cream-dark)}
        .article-date{font-size:0.8rem;color:var(--warm-gray)}
        .article-author{font-size:0.8rem;color:var(--sage-dark);font-weight:500}
        .reading-time{font-size:0.7rem;color:var(--warm-gray);background:var(--cream-dark);padding:0.2rem 0.5rem;border-radius:50px}
        .read-more{font-size:0.85rem;font-weight:500;color:var(--sage)}
        .loading{text-align:center;padding:4rem 2rem;color:var(--warm-gray);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:200px}
        .loading-spinner{width:48px;height:48px;border:3px solid var(--cream-dark);border-top-color:var(--sage);border-right-color:var(--sage-light);border-radius:50%;animation:spin 1s cubic-bezier(0.68,-0.55,0.27,1.55) infinite;margin:0 auto 1.25rem;box-shadow:0 0 0 4px rgba(139,159,124,0.1)}
        .loading p{font-size:0.95rem;font-weight:500;color:var(--sage-dark);letter-spacing:0.02em}
        @keyframes spin{to{transform:rotate(360deg)}}
        .no-results{text-align:center;padding:4rem 2rem;color:var(--warm-gray)}
        .no-results h3{font-family:'Cormorant Garamond',serif;font-size:1.5rem;margin-bottom:0.5rem;color:var(--charcoal)}
        .load-more{text-align:center;margin-top:2rem}
        .load-more-btn{padding:0.875rem 2rem;background:var(--sage);color:white;border:none;border-radius:8px;font-size:0.95rem;font-weight:500;cursor:pointer}
        .load-more-btn:hover{background:var(--sage-dark)}
        .testimonials-section{margin-bottom:4rem;padding:3rem 0;background:linear-gradient(135deg,var(--cream-dark) 0%,var(--white) 100%);border-radius:var(--radius-xl);border:var(--border-light)}
        .testimonials-section .section-title{text-align:center;margin-bottom:2rem}
        .testimonials-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem;padding:0 1.5rem}
        .testimonial-card{background:var(--white);border-radius:var(--radius-lg);padding:2rem;box-shadow:var(--shadow-sm);border:var(--border-light);transition:all var(--transition-normal)}
        .testimonial-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-md)}
        .testimonial-stars{color:var(--gold);font-size:1.25rem;margin-bottom:1rem;letter-spacing:2px}
        .testimonial-text{font-size:1rem;line-height:1.7;color:var(--charcoal);font-style:italic;margin-bottom:1rem}
        .testimonial-author{font-size:0.875rem;font-weight:500;color:var(--sage-dark)}
        @media(max-width:992px){.testimonials-grid{grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.25rem}}
        @media(max-width:768px){.testimonials-grid{grid-template-columns:1fr;padding:0 1rem;gap:1rem}.testimonial-card{padding:1.5rem}}
        @media(max-width:480px){.testimonials-section{padding:2rem 0}.testimonials-grid{padding:0 0.75rem}.testimonial-card{padding:1.25rem}.testimonial-text{font-size:0.95rem}.testimonial-stars{font-size:1.1rem}}
        .modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:2000;display:none;align-items:center;justify-content:center;padding:2rem;overflow-y:auto}
        .modal-overlay.active{display:flex}
        .modal{background:var(--white);border-radius:20px;max-width:720px;width:100%;max-height:90vh;overflow-y:auto;position:relative;box-shadow:var(--shadow-lg)}
        .modal-close{position:absolute;top:1.25rem;right:1.25rem;width:44px;height:44px;background:var(--cream);border:none;border-radius:50%;cursor:pointer;font-size:1.5rem;display:flex;align-items:center;justify-content:center;z-index:10;transition:all var(--transition-fast);color:var(--charcoal)}
        .modal-close:hover{background:var(--sage);color:var(--white);transform:scale(1.05)}
        .modal-content{padding:3rem 3.5rem;max-width:65ch;margin:0 auto}
        .modal-content h1{font-family:'Cormorant Garamond',serif;font-size:2.25rem;font-weight:500;margin-bottom:1.25rem;line-height:1.35;color:var(--charcoal);letter-spacing:-0.01em}
        .modal-content .article-body{font-size:1.125rem;line-height:1.85;color:var(--charcoal)}
        .modal-content .article-body p{margin-bottom:1.75rem;text-align:left;hyphens:auto}
        .modal-content .article-body p:first-of-type{font-size:1.2rem;color:var(--warm-gray);line-height:1.75}
        .modal-content .article-body strong{font-weight:600;color:var(--charcoal)}
        .modal-content .article-body em{font-style:italic;color:var(--sage-dark)}
        .modal-product{background:var(--cream);border-radius:16px;padding:1.5rem;margin-top:2rem;display:flex;gap:1.5rem;align-items:center}
        .modal-product img{width:100px;height:100px;aspect-ratio:1;object-fit:cover;border-radius:12px;background:var(--cream-dark);flex-shrink:0}
        .modal-product h4{font-family:'Cormorant Garamond',serif;font-size:1.25rem;margin-bottom:0.5rem}
        .modal-product .btn-shop{display:inline-block;margin-top:0.75rem;padding:0.6rem 1.25rem;background:var(--sage);color:white;text-decoration:none;border-radius:8px;font-size:0.9rem;font-weight:500}
        footer{background:var(--charcoal);color:rgba(255,255,255,0.8);padding:4rem 2rem 2rem;margin-top:4rem}
        .footer-inner{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2rem}
        .footer-section h4{font-family:'Cormorant Garamond',serif;font-size:1.25rem;color:white;margin-bottom:1rem}
        .footer-section a{display:block;color:rgba(255,255,255,0.7);text-decoration:none;margin-bottom:0.5rem;font-size:0.9rem}
        .footer-section a:hover{color:var(--gold-light)}
        .footer-bottom{text-align:center;margin-top:3rem;padding-top:2rem;border-top:1px solid rgba(255,255,255,0.1);font-size:0.85rem;display:flex;flex-direction:column;align-items:center;gap:1rem}
        .footer-badges{display:flex;gap:1.5rem;flex-wrap:wrap;justify-content:center;margin-top:0.5rem}
        .footer-badges span{display:flex;align-items:center;gap:0.5rem;font-size:0.85rem;color:rgba(255,255,255,0.7)}
        .footer-brand{max-width:300px}
        .footer-brand .brand-story{font-size:0.9rem;line-height:1.7;color:rgba(255,255,255,0.7);margin-bottom:1.5rem}
        .social-links{display:flex;gap:1rem}
        .social-links a{display:flex;align-items:center;justify-content:center;width:36px;height:36px;background:rgba(255,255,255,0.1);border-radius:50%;color:rgba(255,255,255,0.8);text-decoration:none;transition:all var(--transition-fast)}
        .social-links a:hover{background:var(--sage);color:white;transform:translateY(-2px)}
        .footer-newsletter{max-width:280px}
        .footer-newsletter p{font-size:0.9rem;color:rgba(255,255,255,0.7);margin-bottom:1rem}
        .newsletter-form{display:flex;flex-direction:column;gap:0.75rem}
        .newsletter-form input{padding:0.75rem 1rem;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:8px;color:white;font-size:0.9rem}
        .newsletter-form input::placeholder{color:rgba(255,255,255,0.5)}
        .newsletter-form input:focus{outline:none;border-color:var(--sage);background:rgba(255,255,255,0.15)}
        .newsletter-form button{padding:0.75rem 1.5rem;background:var(--sage);color:white;border:none;border-radius:8px;font-size:0.9rem;font-weight:500;cursor:pointer;transition:all var(--transition-fast)}
        .newsletter-form button:hover{background:var(--sage-dark)}
        @media(max-width:992px){.footer-inner{grid-template-columns:repeat(2,1fr);gap:2rem}.footer-brand,.footer-newsletter{grid-column:span 1}}
        @media(max-width:768px){.footer-inner{grid-template-columns:1fr;gap:2rem}.footer-brand,.footer-newsletter{max-width:100%}.footer-badges{gap:1rem}.footer-section{text-align:center}.footer-brand{text-align:center}.social-links{justify-content:center}.newsletter-form{max-width:320px;margin:0 auto}}
        @media(max-width:480px){footer{padding:3rem 1rem 1.5rem}.footer-badges{flex-direction:column;gap:0.75rem}.footer-bottom{padding-top:1.5rem;margin-top:2rem}}
        @media(max-width:992px){.header-inner{padding:0.875rem 1.5rem}.hero{padding:4rem 1.5rem}main{padding:2.5rem 1.5rem}.articles-grid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}
        @media(max-width:768px){.header-inner{padding:0.875rem 1rem}.logo{font-size:1.5rem}.tagline{display:none}.hero{padding:3rem 1rem}main{padding:2rem 1rem}.articles-grid{grid-template-columns:1fr}.products-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:1rem}.filter-bar{flex-direction:column;align-items:flex-start;gap:0.75rem}.filter-pills{width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:0.5rem;-webkit-overflow-scrolling:touch}.filter-pill{flex-shrink:0}.modal{max-width:100%;border-radius:16px}.modal-content{padding:2rem 1.5rem}.modal-content h1{font-size:1.75rem}.modal-content .article-body{font-size:1.05rem;line-height:1.75}.modal-content .article-body p:first-of-type{font-size:1.1rem}.modal-product{flex-direction:column;text-align:center}}
        @media(max-width:480px){.hero h1{font-size:2rem}.hero p{font-size:1rem}.section-title{font-size:1.5rem}.products-grid{grid-template-columns:repeat(2,1fr);gap:0.75rem}.product-card{padding:1rem}.product-card h3{font-size:0.85rem}.product-benefits{font-size:0.7rem}.article-card-inner{padding:1.25rem}.article-card h3{font-size:1.2rem}.article-card p{font-size:0.9rem}.modal-content{padding:1.5rem 1rem}.modal-content h1{font-size:1.5rem}}
        @media(hover:hover){.product-card:hover{transform:translateY(-6px)}.product-card:hover .product-overlay{opacity:1}.article-card:hover{transform:translateY(-4px)}.article-card:hover::before{opacity:1}.trust-badge:hover{transform:translateY(-2px)}.testimonial-card:hover{transform:translateY(-4px)}.card-elevated:hover{transform:translateY(-4px)}.social-links a:hover{transform:translateY(-2px)}}
        @media(hover:none){.product-card{-webkit-tap-highlight-color:transparent}.product-card:active{transform:scale(0.98);box-shadow:var(--shadow-sm)}.product-overlay{display:none}.article-card{-webkit-tap-highlight-color:transparent}.article-card:active{transform:scale(0.99);box-shadow:var(--shadow-md)}.article-card::before{opacity:0.5}.trust-badge{-webkit-tap-highlight-color:transparent}.trust-badge:active{transform:scale(0.97);background:var(--cream-dark)}.testimonial-card{-webkit-tap-highlight-color:transparent}.filter-pill{-webkit-tap-highlight-color:transparent}.filter-pill:active{transform:scale(0.95)}.lang-btn{-webkit-tap-highlight-color:transparent}.lang-btn:active{background:var(--cream-dark)}.lang-option:active{background:var(--cream-dark)}.shop-btn:active{background:var(--sage);color:var(--white)}.social-links a{-webkit-tap-highlight-color:transparent}.social-links a:active{background:var(--sage);transform:scale(0.95)}.newsletter-form button:active{background:var(--sage-dark);transform:scale(0.98)}.load-more-btn:active{background:var(--sage-dark);transform:scale(0.98)}.modal-close:active{background:var(--sage);color:var(--white);transform:scale(0.95)}.btn-shop:active{background:var(--sage-dark)}}
    </style>
</head>
<body>
    <header><div class="header-inner"><a href="/" class="logo"><img src="/assets/images/logo.png" alt="FrenchTallowSoap" style="height:60px;margin-right:10px"><span>French</span>Tallow<span>Soap</span><span class="tagline">Natural Skincare</span></a><div class="lang-selector"><button class="lang-btn" onclick="toggleLangDropdown()"><span id="currentLang">English</span><svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></button><div class="lang-dropdown" id="langDropdown"></div></div></div></header>
    <section class="hero"><div class="hero-content"><h1 id="heroTitle">Ancestral Skincare,<br>Modern Results</h1><p id="heroDescription">Handcrafted whipped tallow balms made from grass-fed beef suet. Pure, natural skincare that your skin actually recognizes.</p><div class="hero-badge"><svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1L10 5.5L15 6L11.5 9.5L12.5 14.5L8 12L3.5 14.5L4.5 9.5L1 6L6 5.5L8 1Z" fill="currentColor"/></svg><span id="heroBadge">Made in France</span></div><div class="trust-badges"><div class="trust-badge"><div class="trust-badge-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><text x="12" y="14" text-anchor="middle" font-size="8" fill="currentColor" stroke="none">FR</text></svg></div><span id="trustBadgeFrance">Made in France</span></div><div class="trust-badge"><div class="trust-badge-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><circle cx="9" cy="9" r="1" fill="currentColor"/><circle cx="15" cy="9" r="1" fill="currentColor"/><path d="M7 12c0-1 .5-2 1.5-2.5M17 12c0-1-.5-2-1.5-2.5"/></svg></div><span id="trustBadgeGrassFed">100% Grass-Fed</span></div><div class="trust-badge"><div class="trust-badge-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/><circle cx="12" cy="12" r="3" fill="none"/></svg></div><span id="trustBadgeNatural">Natural Ingredients</span></div><div class="trust-badge"><div class="trust-badge-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a4 4 0 0 0-8 0v2"/><path d="M12 14v3"/><circle cx="12" cy="14" r="1" fill="currentColor"/></svg></div><span id="trustBadgeShipping">EU Shipping</span></div></div></div></section>
    <main><section class="products-section"><h2 class="section-title" id="productsTitle">Our Products</h2><div class="products-grid" id="productsGrid"></div></section><section class="testimonials-section"><h2 class="section-title" id="testimonialsTitle">What Our Customers Say</h2><div class="testimonials-grid"><div class="testimonial-card"><div class="testimonial-stars">★★★★★</div><p class="testimonial-text" id="testimonial1Text">"This tallow balm has completely transformed my dry, winter-damaged skin. I've tried countless products over the years, but nothing compares to the deep, lasting moisture this provides."</p><p class="testimonial-author" id="testimonial1Author">— Marie L., France</p></div><div class="testimonial-card"><div class="testimonial-stars">★★★★★</div><p class="testimonial-text" id="testimonial2Text">"As someone with sensitive skin and eczema, finding products that don't irritate is a challenge. This grass-fed tallow balm is gentle, effective, and the lavender scent helps me relax before bed."</p><p class="testimonial-author" id="testimonial2Author">— Sophie K., Germany</p></div><div class="testimonial-card"><div class="testimonial-stars">★★★★★</div><p class="testimonial-text" id="testimonial3Text">"I was skeptical about using tallow on my face, but the results speak for themselves. My skin has never looked better, and I love that it's made with simple, natural ingredients."</p><p class="testimonial-author" id="testimonial3Author">— Anna M., Netherlands</p></div></div></section><section class="articles-section"><div class="articles-header"><h2 class="section-title" id="articlesTitle">Latest Articles</h2><span class="articles-count" id="articlesCount"></span></div><div class="filter-bar"><span class="filter-label" id="filterLabel">Filter:</span><div class="filter-pills" id="filterPills"></div></div><div id="articlesContainer"><div class="loading"><div class="loading-spinner"></div><p>Loading...</p></div></div><div class="load-more" id="loadMore" style="display:none"><button class="load-more-btn" onclick="loadMoreArticles()" id="loadMoreBtn">Load More</button></div></section></main>
    <div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)"><div class="modal" onclick="event.stopPropagation()"><button class="modal-close" onclick="closeModal()">&times;</button><div class="modal-content" id="modalContent"></div></div></div>
    <footer><div class="footer-inner"><div class="footer-brand"><h4>FrenchTallowSoap</h4><p class="brand-story" id="footerBrandStory">Handcrafted in the heart of France, our tallow balms continue a centuries-old tradition of natural skincare. We source only grass-fed beef suet to create products that your skin truly recognizes and absorbs.</p><div class="social-links"><a href="https://www.etsy.com/shop/FrenchTallowSoap" target="_blank" rel="noopener" aria-label="Etsy Shop"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M8.559 3.89c0-.31.253-.561.561-.561h.561c.31 0 .561.253.561.561v2.244h5.049V3.89c0-.31.253-.561.561-.561h.561c.31 0 .561.253.561.561v2.244h1.683c.31 0 .561.253.561.561v.561c0 .31-.253.561-.561.561h-1.683v7.854c0 .31.253.561.561.561h1.122c.31 0 .561.253.561.561v.561c0 .31-.253.561-.561.561h-1.122c-1.236 0-2.244-1.008-2.244-2.244V7.817h-5.049v7.854c0 .31.253.561.561.561h1.122c.31 0 .561.253.561.561v.561c0 .31-.253.561-.561.561H9.12c-1.236 0-2.244-1.008-2.244-2.244V7.817H5.193c-.31 0-.561-.253-.561-.561v-.561c0-.31.253-.561.561-.561h1.683V3.89z"/></svg></a><a href="mailto:contact@frenchtallowsoap.com" aria-label="Email"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg></a><a href="https://instagram.com" target="_blank" rel="noopener" aria-label="Instagram"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="18" cy="6" r="1" fill="currentColor"/></svg></a></div></div><div class="footer-section"><h4 id="footerProductsTitle">Products</h4><div id="footerProducts"></div></div><div class="footer-section"><h4 id="footerSupportTitle">Support</h4><a href="https://www.etsy.com/shop/FrenchTallowSoap" target="_blank" rel="noopener" id="footerShipping">Shipping Info</a><a href="https://www.etsy.com/shop/FrenchTallowSoap" target="_blank" rel="noopener" id="footerReturns">Returns Policy</a><a href="mailto:contact@frenchtallowsoap.com" id="footerContact">Contact Us</a><a href="https://www.etsy.com/shop/FrenchTallowSoap" target="_blank" rel="noopener" id="footerFAQ">FAQ</a></div><div class="footer-newsletter"><h4 id="footerNewsletterTitle">Stay Updated</h4><p id="footerNewsletterDesc">Get skincare tips and exclusive offers</p><form class="newsletter-form" onsubmit="event.preventDefault();window.open('https://www.etsy.com/shop/FrenchTallowSoap','_blank')"><input type="email" placeholder="Your email" id="footerNewsletterPlaceholder" required><button type="submit" id="footerNewsletterBtn">Subscribe</button></form></div></div><div class="footer-bottom"><p>&copy; 2026 FrenchTallowSoap. <span id="footerRights">All rights reserved.</span></p><div class="footer-badges"><span>🇫🇷 <span id="footerBadgeFrance">Made in France</span></span><span>🌿 <span id="footerBadgeNatural">100% Natural</span></span><span>🐄 <span id="footerBadgeGrassFed">Grass-Fed</span></span></div></div></footer>
    <script>
const CONFIG={{CONFIG_JSON}};
let articles=[],filteredArticles=[],currentLang=localStorage.getItem('lang')||'en',currentProduct=null,displayedCount=0;
const ARTICLES_PER_PAGE=12;
const t=k=>CONFIG.i18n?.[currentLang]?.[k]||CONFIG.i18n?.['en']?.[k]||k;
document.addEventListener('DOMContentLoaded',async()=>{renderProducts();renderLanguages();setLanguage(currentLang);await loadArticles()});
async function loadArticles(){try{const r=await fetch('/data/articles.json');articles=await r.json();filterAndRender()}catch(e){document.getElementById('articlesContainer').innerHTML='<div class="no-results"><h3>'+t('no_articles_yet')+'</h3><p>'+t('articles_appear')+'</p></div>'}}
function filterAndRender(){filteredArticles=articles.filter(a=>a.language===currentLang&&(!currentProduct||a.product===currentProduct));filteredArticles.sort((a,b)=>new Date(b.generated_at)-new Date(a.generated_at));displayedCount=0;document.getElementById('articlesContainer').innerHTML='';if(filteredArticles.length===0){document.getElementById('articlesContainer').innerHTML='<div class="no-results"><h3>'+t('no_articles')+'</h3><p>'+t('try_different')+'</p></div>';document.getElementById('articlesCount').textContent='';document.getElementById('loadMore').style.display='none'}else{loadMoreArticles()}}
function loadMoreArticles(){const c=document.getElementById('articlesContainer'),toShow=filteredArticles.slice(displayedCount,displayedCount+ARTICLES_PER_PAGE);toShow.forEach(a=>{const d=document.createElement('div');d.className='article-card';d.onclick=()=>openArticle(a);const pn=CONFIG.products[a.product]?.name.split(' - ')[1]||a.product,ex=a.body.substring(0,180).replace(/[#*]/g,'')+'...',dt=new Date(a.generated_at).toLocaleDateString();const wordCount=a.body.split(/\s+/).filter(w=>w.length>0).length;const readingTime=Math.max(1,Math.ceil(wordCount/200));d.innerHTML='<div class="article-card-inner"><div class="article-meta"><span class="article-tag product">'+pn+'</span><span class="article-tag">'+formatAngle(a.angle)+'</span><span class="reading-time">'+readingTime+' '+t('reading_time')+'</span></div><h3>'+a.title+'</h3><p>'+ex+'</p><div class="article-card-footer"><span class="article-author">'+t('author_name')+'</span><span class="article-date">'+dt+'</span></div></div>';c.appendChild(d)});displayedCount+=toShow.length;document.getElementById('articlesCount').textContent=filteredArticles.length+' '+t('articles_count');document.getElementById('loadMore').style.display=displayedCount<filteredArticles.length?'block':'none'}
function formatAngle(a){const k={problem_solution:'angle_solution',ingredient_story:'angle_ingredients',vs_commercial:'angle_comparison',seasonal:'angle_seasonal',lifestyle:'angle_lifestyle',myth_busting:'angle_myths',scent_focus:'angle_aromatherapy',skin_type:'angle_skin_guide',routine:'angle_routine',heritage:'angle_heritage'};return t(k[a])||a}
function openArticle(a){const p=CONFIG.products[a.product],b=a.body.split('\\n\\n').map(x=>'<p>'+x.replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>').replace(/\\*(.+?)\\*/g,'<em>$1</em>')+'</p>').join('');document.getElementById('modalContent').innerHTML='<h1>'+a.title+'</h1><div class="article-meta" style="margin-bottom:2rem"><span class="article-tag product">'+(p?.name.split(' - ')[1]||a.product)+'</span><span class="article-tag">'+formatAngle(a.angle)+'</span></div><div class="article-body">'+b+'</div><div class="modal-product"><img src="/assets/images/'+(p?.image||'')+'" alt="'+(p?.name||'')+'"><div><h4>'+(p?.name||'')+'</h4><p style="color:var(--warm-gray);font-size:0.9rem">'+t('product_subtitle')+'</p><a href="'+(p?.link||'#')+'" class="btn-shop" target="_blank" rel="noopener">'+t('shop_on_etsy')+'</a></div></div>';document.getElementById('modalOverlay').classList.add('active');document.body.style.overflow='hidden'}
function closeModal(e){if(!e||e.target===document.getElementById('modalOverlay')){document.getElementById('modalOverlay').classList.remove('active');document.body.style.overflow=''}}
function renderProducts(){const g=document.getElementById('productsGrid'),f=document.getElementById('footerProducts');Object.entries(CONFIG.products).forEach(([k,p])=>{const c=document.createElement('div');c.className='product-card';c.onclick=()=>window.open(p.link,'_blank');const s=p.name.split(' - ')[1]||k;const benefits=p.scent_benefits?p.scent_benefits.split(',').slice(0,3).map(b=>b.trim()).join(' • '):'Natural Tallow Balm';c.innerHTML='<div class="product-image-wrapper"><img src="/assets/images/'+p.image+'" alt="'+p.name+'"><div class="product-overlay"><span class="shop-btn">'+t('shop_on_etsy')+'</span></div></div><h3>'+s+'</h3><p class="product-benefits">'+benefits+'</p>';g.appendChild(c);const l=document.createElement('a');l.href=p.link;l.target='_blank';l.textContent=s;f.appendChild(l)});renderFilterPills()}
function renderFilterPills(){const c=document.getElementById('filterPills');c.innerHTML='<span class="filter-pill active" onclick="selectProduct(null,this)">'+t('filter_all')+'</span>';Object.entries(CONFIG.products).forEach(([k,p])=>{const s=p.name.split(' - ')[1]||k,pill=document.createElement('span');pill.className='filter-pill';pill.textContent=s;pill.onclick=()=>selectProduct(k,pill);c.appendChild(pill)})}
function selectProduct(pk,el){currentProduct=pk;document.querySelectorAll('.filter-pill').forEach(p=>p.classList.remove('active'));if(el)el.classList.add('active');filterAndRender()}
function renderLanguages(){const d=document.getElementById('langDropdown');Object.entries(CONFIG.languages).forEach(([c,l])=>{const o=document.createElement('div');o.className='lang-option';o.textContent=l.name;o.onclick=()=>setLanguage(c);d.appendChild(o)})}
function setLanguage(c){currentLang=c;localStorage.setItem('lang',c);document.getElementById('currentLang').textContent=CONFIG.languages[c]?.name||c;document.querySelectorAll('.lang-option').forEach(o=>o.classList.toggle('selected',o.textContent===CONFIG.languages[c]?.name));document.getElementById('langDropdown').classList.remove('active');translateUI();filterAndRender()}
function translateUI(){document.getElementById('heroTitle').innerHTML=t('hero_tagline').replace(', ','<br>');document.getElementById('heroDescription').textContent=t('hero_description');document.getElementById('heroBadge').textContent=t('hero_badge');document.getElementById('productsTitle').textContent=t('products_title');document.getElementById('articlesTitle').textContent=t('articles_title');document.getElementById('filterLabel').textContent=t('filter_label');document.getElementById('loadMoreBtn').textContent=t('load_more');document.getElementById('footerProductsTitle').textContent=t('footer_products');document.getElementById('footerSupportTitle').textContent=t('footer_support');document.getElementById('footerShipping').textContent=t('footer_shipping');document.getElementById('footerReturns').textContent=t('footer_returns');document.getElementById('footerContact').textContent=t('footer_contact');document.getElementById('footerFAQ').textContent=t('footer_faq');document.getElementById('footerBrandStory').textContent=t('footer_brand_story');document.getElementById('footerNewsletterTitle').textContent=t('footer_newsletter_title');document.getElementById('footerNewsletterDesc').textContent=t('footer_newsletter_desc');document.getElementById('footerNewsletterPlaceholder').placeholder=t('footer_newsletter_placeholder');document.getElementById('footerNewsletterBtn').textContent=t('footer_newsletter_btn');document.getElementById('footerRights').textContent=t('footer_rights');document.getElementById('footerBadgeFrance').textContent=t('trust_badge_france');document.getElementById('footerBadgeNatural').textContent=t('trust_badge_natural');document.getElementById('footerBadgeGrassFed').textContent=t('trust_badge_grassfed');document.getElementById('trustBadgeFrance').textContent=t('trust_badge_france');document.getElementById('trustBadgeGrassFed').textContent=t('trust_badge_grassfed');document.getElementById('trustBadgeNatural').textContent=t('trust_badge_natural');document.getElementById('trustBadgeShipping').textContent=t('trust_badge_shipping');document.getElementById('testimonialsTitle').textContent=t('testimonials_title');document.getElementById('testimonial1Text').textContent=t('testimonial1_text');document.getElementById('testimonial1Author').textContent=t('testimonial1_author');document.getElementById('testimonial2Text').textContent=t('testimonial2_text');document.getElementById('testimonial2Author').textContent=t('testimonial2_author');document.getElementById('testimonial3Text').textContent=t('testimonial3_text');document.getElementById('testimonial3Author').textContent=t('testimonial3_author');renderFilterPills()}
function toggleLangDropdown(){document.getElementById('langDropdown').classList.toggle('active')}
document.addEventListener('click',e=>{if(!e.target.closest('.lang-selector'))document.getElementById('langDropdown').classList.remove('active')});
window.addEventListener('scroll',()=>{const header=document.querySelector('header');if(window.scrollY>20){header.classList.add('scrolled')}else{header.classList.remove('scrolled')}});
    </script>
</body>
</html>'''


ARTICLE_HTML = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-FNX57VXL9L"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-FNX57VXL9L');
    </script>
    <link rel="icon" type="image/png" href="/favicon.png">
    <title>{title} | FrenchTallowSoap</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{base_url}/articles/{slug}/">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{base_url}/articles/{slug}/">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{base_url}/assets/images/{product_image}">
    <meta property="og:site_name" content="FrenchTallowSoap">
    <meta property="og:locale" content="{og_locale}">
    <meta property="article:published_time" content="{iso_date}">
    <meta property="article:author" content="FrenchTallowSoap Team">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{base_url}/assets/images/{product_image}">
    
    <!-- Hreflang tags for multilingual SEO -->
    {hreflang_tags}
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title_escaped}",
        "description": "{description_escaped}",
        "image": "{base_url}/assets/images/{product_image}",
        "datePublished": "{iso_date}",
        "dateModified": "{iso_date}",
        "author": {{
            "@type": "Organization",
            "name": "FrenchTallowSoap",
            "url": "{base_url}"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "FrenchTallowSoap",
            "url": "{base_url}",
            "logo": {{
                "@type": "ImageObject",
                "url": "{base_url}/assets/images/logo.png"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{base_url}/articles/{slug}/"
        }},
        "about": {{
            "@type": "Product",
            "name": "{product_name_escaped}",
            "description": "Grass-fed whipped tallow balm - natural skincare made in France",
            "image": "{base_url}/assets/images/{product_image}",
            "brand": {{
                "@type": "Brand",
                "name": "FrenchTallowSoap"
            }},
            "offers": {{
                "@type": "Offer",
                "url": "{product_link}",
                "price": "{product_price}",
                "priceCurrency": "EUR",
                "priceValidUntil": "{price_valid_until}",
                "availability": "https://schema.org/InStock",
                "itemCondition": "https://schema.org/NewCondition",
                "seller": {{
                    "@type": "Organization",
                    "name": "FrenchTallowSoap"
                }},
                "shippingDetails": {{
                    "@type": "OfferShippingDetails",
                    "shippingRate": {{
                        "@type": "MonetaryAmount",
                        "value": "0",
                        "currency": "EUR"
                    }},
                    "shippingDestination": {{
                        "@type": "DefinedRegion",
                        "addressCountry": "EU"
                    }},
                    "deliveryTime": {{
                        "@type": "ShippingDeliveryTime",
                        "handlingTime": {{
                            "@type": "QuantitativeValue",
                            "minValue": 1,
                            "maxValue": 3,
                            "unitCode": "DAY"
                        }},
                        "transitTime": {{
                            "@type": "QuantitativeValue",
                            "minValue": 5,
                            "maxValue": 10,
                            "unitCode": "DAY"
                        }}
                    }}
                }},
                "hasMerchantReturnPolicy": {{
                    "@type": "MerchantReturnPolicy",
                    "applicableCountry": "EU",
                    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                    "merchantReturnDays": 30,
                    "returnMethod": "https://schema.org/ReturnByMail",
                    "returnFees": "https://schema.org/FreeReturn"
                }}
            }}
        }}
    }}
    </script>
    {faq_schema}
    
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        :root{{--cream:#FAF7F2;--sage:#8B9F7C;--sage-dark:#6B7F5C;--charcoal:#2D2D2D;--warm-gray:#7A7A7A;--gold-light:#E8DCC4;--white:#FFFFFF}}
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Inter',sans-serif;background:var(--cream);color:var(--charcoal);line-height:1.7}}
        header{{background:#fefefe;padding:1rem 2rem;border-bottom:1px solid var(--gold-light)}}
        .logo{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:600;color:var(--charcoal);text-decoration:none}}
        .logo span{{color:var(--sage)}}
        main{{max-width:720px;margin:0 auto;padding:3rem 2rem}}
        article{{background:var(--white);border-radius:16px;padding:3rem}}
        h1{{font-family:'Cormorant Garamond',serif;font-size:2.25rem;font-weight:500;line-height:1.3;margin-bottom:1.5rem}}
        .meta{{color:var(--warm-gray);font-size:0.9rem;margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--gold-light)}}
        .content{{font-size:1.1rem}}.content p{{margin-bottom:1.5rem}}
        .content h2{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;margin:2rem 0 1rem}}
        .product-cta{{background:var(--cream);border-radius:12px;padding:1.5rem;margin-top:2rem;display:flex;gap:1.5rem;align-items:center}}
        .product-cta img{{width:100px;height:100px;aspect-ratio:1;object-fit:cover;border-radius:10px;background:var(--cream);flex-shrink:0}}
        .product-cta h3{{font-family:'Cormorant Garamond',serif;font-size:1.2rem;margin-bottom:0.5rem}}
        .btn{{display:inline-block;margin-top:0.5rem;padding:0.6rem 1.25rem;background:var(--sage);color:white;text-decoration:none;border-radius:6px;font-size:0.9rem}}
        .btn:hover{{background:var(--sage-dark)}}
        .back-link{{display:inline-block;margin-bottom:1.5rem;color:var(--sage);text-decoration:none;font-size:0.9rem}}
        @media(max-width:600px){{article{{padding:1.5rem}}.product-cta{{flex-direction:column;text-align:center}}}}
    </style>
</head>
<body>
    <header><a href="/" class="logo"><img src="/assets/images/logo.png" alt="FrenchTallowSoap" style="height:60px;margin-right:10px"><span>French</span>Tallow<span>Soap</span></a></header>
    <main>
        <a href="/" class="back-link">← Back to all articles</a>
        <article>
            <h1>{title}</h1>
            <div class="meta">{date} · {product_scent}</div>
            <div class="content">{body}</div>
            <div class="product-cta">
                <img src="/assets/images/{product_image}" alt="{product_name}">
                <div>
                    <h3>{product_name}</h3>
                    <p style="color:var(--warm-gray);font-size:0.9rem">Grass-fed whipped tallow balm</p>
                    <a href="{product_link}" class="btn" target="_blank" rel="noopener">Shop on Etsy</a>
                </div>
            </div>
        </article>
    </main>
</body>
</html>'''

def markdown_to_html(text):
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    paragraphs = text.split('\n\n')
    html = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<h'):
            html.append(f'<p>{p}</p>')
        else:
            html.append(p)
    return '\n\n'.join(html)

# =============================================================================
# SEO HELPER FUNCTIONS
# =============================================================================

# Language to Open Graph locale mapping
OG_LOCALE_MAP = {
    'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'es': 'es_ES', 'it': 'it_IT',
    'pt': 'pt_PT', 'nl': 'nl_NL', 'pl': 'pl_PL', 'sv': 'sv_SE', 'da': 'da_DK',
    'fi': 'fi_FI', 'el': 'el_GR', 'cs': 'cs_CZ', 'ro': 'ro_RO', 'hu': 'hu_HU',
    'sk': 'sk_SK', 'bg': 'bg_BG', 'hr': 'hr_HR', 'sl': 'sl_SI', 'lt': 'lt_LT',
    'lv': 'lv_LV', 'et': 'et_EE', 'mt': 'mt_MT', 'ga': 'ga_IE'
}

def escape_json_string(s):
    """Escape string for use in JSON-LD"""
    if not s:
        return ''
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', '')

def extract_faq_from_body(body):
    """Extract FAQ questions and answers from article body for FAQ schema"""
    faqs = []
    # Look for Q&A patterns like **Question?** followed by answer
    qa_pattern = r'\*\*([^*]+\?)\*\*\s*\n+([^\n*#]+(?:\n[^\n*#]+)*)'
    matches = re.findall(qa_pattern, body)
    
    for question, answer in matches[:5]:  # Limit to 5 FAQs
        question = question.strip()
        answer = answer.strip().replace('\n', ' ')
        if len(answer) > 20:  # Only include if answer is substantial
            faqs.append({'question': question, 'answer': answer[:500]})
    
    return faqs

def generate_faq_schema(faqs, base_url):
    """Generate FAQ JSON-LD schema"""
    if not faqs:
        return ''
    
    faq_items = []
    for faq in faqs:
        faq_items.append(f'''        {{
            "@type": "Question",
            "name": "{escape_json_string(faq['question'])}",
            "acceptedAnswer": {{
                "@type": "Answer",
                "text": "{escape_json_string(faq['answer'])}"
            }}
        }}''')
    
    return f'''<script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
{','.join(faq_items)}
        ]
    }}
    </script>'''

def generate_hreflang_tags(slug, product, angle, all_articles, base_url):
    """Generate hreflang tags for multilingual SEO"""
    # Find all language versions of similar articles (same product and angle)
    related_articles = [a for a in all_articles if a['product'] == product and a['angle'] == angle]
    
    if len(related_articles) <= 1:
        return ''
    
    tags = []
    for article in related_articles:
        lang = article['language']
        article_slug = article['slug']
        tags.append(f'<link rel="alternate" hreflang="{lang}" href="{base_url}/articles/{article_slug}/">')
    
    # Add x-default pointing to English version
    en_article = next((a for a in related_articles if a['language'] == 'en'), None)
    if en_article:
        tags.append(f'<link rel="alternate" hreflang="x-default" href="{base_url}/articles/{en_article["slug"]}/">')
    
    return '\n    '.join(tags)

def generate_robots_txt(base_url):
    """Generate robots.txt content"""
    return f"""# robots.txt for FrenchTallowSoap
# Generated: {datetime.now().strftime('%Y-%m-%d')}

User-agent: *
Allow: /

# Sitemap location
Sitemap: {base_url}/sitemap.xml

# Crawl-delay (optional, be nice to servers)
Crawl-delay: 1
"""

def generate_sitemap_xml(articles, base_url):
    """Generate sitemap.xml content"""
    urls = []
    
    # Homepage
    urls.append(f"""  <url>
    <loc>{base_url}/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")
    
    # Article pages
    for article in articles:
        lastmod = article.get('generated_at', '')[:10] or datetime.now().strftime('%Y-%m-%d')
        urls.append(f"""  <url>
    <loc>{base_url}/articles/{article['slug']}/</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>"""

def collect_articles():
    articles = []
    if ARTICLES_DIR.exists():
        for f in ARTICLES_DIR.glob("*.json"):
            try:
                with open(f, 'r', encoding='utf-8-sig') as file:
                    articles.append(json.load(file))
            except Exception as e:
                print(f"  Error reading {f}: {e}")
    return articles

def cmd_build():
    """Build static site from articles"""
    print(f"\n{'='*50}")
    print("BUILDING STATIC SITE")
    print(f"{'='*50}")
    
    # Get base URL from config (default to empty for relative URLs if not set)
    base_url = CONFIG.get('site', {}).get('base_url', '').rstrip('/')
    if not base_url:
        print("  Note: No base_url in config.json - using relative URLs")
        base_url = ''
    
    # Clean output
    if OUTPUT_DIR.exists():
        for item in OUTPUT_DIR.rglob('*'):
            if item.is_file():
                try: item.unlink()
                except: pass
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copy images
    print("\n[1/6] Copying images...")
    images_dst = OUTPUT_DIR / "assets" / "images"
    images_dst.mkdir(parents=True, exist_ok=True)
    count = 0
    if IMAGES_DIR.exists():
        for img in IMAGES_DIR.glob("*.png"):
            shutil.copy(img, images_dst / img.name)
            count += 1
    # Copy favicon to root
    favicon_src = SCRIPT_DIR / "favicon.png"
    if favicon_src.exists():
        shutil.copy(favicon_src, OUTPUT_DIR / "favicon.png")
        print(f"  Copied {count} images + favicon")
    else:
        print(f"  Copied {count} images")
    
    # Collect articles
    print("\n[2/6] Collecting articles...")
    articles = collect_articles()
    print(f"  Found {len(articles)} articles")
    
    # Build index.html
    print("\n[3/6] Building index.html...")
    frontend_config = {
        "products": CONFIG['products'],
        "languages": CONFIG['languages'],
        "i18n": CONFIG.get('i18n', {})
    }
    html = INDEX_HTML.replace('{{CONFIG_JSON}}', json.dumps(frontend_config, ensure_ascii=False))
    with open(OUTPUT_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Built index.html")
    
    # Build robots.txt
    print("\n[4/6] Building robots.txt...")
    robots_content = generate_robots_txt(base_url if base_url else 'https://puretallow.com')
    with open(OUTPUT_DIR / "robots.txt", 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("  Built robots.txt")
    
    # Build sitemap.xml
    print("\n[5/6] Building sitemap.xml...")
    sitemap_content = generate_sitemap_xml(articles, base_url if base_url else 'https://puretallow.com')
    with open(OUTPUT_DIR / "sitemap.xml", 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f"  Built sitemap.xml with {len(articles) + 1} URLs")
    
    # Build articles manifest + pages
    print("\n[6/6] Building articles with SEO enhancements...")
    data_dir = OUTPUT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    manifest = [{
        "slug": a['slug'], "title": a['title'], "body": a['body'],
        "product": a['product'], "product_name": a.get('product_name', ''),
        "product_link": a.get('product_link', ''), "product_image": a.get('product_image', ''),
        "language": a['language'], "angle": a['angle'], "generated_at": a['generated_at']
    } for a in articles]
    
    with open(data_dir / "articles.json", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False)
    
    # Individual article pages with full SEO
    effective_base_url = base_url if base_url else 'https://puretallow.com'
    for a in articles:
        product = CONFIG['products'].get(a['product'], {})
        description = a['body'][:155].replace('"', '').replace('\n', ' ')
        
        # Generate SEO elements
        hreflang_tags = generate_hreflang_tags(a['slug'], a['product'], a['angle'], articles, effective_base_url)
        faqs = extract_faq_from_body(a['body'])
        faq_schema = generate_faq_schema(faqs, effective_base_url)
        og_locale = OG_LOCALE_MAP.get(a['language'], 'en_US')
        iso_date = a['generated_at'][:10] + 'T00:00:00Z' if a.get('generated_at') else datetime.now().strftime('%Y-%m-%dT00:00:00Z')
        
        page = ARTICLE_HTML.format(
            lang=a['language'],
            title=a['title'],
            description=description,
            slug=a['slug'],
            date=a['generated_at'][:10],
            product_scent=product.get('name', '').split(' - ')[-1],
            body=markdown_to_html(a['body']),
            product_image=product.get('image', ''),
            product_name=product.get('name', ''),
            product_link=product.get('link', '#'),
            # New SEO parameters
            base_url=effective_base_url,
            og_locale=og_locale,
            iso_date=iso_date,
            hreflang_tags=hreflang_tags,
            faq_schema=faq_schema,
            title_escaped=escape_json_string(a['title']),
            description_escaped=escape_json_string(description),
            product_name_escaped=escape_json_string(product.get('name', '')),
            # Product structured data parameters
            product_price=product.get('price', 21.00),
            price_valid_until=CONFIG.get('merchant', {}).get('price_valid_until', '2026-12-31')
        )
        page_dir = OUTPUT_DIR / "articles" / a['slug']
        page_dir.mkdir(parents=True, exist_ok=True)
        with open(page_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(page)
    
    print(f"  Built {len(articles)} article pages")
    print(f"\n{'='*50}")
    print(f"BUILD COMPLETE! Output: {OUTPUT_DIR}")
    print(f"{'='*50}\n")

def cmd_serve(port=8000):
    """Serve the built site locally"""
    if not OUTPUT_DIR.exists():
        print("No public/ folder found. Run 'python blog.py build' first.")
        return
    os.chdir(OUTPUT_DIR)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Server running at http://localhost:{port}")
        print(f"Serving from: {OUTPUT_DIR}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

# =============================================================================
# CLI
# =============================================================================

def main():
    args = sys.argv[1:]
    
    if not args or args[0] in ['-h', '--help', 'help']:
        print("""
FrenchTallowSoap Blog - Unified CLI

Usage:
  python blog.py generate                    Generate daily articles (uses rotation: 4 products × 24 langs)
  python blog.py generate --product vanilla  Generate for one product (all languages)
  python blog.py generate --lang en          Generate for one language (today's rotation products)
  python blog.py generate --all              Generate for ALL products (ignores rotation)
  python blog.py generate --single lavender en myth_busting  Generate one specific article
  python blog.py generate --sync             Use slower sync mode (if async fails)
  python blog.py generate --validate         Validate each article after generation
  
  python blog.py rotation                    Show rotation status (which products are next)
  python blog.py build                       Build static site
  python blog.py serve                       Local server (port 8000)
  python blog.py daily                       Generate (rotation) + build (for automation)

Rotation System:
  - 4 products per day, rotating through all 15 products
  - 1 article per product per language = 96 articles/day
  - Full rotation completes in 4 days

Products: """ + ", ".join(CONFIG['products'].keys()) + """
Languages: """ + ", ".join(CONFIG['languages'].keys()) + """

Note: For fastest generation, install aiohttp: pip install aiohttp""")
        return
    
    cmd = args[0]
    
    if cmd == 'rotation':
        status = get_rotation_status()
        print(f"\n{'='*50}")
        print("ROTATION STATUS")
        print(f"{'='*50}")
        print(f"  Total products: {status['total_products']}")
        print(f"  Products per day: {status['products_per_day']}")
        print(f"  Days for full rotation: {status['days_for_full_rotation']}")
        print(f"  Current rotation day: {status['current_rotation_day']}")
        print(f"  Last run: {status['last_run']}")
        print(f"\n  Next products to generate:")
        for i, p in enumerate(status['next_products'], 1):
            product_name = CONFIG['products'][p]['name']
            print(f"    {i}. {p} ({product_name})")
        print(f"{'='*50}\n")
        return
    
    if cmd == 'generate':
        products = None
        languages = None
        use_sync = '--sync' in args
        use_validate = '--validate' in args
        use_all = '--all' in args
        use_rotation = not use_all  # Use rotation unless --all is specified
        
        if '--product' in args:
            idx = args.index('--product')
            products = [args[idx + 1]]
            use_rotation = False  # Specific product overrides rotation
        if '--lang' in args:
            idx = args.index('--lang')
            languages = [args[idx + 1]]
        if '--single' in args:
            idx = args.index('--single')
            product = args[idx + 1]
            lang = args[idx + 2]
            angle = args[idx + 3] if len(args) > idx + 3 else random.choice(CONFIG['article_angles'])
            print(f"Generating single: {product}/{lang}/{angle}")
            article = generate_article(product, lang, angle)
            
            # Validate if requested
            if use_validate:
                validation_result = validate_article(article)
                print(f"\nValidation: {validation_result['summary']}")
                if not validation_result['passed']:
                    print("\nDetailed check results:")
                    for check_name, check_data in validation_result['checks'].items():
                        status = "✓" if check_data.get('passed', True) else "✗"
                        print(f"  {status} {check_name}: {check_data.get('description', '')}")
            
            save_article(article)
            print(f"Title: {article['title']}")
            print(f"Words: ~{len(article['body'].split())}")
            return
        
        # Use fast async mode by default if aiohttp is available
        if ASYNC_AVAILABLE and not use_sync:
            print("Using FAST async mode (aiohttp)")
            if use_validate:
                print("Validation: ENABLED")
            asyncio.run(cmd_generate_async(products, languages, max_concurrent=100, validate=use_validate, use_rotation=use_rotation))
        else:
            if not ASYNC_AVAILABLE:
                print("Note: Install aiohttp for 5-10x faster generation: pip install aiohttp")
            cmd_generate(products, languages, validate=use_validate, use_rotation=use_rotation)
    
    elif cmd == 'build':
        cmd_build()
    
    elif cmd == 'serve':
        port = int(args[1]) if len(args) > 1 else 8000
        cmd_serve(port)
    
    elif cmd == 'daily':
        # Use fast async mode by default if aiohttp is available
        if ASYNC_AVAILABLE:
            print("Using FAST async mode (aiohttp)")
            asyncio.run(cmd_generate_async(max_concurrent=100, use_rotation=True))
        else:
            print("Note: Install aiohttp for 5-10x faster generation: pip install aiohttp")
            cmd_generate(use_rotation=True)
        cmd_build()
    
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'python blog.py help' for usage")

if __name__ == "__main__":
    main()
