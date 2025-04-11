from fuzzywuzzy import fuzz

def is_related(news_entities, fund_name):
    return any(fuzz.partial_ratio(ent.lower(), fund_name.lower()) > 80 for ent in news_entities)

