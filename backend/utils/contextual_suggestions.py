import json
import re
from collections import defaultdict, Counter
from pathlib import Path
from typing import List


# ----------------------------
# CONFIG
# ----------------------------

N = 3  # Trigram model


# ----------------------------
# TEXT CLEANING
# ----------------------------

def normalize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.split()


# ----------------------------
# LOAD CHAT HISTORY
# ----------------------------

def load_sentences(path: Path) -> List[List[str]]:
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    sentences = []

    for item in data:
        msg = item.get("message", "")
        tokens = normalize(msg)
        if len(tokens) >= N:
            sentences.append(tokens)

    return sentences


# ----------------------------
# BUILD N-GRAM MODEL
# ----------------------------

def build_ngram_model(sentences: List[List[str]]) -> dict:
    model = defaultdict(Counter)

    for tokens in sentences:
        for i in range(len(tokens) - N + 1):
            prefix = tuple(tokens[i:i + N - 1])
            next_word = tokens[i + N - 1]
            model[prefix][next_word] += 1

    return model


# ----------------------------
# AUTOCOMPLETE CORE
# ----------------------------

def autocomplete(model, user_input: str, max_words: int = 10) -> str:
    tokens = normalize(user_input)

    if len(tokens) < N - 1:
        return ""

    prefix = tuple(tokens[-(N - 1):])
    suggestion = []

    for _ in range(max_words):
        if prefix not in model:
            break

        next_word = model[prefix].most_common(1)[0][0]
        suggestion.append(next_word)
        prefix = (*prefix[1:], next_word)

    return " ".join(suggestion)


# ----------------------------
# PUBLIC FUNCTION (USED BY ContextLoader)
# ----------------------------

def get_contextual_suggestion(
    chat_history_path: Path,
    user_input: str,
    max_words: int = 10
) -> str:
    """
    Returns a contextual text suggestion based on chat history.
    This function is meant to be called from ContextLoader.
    """
    sentences = load_sentences(chat_history_path)
    if not sentences:
        return ""

    model = build_ngram_model(sentences)
    return autocomplete(model, user_input, max_words)
