from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

load_dotenv()


web_agent=Agent(
	name="web_agent",
 	role="search the web",
 	# model=Groq(id="llama-3.3-70b-versatile"),
    model=Gemini(id="gemini-2.0-flash-exp"),
  	tools=[DuckDuckGo()],
    show_tool_calls=True,
    instructions=["Always include sources"],
    markdown=True,


)

finance_agent=Agent(
	name="finance_agent",
     # model=Groq(id="llama-3.3-70b-versatile"),
    role="get financial information",
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True)],
	show_tool_calls=True,
	markdown=True,
    instructions=["Use Tables to display the data"],
)


agent_team = Agent(
    # model=Groq(id="llama-3.3-70b-versatile"),
    name="agent_team",
    model=Gemini(id="gemini-2.0-flash-exp"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("Summarize analyst recommendations and share the latest news for Google", stream=True)
