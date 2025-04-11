from app.query_engine import answer_query

def test_answer_query():
    fund = "Nifty"
    result = answer_query(fund)
    assert "insights" in result