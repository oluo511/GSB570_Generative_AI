from agents import TradingAdvisor
from tools import CryptoData, SentimentAnalyzer, WebSearch, Utils

def main():
    print("\n🔄 Testing CryptoData...")
    crypto_data = CryptoData()
    btc_price = crypto_data.get_price("bitcoin")
    print(f"BTC Price: {Utils.format_price(btc_price)}")

    print("\n🔄 Testing WebSearch...")
    web_search = WebSearch()
    search_results = web_search.search("Bitcoin price prediction")
    print("\nTop 5 Search Results:")
    print("\n".join(search_results))

    print("\n🔄 Testing SentimentAnalyzer...")
    sentiment_analyzer = SentimentAnalyzer()
    sentiment_results = sentiment_analyzer.analyze_sentiment("Bitcoin", max_results=5)
    print("\nTop 5 Sentiment Results:")
    print("\n".join(sentiment_results))

    print("\n🔄 Testing TradingAdvisor...")
    advisor = TradingAdvisor()
    advice = advisor.generate_advice("Bitcoin")
    print("\n💬 Trading Advice:")
    print(advice)

    print("\n✅ All Tests Complete")

if __name__ == "__main__":
    main()