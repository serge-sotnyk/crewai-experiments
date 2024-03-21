from crewai import Agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from dotenv import load_dotenv

load_dotenv()

max_iterations_before_best_answer = 4
remember_prev_iterations = True

defalut_llm = ChatOpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
                        openai_api_key=os.environ.get("OPENAI_API_KEY"),
                        temperature=0,
                        # model_name=os.environ.get("MODEL_NAME", "gpt-4"),
                        model_name=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
                        top_p=0.3)

class PricingAgents():

  def competitor_research_agent(self):
    return Agent(
        role='Competitor Research Expert',
        goal='Identify the main competitors for a given product',
        backstory='An expert in market research and competitive analysis',
        max_iter=max_iterations_before_best_answer,
        memory=remember_prev_iterations,
        llm=defalut_llm,
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        verbose=True)

  def pricing_strategy_agent(self):
    return Agent(
        role='Pricing Strategy Expert',
        goal='Provide insights and suggestions for pricing based on the competitor pricing analysis',
        backstory='An experienced strategist with a deep understanding of pricing dynamics in the market',
        max_iter=max_iterations_before_best_answer,
        memory=remember_prev_iterations,
        llm=defalut_llm,
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        verbose=True)
