import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
import tempfile, os, shutil

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    body {background-color:#0b0f16; color:#e8edf2;}
    .main {background-color:#0b0f16;}
    h1,h2,h3,h4 {color:#fff;}
    .css-1cpxqw2, .stTextInput>div>div>input {color:#fff !important;}
    .stButton>button {
        background:linear-gradient(135deg,#ff6b9d,#e5527e);
        border:none;color:white;padding:0.6rem 1.6rem;
        border-radius:8px;font-weight:600;
        transition:all .3s;
    }
    .stButton>button:hover {transform:translateY(-2px);
        box-shadow:0 4px 15px rgba(255,107,157,0.3);}
    .banner {
        background:linear-gradient(135deg,#ff6b9d 0%,#e5527e 40%,#6366f1 100%);
        padding:1.2rem;border-radius:14px;text-align:center;
        color:#fff;margin-bottom:1.5rem;box-shadow:0 5px 20px rgba(0,0,0,0.25);
    }
    .footer {text-align:center;color:#9ba3b1;font-size:0.9rem;margin-top:2rem;}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="banner">
    <h2>📄 AI Document Assistant</h2>
    <p>Built by <b>Winnie Kenneth</b> – Final-Year Computer Science Student, University of Hull</p>
</div>
""", unsafe_allow_html=True)

# -------------------- API KEY --------------------
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ Missing OpenAI API key in Streamlit Secrets.")
    st.stop()

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("🔍 Processing your document..."):
        try:
            # load pdf
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

            # split text
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            # temp folder for chroma to prevent tenant error
            chroma_tmp = tempfile.mkdtemp()
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            vectorstore = Chroma.from_documents(
                chunks, embedding=embeddings, persist_directory=chroma_tmp
            )

            # retrieval + llm
            retriever = vectorstore.as_retriever(search_kwargs={"k":3})
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
            qa = RetrievalQA.from_chain_type(
                llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
            )

            st.success(f"✅ Document processed ({len(docs)} pages). Ask your questions below!")

            # QUESTION INPUT
            question = st.text_input("💬 Ask a question about your document:")

            if question:
                with st.spinner("Thinking..."):
                    result = qa({"query": question})
                    st.markdown("### ✨ Answer")
                    st.write(result["result"])

                    with st.expander("📚 Source text used"):
                        for i, doc in enumerate(result["source_documents"]):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.text(doc.page_content[:600] + "...")
                            st.markdown("---")

        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)
            if os.path.exists(chroma_tmp): shutil.rmtree(chroma_tmp)

else:
    st.info("""
    **How to use**
    1. Upload a PDF document  
    2. Wait for it to be processed  
    3. Ask any question – summaries, insights, or keyword lookups  
    """)

# -------------------- FOOTER --------------------
st.markdown("""
<div class="footer">
    <p>Powered by LangChain ⚙️ OpenAI 🤖 Streamlit ☁️</p>
    <p>
        <a href="https://whiney001.github.io" style="color:#ff6b9d;">Portfolio</a> |
        <a href="https://github.com/Whiney001" style="color:#ff6b9d;">GitHub</a> |
        <a href="https://linkedin.com/in/winnie-kenneth-28a862287" style="color:#ff6b9d;">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
