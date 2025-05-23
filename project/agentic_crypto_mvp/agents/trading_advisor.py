from tools import WebSearch
from llm import get_bedrock_llm
from agent_base import AgentBase

class TradingAdvisor(AgentBase):
    def __init__(self, name="strategist"):
        super().__init__(name)
        self.web_search = WebSearch()
        self.llm = get_bedrock_llm()

    def generate_advice(self, asset):
        # Use the LLM to generate trading advice
        prompt = f"Generate a trading advice for the asset: {asset}"
        response = self.llm(prompt)
        return response.strip()

    def summarize_whitepaper(self, asset):
        # Search for the whitepaper
        search_results = self.web_search.search_whitepaper(asset)
        if not search_results:
            return f"No whitepaper found for {asset}."

        # Get the first relevant link
        whitepaper_link = search_results[0]['link']
        print(f"🔗 Found whitepaper link: {whitepaper_link}")

        # Summarize the whitepaper using the LLM
        prompt = f"Summarize the whitepaper found here: {whitepaper_link}"
        summary = self.llm(prompt)
        return summary.strip()

# Testing the TradingAdvisor
if __name__ == "__main__":
    advisor = TradingAdvisor(name="whitepaper_analyst")
    print(advisor.summarize_whitepaper("Ethereum"))