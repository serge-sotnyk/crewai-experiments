import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from tavily import TavilyClient

class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    tavily = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    print(f"Scraping website: {website}")
    results = tavily.search(website)

    summaries = []
    for result in results['results']:
      print(f"Showing scrape results: {result}")
      agent = Agent(
        role='Principal Researcher',
        goal=
        'Do amazing research and summaries based on the content you are working with',
        backstory=
        "You're a Principal Researcher at a big company and you need to do research about a given topic.",
        allow_delegation=False)
      task = Task(
        agent=agent,
        description=
        f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{result}',
        expected_output="Summary of the content"
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)
