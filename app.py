import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

# Page config
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")

# Custom CSS
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

# Initialize session state
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

# Constants
MAX_QUERIES = 3

# Get API key from Streamlit secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    st.error("Configuration error. Please contact the developer.")
    st.stop()

# Header
st.title("AI Document Assistant")
st.markdown("### Upload a PDF and ask questions about it!")

# Demo banner
st.markdown(f"""
<div class="demo-banner">
    <h4 style="margin:0; color:#1a1a1a;">Demo Mode</h4>
    <p style="margin:0.5rem 0 0 0; color:#6b6b6b;">
        This is a live demonstration. You have <strong>{MAX_QUERIES - st.session_state.query_count}</strong> free queries remaining.
    </p>
    <p style="margin:0.3rem 0 0 0; font-size:0.9rem; color:#9ba3b1;">
        Built with LangChain, OpenAI, and Streamlit | 
        <a href="https://github.com/Whiney001/ai-document-assistant" target="_blank" style="color:#ff6b9d;">View Source Code</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Query counter
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="query-counter">
        Queries Used: {st.session_state.query_count}/{MAX_QUERIES}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", help="Upload any PDF document to analyze")

if uploaded_file is not None:
    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    
    # Process document if not already processed
    if st.session_state.vectorstore is None:
        with st.spinner("Reading and processing your document..."):
            try:
                # Load PDF
                loader = PyPDFLoader(tmp_file_path)
                documents = loader.load()
                
                # Split into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                texts = text_splitter.split_documents(documents)
                
                # Create embeddings and vector store
                embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
                vectorstore = Chroma.from_documents(texts, embeddings)
                
                # Create QA chain
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
                
                # Store in session state
                st.session_state.vectorstore = vectorstore
                st.session_state.qa_chain = qa_chain
                
                st.success(f"Document processed! Found {len(documents)} pages. You can now ask questions!")
                
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")
                st.stop()
            finally:
                # Clean up temp file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
    
    # Question input
    st.markdown("### Ask a Question")
    
    # Check if queries exceeded
    if st.session_state.query_count >= MAX_QUERIES:
        st.warning("You've reached the maximum number of demo queries. This is a portfolio demonstration project.")
        st.info("""
        **Want unlimited access?**
        - View the [source code on GitHub](https://github.com/Whiney001/ai-document-assistant)
        - Contact me for a full demonstration: kennethwinniefred746@gmail.com
        - This app was built with LangChain, OpenAI API, and Streamlit
        """)
    else:
        question = st.text_input(
            "What would you like to know about this document?",
            placeholder="e.g., What is the main topic of this document?",
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("Ask", use_container_width=True)
        
        if ask_button and question:
            if st.session_state.qa_chain is None:
                st.error("Please upload a document first!")
            else:
                with st.spinner("Thinking..."):
                    try:
                        # Get answer
                        result = st.session_state.qa_chain({"query": question})
                        
                        # Increment query count
                        st.session_state.query_count += 1
                        
                        # Display answer
                        st.markdown("### Answer")
                        st.write(result['result'])
                        
                        # Display sources
                        with st.expander("View Source Sections"):
                            for i, doc in enumerate(result['source_documents']):
                                st.markdown(f"**Source {i+1}:**")
                                st.text(doc.page_content[:300] + "...")
                                st.markdown("---")
                        
                        # Show remaining queries
                        remaining = MAX_QUERIES - st.session_state.query_count
                        if remaining > 0:
                            st.info(f"You have {remaining} demo queries remaining.")
                        else:
                            st.warning("Demo limit reached. Thanks for trying out my project!")
                            
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
        
        elif ask_button:
            st.warning("Please enter a question first!")

else:
    # Instructions when no file uploaded
    st.info("""
    **Get Started:**
    1. Upload a PDF document using the file uploader above
    2. Wait for the document to be processed
    3. Ask up to 3 questions about the content (demo limit)
    
    **Example questions:**
    - "What is the main topic of this document?"
    - "Can you summarize the key points?"
    - "What are the conclusions mentioned?"
    """)
    
    # Example use cases
    st.markdown("### Use Cases")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Research Papers**
        - Quick paper summaries
        - Find specific methodology
        - Extract key findings
        """)
    
    with col2:
        st.markdown("""
        **Business Reports**
        - Financial data extraction
        - Performance metrics
        - Strategic insights
        """)
    
    with col3:
        st.markdown("""
        **Study Materials**
        - Concept explanations
        - Quick Q&A
        - Chapter summaries
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ba3b1; font-size: 0.9rem;">
    <p>Built by <strong>Winnie Kenneth</strong> | Final-Year Computer Science Student at University of Hull</p>
    <p>
        <a href="https://whiney001.github.io" target="_blank" style="color: #ff6b9d; text-decoration: none;">Portfolio</a> | 
        <a href="https://github.com/Whiney001" target="_blank" style="color: #ff6b9d; text-decoration: none;">GitHub</a> | 
        <a href="https://linkedin.com/in/winnie-kenneth-28a862287" target="_blank" style="color: #ff6b9d; text-decoration: none;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
