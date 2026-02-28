from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

_search = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the internet for current, real-time information.
    Use this to answer questions about recent events, verify facts,
    or retrieve up-to-date data."""
    return _search.run(query)


tools = [web_search]
