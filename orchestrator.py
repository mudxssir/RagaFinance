from agents.voice_agent import VoiceAgent
from agents.retriever_agent import build_index, retrieve_top_k
from agents.analysis_agent import analyze_stock_data
from agents.language_agent import generate_narrative

class Orchestrator:
    def __init__(self):
        self.voice_agent = VoiceAgent()
        
    def run(self) -> str | None:
        # 1. Get voice input
        query = self.voice_agent.speech_to_text()
        if not query:
            self.voice_agent.text_to_speech("Sorry, I did not catch that. Please try again.")
            return None
        
        # For demo, assume query contains tickers separated by spaces, e.g. "AAPL TSLA"
        tickers = query.upper().split()
        
        # 2. Build index (fetch & embed news for tickers)
        build_index(tickers)
        
        # 3. Retrieve top-k relevant chunks for the full query
        top_chunks = retrieve_top_k(query, k=3)
        
        if not top_chunks:
            self.voice_agent.text_to_speech("Couldn't find relevant news. Try again.")
            return None

        # 4. Combine texts into one string for analysis
        combined_text = " ".join([chunk["text"] for chunk in top_chunks])
        
        # 5. Analyze data
        analysis = analyze_stock_data(combined_text)
        
        # 6. Generate narrative
        narrative = generate_narrative(analysis)
        
        # 7. Speak and return narrative
        self.voice_agent.text_to_speech(narrative)
        return narrative

if __name__ == "__main__":
    orch = Orchestrator()
    output = orch.run()
    if output:
        print("Market Brief:", output)
