from crewai import Crew, Process
from langchain.chat_models import ChatOpenAI
from textwrap import dedent
from agents import PricingAgents
from tasks import PricingTasks
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class PricingCrew:

  def __init__(self, product):
    self.product = product

  def run(self):
    agents = PricingAgents()
    listOfTasks = PricingTasks()

    competitor_research_agent = agents.competitor_research_agent()
    pricing_strategy_agent = agents.pricing_strategy_agent()

    competitor_research_task = listOfTasks.competitor_research_task(
      competitor_research_agent, self.product
    )

    pricing_strategy_task = listOfTasks.pricing_strategy_task(
      pricing_strategy_agent, self.product, competitor_research_task
    )

    crewResearch = Crew(
      agents=[competitor_research_agent, pricing_strategy_agent],
      tasks=[competitor_research_task, pricing_strategy_task],
      verbose=True
    )

    research_result = crewResearch.kickoff()

    return research_result

if __name__ == "__main__":
    print("## Welcome to Pricing Crew")
    print('-------------------------------')

    product = input(
        dedent("""
            What product are you interested in researching?
        """))

    pricing_crew = PricingCrew(product)
    result = pricing_crew.run()

    print("\n\n########################")
    print("## Here is your Pricing Research Result")
    print("########################\n")
    print(result)

    # Remove whitespaces from product
    product = product.replace(' ', '')
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')

    # Save the results in a Markdown file
    with open(f'competitors/{product}_{timestamp}.md', 'w') as f:
        f.write("# Pricing Research Result\n")
        f.write("## Product\n")
        f.write(f"{product}\n")
        f.write("## Result\n")
        f.write(f"{result}\n")
