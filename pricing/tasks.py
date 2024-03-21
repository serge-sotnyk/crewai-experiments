from crewai import Task
from textwrap import dedent

class PricingTasks:
    def competitor_research_task(self, agent, product):
        return Task(
            description=dedent(f"""
                Your task is to identify the main competitors for the given product.
                You should provide a list of 5-10 competitors and a brief description of their product offerings and prices for those.
                Product: {product}
            """),
            expected_output="List of competitors, their product offerings, website urls and prices (subscription, membership costs)."
                            "Return json object with keys: 'name', 'description', 'url', 'price'",
            agent=agent
        )

    def pricing_strategy_task(self, agent, product, competitor_research_task):
        return Task(
            description=dedent(f"""
                Based on the competitor research pricing analysis, your task is to assign price for the given product.
                You should consider factors like market trends, product features, and cost of production.
                Provide justification for the pricing strategy.
                Product: {product}
                Competitor Research Output: {competitor_research_task.output}
            """),
            expected_output="Defined pricing strategy for the product, prices included. Return formatted markdown text.",
            agent=agent,
            context=[competitor_research_task]
        )
