import streamlit as st
from orchestrator import Orchestrator

st.set_page_config(page_title="RagaBro - Market Brief", layout="centered")
st.title("🎙️ RagaBro - AI Market Brief")

orch = Orchestrator()

if "last_brief" not in st.session_state:
    st.session_state.last_brief = ""
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

st.markdown("Click below to **speak your query** (e.g., `AAPL TSLA news`)")

if st.button("🎤 Start Voice Input"):
    with st.spinner("Listening and processing..."):
        result = orch.run()
        if result:
            st.session_state.last_brief = result
            st.session_state.last_query = orch.voice_agent.last_text if hasattr(orch.voice_agent, "last_text") else ""
        else:
            st.error("Sorry, I couldn't generate a response. Try again.")

# Optional: text input fallback (for testing or voice not working)
st.markdown("Or type a query directly:")
manual_query = st.text_input("Enter ticker symbols (e.g., AAPL TSLA)", "")

if manual_query:
    with st.spinner("Fetching and analyzing data..."):
        tickers = manual_query.upper().split()
        from agents.retriever_agent import build_index, retrieve_top_k
        from agents.analysis_agent import analyze_stock_data
        from agents.language_agent import generate_narrative

        build_index(tickers)
        top_chunks = retrieve_top_k(manual_query, k=3)

        if not top_chunks:
            st.error("No relevant news found.")
        else:
            combined_text = " ".join([chunk["text"] for chunk in top_chunks])
            analysis = analyze_stock_data(combined_text)
            narrative = generate_narrative(analysis)
            st.session_state.last_brief = narrative
            st.session_state.last_query = manual_query

# Output
if st.session_state.last_brief:
    st.subheader("📊 Market Brief")
    st.markdown(f"**Query:** {st.session_state.last_query}")
    st.success(st.session_state.last_brief)
