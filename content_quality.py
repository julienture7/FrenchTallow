"""
Content Quality Validation Module for Pure Tallow Blog

This module provides functions to validate generated article content
against quality standards defined in the SEO Content Optimization spec.
"""

import re
import statistics
from typing import List, Tuple


# Forbidden AI-typical phrases (from Requirements 3.5)
FORBIDDEN_PHRASES = [
    "dive into",
    "dive deep",
    "unlock",
    "unleash",
    "harness",
    "leverage",
    "in this article",
    "let's explore",
    "without further ado",
    "in today's world",
    "at the end of the day",
    "it's important to note",
    "in conclusion",
    "to summarize",
    "game-changer",
    "revolutionary",
    "transformative",
    "seamlessly",
    "robust",
    "cutting-edge",
    "holistic approach",
]

# Hyperbolic terms to avoid (from Requirements 5.2)
HYPERBOLIC_TERMS = [
    "miracle",
    "cure",
    "100%",
    "guaranteed",
    "perfect",
    "instant",
    "overnight transformation",
    "completely eliminate",
]

# Generic opening patterns to avoid (from Requirements 6.1)
GENERIC_OPENING_PATTERNS = [
    r"^in this article",
    r"^today we",
    r"^welcome to",
    r"^let's talk about",
    r"^have you ever wondered",
]

# Hard-sell closing phrases to avoid (from Requirements 6.4)
HARD_SELL_PHRASES = [
    "click here",
    "buy now",
    "don't miss",
    "order today",
    "limited time",
    "act now",
]

# Common contractions for counting (from Requirements 3.2)
CONTRACTIONS = [
    "i'm", "i've", "i'll", "i'd",
    "you're", "you've", "you'll", "you'd",
    "he's", "he'll", "he'd",
    "she's", "she'll", "she'd",
    "it's", "it'll", "it'd",
    "we're", "we've", "we'll", "we'd",
    "they're", "they've", "they'll", "they'd",
    "that's", "that'll", "that'd",
    "who's", "who'll", "who'd",
    "what's", "what'll", "what'd",
    "where's", "where'll", "where'd",
    "when's", "when'll", "when'd",
    "why's", "why'll", "why'd",
    "how's", "how'll", "how'd",
    "isn't", "aren't", "wasn't", "weren't",
    "hasn't", "haven't", "hadn't",
    "doesn't", "don't", "didn't",
    "won't", "wouldn't",
    "can't", "couldn't",
    "shouldn't", "mightn't", "mustn't",
    "let's", "here's", "there's",
]


def check_forbidden_phrases(text: str) -> List[str]:
    """
    Check for AI-typical forbidden phrases in the text.
    
    Args:
        text: The article content to check
        
    Returns:
        List of forbidden phrases found in the text
    """
    text_lower = text.lower()
    found = []
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in text_lower:
            found.append(phrase)
    return found


def count_contractions(text: str) -> int:
    """
    Count the number of contractions in the text.
    Handles both straight apostrophes (') and curly apostrophes (').
    
    Args:
        text: The article content to check
        
    Returns:
        Count of contractions found
    """
    # Normalize curly apostrophes to straight apostrophes for matching
    text_normalized = text.replace("'", "'").replace("'", "'")
    text_lower = text_normalized.lower()
    count = 0
    for contraction in CONTRACTIONS:
        # Use word boundary matching to avoid partial matches
        pattern = r"\b" + re.escape(contraction) + r"\b"
        count += len(re.findall(pattern, text_lower))
    return count



def count_rhetorical_questions(text: str) -> int:
    """
    Count the number of rhetorical questions in the text.
    
    Args:
        text: The article content to check
        
    Returns:
        Count of sentences ending with question marks
    """
    # Count sentences ending with ?
    questions = re.findall(r'[^.!?]*\?', text)
    return len(questions)


def _split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences for analysis.
    
    Args:
        text: The text to split
        
    Returns:
        List of sentences
    """
    # Split on sentence-ending punctuation, keeping the delimiter
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Filter out empty strings and very short fragments
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 2]
    return sentences


def _count_words(sentence: str) -> int:
    """
    Count words in a sentence.
    
    Args:
        sentence: The sentence to count words in
        
    Returns:
        Word count
    """
    words = re.findall(r'\b\w+\b', sentence)
    return len(words)


def calculate_sentence_burstiness(text: str) -> float:
    """
    Calculate the standard deviation of sentence lengths within the text.
    Higher values indicate more dramatic variation (burstiness).
    
    Args:
        text: The article content to analyze
        
    Returns:
        Standard deviation of sentence lengths in words.
        Returns 0.0 if fewer than 2 sentences.
    """
    sentences = _split_into_sentences(text)
    
    if len(sentences) < 2:
        return 0.0
    
    word_counts = [_count_words(s) for s in sentences]
    
    # Filter out zero-length sentences
    word_counts = [c for c in word_counts if c > 0]
    
    if len(word_counts) < 2:
        return 0.0
    
    return statistics.stdev(word_counts)


def check_hyperbolic_claims(text: str) -> List[str]:
    """
    Check for hyperbolic terms that should be avoided.
    
    Args:
        text: The article content to check
        
    Returns:
        List of hyperbolic terms found in the text
    """
    text_lower = text.lower()
    found = []
    for term in HYPERBOLIC_TERMS:
        if term.lower() in text_lower:
            found.append(term)
    return found


def count_etsy_mentions(text: str) -> int:
    """
    Count occurrences of "Etsy" in the text.
    
    Args:
        text: The article content to check
        
    Returns:
        Count of "Etsy" mentions
    """
    # Case-insensitive count
    return len(re.findall(r'\betsy\b', text, re.IGNORECASE))


def check_generic_opening(text: str) -> bool:
    """
    Check if the article has a generic opening.
    
    Args:
        text: The article content to check
        
    Returns:
        True if the opening matches a generic pattern, False otherwise
    """
    # Get the first sentence or first 200 characters
    first_part = text[:200].lower().strip()
    
    for pattern in GENERIC_OPENING_PATTERNS:
        if re.search(pattern, first_part, re.IGNORECASE):
            return True
    return False


def check_generic_closing(text: str) -> bool:
    """
    Check if the article has a hard-sell closing.
    
    Args:
        text: The article content to check
        
    Returns:
        True if the closing contains hard-sell phrases, False otherwise
    """
    # Get the last paragraph (approximately last 500 characters)
    last_part = text[-500:].lower() if len(text) > 500 else text.lower()
    
    for phrase in HARD_SELL_PHRASES:
        if phrase.lower() in last_part:
            return True
    return False



# Sensory words for Property 5 validation
SENSORY_WORDS = [
    "texture", "smooth", "silky", "scent", "aroma", "feel",
    "soft", "rich", "creamy", "velvety", "buttery", "warm",
    "cool", "thick", "light", "heavy", "gentle", "rough",
    "dry", "moist", "oily", "greasy", "fresh", "clean",
]

# Emotional words for Property 5 validation
EMOTIONAL_WORDS = [
    "comfort", "relief", "confidence", "frustration", "finally",
    "love", "hate", "joy", "happy", "sad", "anxious", "calm",
    "excited", "worried", "hopeful", "disappointed", "satisfied",
    "grateful", "surprised", "amazed", "delighted", "pleased",
]

# Balancing phrases for Property 10 validation
BALANCE_INDICATORS = [
    "results vary",
    "not for everyone",
    "some people find",
    "in my experience",
    "your mileage may vary",
    "that said",
    "however",
    "although",
    "might not",
    "may not",
    "depends on",
    "individual",
    "varies",
]

# Messy transition markers for Property 13 validation
MESSY_TRANSITION_MARKERS = [
    "anyway",
    "actually",
    "speaking of",
    "i digress",
    "back to",
    "oh, and",
    "sorry",
    "where was i",
    "but anyway",
    "let me back up",
    "tangent",
    "off-topic",
    "sidetracked",
]

# Freshness markers for Property 14 validation
FRESHNESS_MARKERS = [
    "lately",
    "recently",
    "this season",
    "past few months",
    "this year",
    "just",
    "other day",
    "other week",
    "last month",
    "last week",
    "these days",
    "nowadays",
]


def count_sensory_words(text: str) -> int:
    """
    Count sensory words in the text.
    
    Args:
        text: The article content to check
        
    Returns:
        Count of sensory words found
    """
    text_lower = text.lower()
    count = 0
    for word in SENSORY_WORDS:
        pattern = r'\b' + re.escape(word) + r'\w*\b'
        count += len(re.findall(pattern, text_lower))
    return count


def count_emotional_words(text: str) -> int:
    """
    Count emotional words in the text.
    
    Args:
        text: The article content to check
        
    Returns:
        Count of emotional words found
    """
    text_lower = text.lower()
    count = 0
    for word in EMOTIONAL_WORDS:
        pattern = r'\b' + re.escape(word) + r'\w*\b'
        count += len(re.findall(pattern, text_lower))
    return count


def check_balanced_perspective(text: str) -> bool:
    """
    Check if the text contains balanced perspective indicators.
    
    Args:
        text: The article content to check
        
    Returns:
        True if at least one balancing phrase is found
    """
    text_lower = text.lower()
    for indicator in BALANCE_INDICATORS:
        if indicator.lower() in text_lower:
            return True
    return False


def check_messy_transitions(text: str) -> bool:
    """
    Check if the text contains messy transition markers for natural flow.
    
    Args:
        text: The article content to check
        
    Returns:
        True if at least one messy transition marker is found
    """
    text_lower = text.lower()
    for marker in MESSY_TRANSITION_MARKERS:
        if marker.lower() in text_lower:
            return True
    return False


def check_freshness_signals(text: str) -> bool:
    """
    Check if the text contains freshness/currency signals.
    
    Args:
        text: The article content to check
        
    Returns:
        True if at least one freshness marker is found
    """
    text_lower = text.lower()
    for marker in FRESHNESS_MARKERS:
        if marker.lower() in text_lower:
            return True
    return False


def validate_article(text: str) -> dict:
    """
    Run all quality checks on an article and return results.
    
    Args:
        text: The article content to validate
        
    Returns:
        Dictionary with validation results for each check
    """
    forbidden = check_forbidden_phrases(text)
    hyperbolic = check_hyperbolic_claims(text)
    
    return {
        "forbidden_phrases": forbidden,
        "forbidden_phrases_pass": len(forbidden) == 0,
        "contractions_count": count_contractions(text),
        "contractions_pass": count_contractions(text) >= 5,
        "rhetorical_questions_count": count_rhetorical_questions(text),
        "rhetorical_questions_pass": count_rhetorical_questions(text) >= 2,
        "sentence_burstiness": calculate_sentence_burstiness(text),
        "sentence_burstiness_pass": calculate_sentence_burstiness(text) > 8,
        "hyperbolic_claims": hyperbolic,
        "hyperbolic_claims_pass": len(hyperbolic) == 0,
        "etsy_mentions": count_etsy_mentions(text),
        "etsy_mentions_pass": count_etsy_mentions(text) <= 1,
        "generic_opening": check_generic_opening(text),
        "generic_opening_pass": not check_generic_opening(text),
        "generic_closing": check_generic_closing(text),
        "generic_closing_pass": not check_generic_closing(text),
        "sensory_words_count": count_sensory_words(text),
        "sensory_words_pass": count_sensory_words(text) >= 3,
        "emotional_words_count": count_emotional_words(text),
        "emotional_words_pass": count_emotional_words(text) >= 2,
        "balanced_perspective": check_balanced_perspective(text),
        "messy_transitions": check_messy_transitions(text),
        "freshness_signals": check_freshness_signals(text),
    }
