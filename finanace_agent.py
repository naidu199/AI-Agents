from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.google import Gemini
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()


def get_company_symbol(company: str) -> str:
    """Use this function to get the symbol for a company.

    Args:
        company (str): The name of the company.

    Returns:
        str: The symbol for the company.
    """
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
    }
    return symbols.get(company, "Unknown")


agent = Agent(
    		# model=Groq(id="llama-3.3-70b-versatile"),
        	model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True),get_company_symbol],
            show_tool_calls=True,
            markdown=True,
            instructions=["Use Tables to display the data, if u cant find the data use this function get_company_symbol"],
            debug_mode=True,
	)
agent.print_response("Analysis the stock of the Phidata")

