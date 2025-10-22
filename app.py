import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

# --- Streamlit Page Setup ---
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
    .main {background-color: #fdf8f6;}
    .stButton>button {
        background: linear-gradient(135deg, #ff6b9d, #e5527e);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,107,157,0.3);
    }
    .demo-banner {
        background: linear-gradient(135deg, rgba(255,107,157,0.1), rgba(99,102,241,0.1));
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #ffe4ee;
        margin-bottom: 1rem;
        text-align: center;
    }
    .query-counter {
        background: #fff5f2;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid #ffe4ee;
        display: inline-block;
        font-weight: 600;
        color: #ff6b9d;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

MAX_QUERIES = 3  # demo limit

# --- API Key Setup ---
# Instead of asking recruiters, you’ll use your private key stored in Streamlit Secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception as e:
    st.error("⚠️ Missing API key configuration. Please contact the developer (kennethwinniefred746@gmail.com).")
    st.stop()

# --- Header ---
st.title("📄 AI Document Assistant")
st.markdown("### Upload a PDF and ask questions about it!")

# --- Demo Banner ---
st.markdown(f"""
<div class="demo-banner">
    <h4 style="margin:0; color:#1a1a1a;">Live Demo Mode</h4>
    <p style="margin:0.5rem 0 0 0; color:#6b6b6b;">
        You have <strong>{MAX_QUERIES - st.session_state.query_count}</strong> free demo queries remaining.
    </p>
    <p style="margin:0.3rem 0 0 0; font-size:0.9rem; color:#9ba3b1;">
        Built with LangChain, OpenAI, and Streamlit |
        <a href="https://github.com/Whiney001/ai-document-assistant" target="_blank" style="color:#ff6b9d;">View Source Code</a>
    </p>
</div>
""", unsafe_allow_html=True)

# --- Query Counter ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="query-counter">
        Queries Used: {st.session_state.query_count}/{MAX_QUERIES}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- File Upload ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    if st.session_state.vectorstore is None:
        with st.spinner("Reading and processing your document..."):
            try:
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()

                # Split into chunks
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=200
                )
                texts = splitter.split_documents(documents)

                # Embeddings + Vector DB (in-memory fix for Streamlit)
                embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
                vectorstore = Chroma.from_documents(
                    texts,
                    embeddings,
                    persist_directory=None  # in-memory only
                )

                llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0,
                    openai_api_key=OPENAI_API_KEY
                )

                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
                    return_source_documents=True
                )

                # Store session objects
                st.session_state.vectorstore = vectorstore
                st.session_state.qa_chain = qa_chain

                st.success(f"✅ Document processed successfully! {len(documents)} pages loaded.")
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                st.stop()
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    # --- Ask a Question ---
    st.markdown("### Ask a Question")

    if st.session_state.query_count >= MAX_QUERIES:
        st.warning("You’ve reached the demo limit (3 questions).")
        st.info("""
        Want to explore further?
        - View [Source Code](https://github.com/Whiney001/ai-document-assistant)
        - Email: kennethwinniefred746@gmail.com for collaboration inquiries.
        """)
    else:
        question = st.text_input(
            "What would you like to know?",
            placeholder="e.g., Summarize this document"
        )
        if st.button("Ask"):
            if question:
                with st.spinner("Thinking..."):
                    try:
                        result = st.session_state.qa_chain({"query": question})
                        st.session_state.query_count += 1

                        st.markdown("### 💬 Answer")
                        st.write(result['result'])

                        with st.expander("📑 Source Context"):
                            for i, doc in enumerate(result['source_documents']):
                                st.markdown(f"**Source {i+1}:**")
                                st.text(doc.page_content[:400] + "...")
                                st.markdown("---")

                        remaining = MAX_QUERIES - st.session_state.query_count
                        if remaining > 0:
                            st.info(f"You have {remaining} demo queries left.")
                        else:
                            st.warning("Demo limit reached. Refresh to restart!")
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
            else:
                st.warning("Please enter a question first!")

else:
    st.info("""
    **How to Use**
    1. Upload any PDF file  
    2. Wait for it to process  
    3. Ask up to 3 questions about the document (demo limit)
    
    **Example questions:**
    - “Summarize the document.”
    - “What are the key findings?”
    - “Who are the main authors or stakeholders?”
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#9ba3b1; font-size:0.9rem;">
  <p>Built by <strong>Winnie Kenneth</strong> | Final-Year BSc Computer Science Student at University of Hull</p>
  <p>
    <a href="https://whiney001.github.io" target="_blank" style="color:#ff6b9d;">Portfolio</a> |
    <a href="https://github.com/Whiney001" target="_blank" style="color:#ff6b9d;">GitHub</a> |
    <a href="https://linkedin.com/in/winnie-kenneth-28a862287" target="_blank" style="color:#ff6b9d;">LinkedIn</a>
  </p>
</div>
""", unsafe_allow_html=True)
