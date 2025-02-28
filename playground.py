from phi.agent import Agent
# from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.model.google import Gemini
from phi.playground import Playground, serve_playground_app
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.tools.googlesearch import GoogleSearch
from scholarly_tool import GoogleScholarToolkit

web_agent = Agent(
    name="Web Agent",
    # model=Gemini(id="gemini-2.0-pro"),
     model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo(),GoogleSearch()],
    instructions=["Always include sources"],
    storage=SqlAgentStorage(table_name="web_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    # model=Gemini(id="gemini-2.0-pro"),
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
    storage=SqlAgentStorage(table_name="finance_agent", db_file="agents.db"),
    add_history_to_messages=True,
    markdown=True,
)
web_research_agent = Agent(
    name="web_research_agent",
    role="You are a web research agent that finds research papers.",
    # model=Gemini(id="gemini-2.0-pro"),
     model=Groq(id="llama-3.3-70b-versatile"),
    tools=[GoogleSearch(timeout=20)],
    show_tool_calls=True,
    instructions=[
        "- Search for information related to the topic.",
        "- Always include source links.",
        "- Prioritize research from India first, then globally.",
    ],
    markdown=True,
)

# Academic Research Agent - Finds scholarly papers
scholarly_arxiv_agent = Agent(
    name="scholarly_research_agent",
    role="Retrieve academic research from Google Scholar and Arxiv.",
    # model=Gemini(id="gemini-2.0-pro"),
     model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        ArxivToolkit(search_arxiv=True),  # Fetches papers from Arxiv
        GoogleScholarToolkit(search_scholar=True),  # Fetches papers from Google Scholar
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "- Fetch 10 research papers from Google Scholar and Arxiv.",
        "- Provide title, authors, year, link, and summary.",
        "- Display results in a structured table format.",
    ],
)

# Team of Agents - Runs both searches
research_agent = Agent(
    name="Research Agent",
    # model=Gemini(id="gemini-2.0-pro"),
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[
        web_research_agent,
        #   scholarly_arxiv_agent
          ],
    instructions=[
        "1. Start by searching for general web information.",
        "2. Then fetch 5 research papers from Google Scholar and Arxiv.",
        "3. Ensure all research papers have clickable links.",
        "4. Use structured tables for clarity.",
    ],
    show_tool_calls=True,
    storage=SqlAgentStorage(table_name="research_agent", db_file="agents.db"),
    markdown=True,
)
app = Playground(agents=[finance_agent, web_agent,research_agent,web_research_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
