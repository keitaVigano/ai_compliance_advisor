import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from src.pipeline import graph  # Import the compiled graph from your orchestrator

# Configurazione iniziale dell'app Streamlit
st.set_page_config(
    page_title="Agentic RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 Agentic RAG Chatbot")
st.markdown(
    """
    Welcome to the **Agentic Retrieval-Augmented Generation (RAG) Chatbot**!
    Ask questions, and the chatbot will fetch relevant documents, analyze them, and generate concise responses.
    """
)

# Sidebar con istruzioni
with st.sidebar:
    st.header("How it works:")
    st.markdown(
        """
        1. Enter your query in the text box.
        2. The chatbot processes your query using an agentic pipeline.
        3. It retrieves documents, checks relevance, and generates an answer.
        4. If something fails, you'll be asked to try a new question.
        """
    )
    st.markdown("---")
    st.markdown("### Example Queries:")
    st.markdown("- What does the GDPR regulate?")
    st.markdown("- What are the principles of GDPR?")
    st.markdown("- Who needs to comply with GDPR?")
    st.markdown("---")
    st.info("💡 Use this interface to explore the capabilities of the RAG pipeline!")

# Input per la domanda
query = st.text_input("💬 Enter your question:", value="")

# Spazi per l'output
st.markdown("### Intermediate Steps:")
intermediate_steps = st.empty()

st.markdown("### Final Answer:")
final_answer = st.empty()

# Esegui il flusso RAG
if st.button("Submit Query") and query.strip():
    st.info("Processing your query... Please wait.")
    inputs = {"messages": [HumanMessage(content=query)]}
    outputs = []
    try:
        # Esegui la pipeline e mostra i passi intermedi
        for output in graph.stream(inputs):
            for key, value in output.items():
                outputs.append((key, value))
                intermediate_steps.markdown(
                    f"#### Node: `{key}`\n```json\n{value}\n```", unsafe_allow_html=True
                )

        # Estrai la risposta finale
        if outputs:
            final = outputs[-1]
            response = final[1].get("response", None)
            if response:
                final_answer.markdown(f"**Response:** {response}")
            else:
                final_answer.error("⚠️ Unable to generate a response.")
        else:
            final_answer.error("⚠️ No output generated by the pipeline.")

    except Exception as e:
        # Gestione degli errori: Mostra il messaggio e interrompi
        st.error(f"An error occurred: {e}")
        st.warning("⚠️ Something went wrong. Please try asking another question.")

# Chiedi all'utente se vuole continuare
st.markdown("---")
if st.button("Ask Another Question"):
    st.experimental_rerun()  # Ricarica la pagina per un nuovo ciclo