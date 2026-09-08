import json

from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.models.database import AuditEvent
from app.services.analytics import AnalyticsService


class AIAssistant:
    def __init__(self, db: Session):
        self.db = db
        self.analytics = AnalyticsService(db)

    def _fallback_answer(self, question, data):
        q = question.lower()

        if "highest" in q and "revenue" in q and "product" in q:
            items = data["sales_by_product"]
            if items:
                top = items[0]
                return f"{top['product']} generated the highest revenue at {top['revenue']:,.2f}."

        if "region" in q and "revenue" in q:
            items = data["sales_by_region"]
            if items:
                top = items[0]
                return f"{top['region']} generated the highest revenue at {top['revenue']:,.2f}."

        if "month" in q and ("highest" in q or "best" in q):
            items = data["sales_by_month"]
            if items:
                top = max(items, key=lambda x: x["revenue"])
                return f"{top['month']} had the highest revenue at {top['revenue']:,.2f}."

        if "total sales" in q or "total revenue" in q:
            return (
                f"Total sales are {data['kpis']['total_sales']:,.2f} "
                f"across {data['kpis']['total_orders']} orders."
            )

        return (
            "Fallback mode could not map the question to a specific rule. "
            "The trusted analytics snapshot is available in the data field."
        )

    def ask(self, question):
        data = self.analytics.snapshot()

        if settings.openai_api_key:
            llm = ChatOpenAI(
                api_key=settings.openai_api_key,
                model=settings.openai_model,
                temperature=0,
            )

            prompt = f'''
You are a business analytics assistant.

Answer the user's question using ONLY the trusted analytical data below.
Do not invent numbers.
If the data is insufficient, say so clearly.
Keep the answer concise and business-friendly.

USER QUESTION:
{question}

TRUSTED ANALYTICS DATA:
{json.dumps(data, indent=2)}
'''

            response = llm.invoke(prompt)
            answer = response.content
        else:
            answer = self._fallback_answer(question, data)

        self.db.add(AuditEvent(event_type="ai_question", question=question))
        self.db.commit()

        return answer, data
