from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.arxiv_toolkit import ArxivToolkit
from phi.tools.googlesearch import GoogleSearch
from scholarly_tool import GoogleScholarToolkit  # Import custom tool
from dotenv import load_dotenv

load_dotenv()

# Web Research Agent - General search
web_agent = Agent(
    name="web_research_agent",
    role="You are a web research agent that finds research papers.",
    model=Gemini(id="gemini-2.0-flash-exp"),
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
    model=Gemini(id="gemini-2.0-flash-exp"),
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
agent_team = Agent(
    name="agent_team",
    model=Gemini(id="gemini-2.0-flash-exp"),
    team=[web_agent, scholarly_arxiv_agent],
    instructions=[
        "1. Start by searching for general web information.",
        "2. Then fetch 10 research papers from Google Scholar and Arxiv.",
        "3. Ensure all research papers have clickable links.",
        "4. Use structured tables for clarity.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Run the Agent
agent_team.print_response("Give me tricky situations or problems that confuse human brain , like something based on psychology", stream=True)
