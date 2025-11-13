from transformers import pipeline
from utils.openai_client import llm
from utils.prompts import TONE_REWRITE_PROMPT

# one-time load
_sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

def analyze_sentiment(text: str):
    return _sentiment(text[:4800])  # keep it short for speed

def rewrite_tone(text: str, tone: str="persuasive"):
    prompt = TONE_REWRITE_PROMPT.format(tone=tone, content=text)
    return llm([{"role":"user","content":prompt}])
