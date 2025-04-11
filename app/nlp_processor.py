import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")

def process_article(article):
    summary = summarizer(article["content"][:1000])[0]["summary_text"]
    ents = [ent.text for ent in nlp(article["content"]).ents]
    sentiment = sentiment_analyzer(article["content"][:512])[0]
    return {
        "summary": summary,
        "entities": ents,
        "sentiment": sentiment
    }