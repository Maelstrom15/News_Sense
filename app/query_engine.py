from app.openai_client import ask_openai

def answer_query(fund):
    news = scrape_moneycontrol()
    summaries = []

    for article in news:
        processed = process_article(article)
        save_article_to_db(article, processed)

        if is_related(processed["entities"], fund):
            summaries.append(f"- {processed['summary']} (Sentiment: {processed['sentiment']['label']})")

    context = "\n".join(summaries[:5])  # only top 5
    question = f"Why is {fund} down today?"

    if context:
        gpt_answer = ask_openai(question, context)
        return {
            "fund": fund,
            "context_used": summaries[:3],
            "gpt_response": gpt_answer
        }
    else:
        return {"fund": fund, "message": "No related news found."}
