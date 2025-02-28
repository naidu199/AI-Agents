import json
from typing import List, Optional, Dict, Any

from phi.tools import Toolkit
from phi.utils.log import logger

try:
    from scholarly import scholarly
except ImportError:
    raise ImportError("`scholarly` not installed. Please install using `pip install scholarly`")


class GoogleScholarToolkit(Toolkit):
    def __init__(self, search_scholar: bool = True):
        super().__init__(name="google_scholar_tools")

        if search_scholar:
            self.register(self.search_scholar_and_return_articles)

    def search_scholar_and_return_articles(self, query: str, num_articles: int = 10) -> str:
        """Search Google Scholar for a query and return the top articles.

        Args:
            query (str): The search query.
            num_articles (int, optional): Number of articles to return. Defaults to 10.

        Returns:
            str: A JSON containing articles with title, authors, year, and link.
        """
        articles = []
        logger.info(f"Searching Google Scholar for: {query}")

        try:
            search_results = scholarly.search_pubs(query)
            for i, result in enumerate(search_results):
                if i >= num_articles:
                    break

                article: Dict[str, Any] = {
                    "title": result['bib'].get('title', 'Unknown Title'),
                    "authors": result['bib'].get('author', ['Unknown Authors']),
                    "year": result['bib'].get('pub_year', 'N/A'),
                    "link": result.get('pub_url', 'Not Available'),
                    "summary": result['bib'].get('abstract', 'No abstract available.')
                }
                articles.append(article)
        except Exception as e:
            logger.error(f"Error fetching research papers: {e}")
            return json.dumps({"error": str(e)}, indent=4)

        return json.dumps(articles, indent=4)
