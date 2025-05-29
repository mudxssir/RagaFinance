import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize model and FAISS index globally (for simplicity)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384  # embedding dimension for all-MiniLM-L6-v2

# In-memory store for documents and index
corpus = []     # List[str], holds text chunks
corpus_meta = []  # List[str], metadata like ticker + snippet id
index = faiss.IndexFlatL2(dimension)

def build_index(tickers: List[str]):
    """
    Fetch news, embed and build FAISS index for given tickers.
    """
    global corpus, corpus_meta, index
    corpus.clear()
    corpus_meta.clear()
    index.reset()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    for ticker in tickers:
        try:
            url = f"https://www.google.com/search?q={ticker}+stock+news&hl=en&tbm=nws"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            news_items = soup.select("div.dbsr")[:10]  # get more news

            for i, item in enumerate(news_items):
                title = item.select_one("div.JheGif.nDgy9d")
                snippet = item.select_one("div.Y3v8qd")
                if title and snippet:
                    text = f"{title.text.strip()}. {snippet.text.strip()}"
                    corpus.append(text)
                    corpus_meta.append(f"{ticker}_news_{i}")

            # Build embeddings and index after collecting all
            if corpus:
                embeddings = embed_model.encode(corpus, convert_to_numpy=True)
                index.add(embeddings)

        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")

def retrieve_top_k(query: str, k: int = 3) -> List[Dict]:
    """
    Embed the query, search FAISS, return top-k matched chunks with metadata.
    """
    if index.ntotal == 0:
        return []

    query_emb = embed_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, k)
    results = []

    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(corpus):
            results.append({
                "text": corpus[idx],
                "metadata": corpus_meta[idx],
                "distance": float(dist)
            })

    return results

# Example usage
if __name__ == "__main__":
    test_tickers = ["AAPL", "TSLA"]
    build_index(test_tickers)
    query = "Apple stock earnings and news"
    top_chunks = retrieve_top_k(query, k=3)
    for chunk in top_chunks:
        print(chunk)
