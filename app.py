import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
import tempfile
import os
import shutil

# --- Page setup ---
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")
st.title(" AI Document Assistant")
st.write("Upload a PDF and ask any questions about its content.")

# --- API Key ---
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error(" Missing API key in Streamlit Secrets. Please contact the developer.")
    st.stop()

# --- File uploader ---
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("Processing your document..."):
        try:
            # Load PDF
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()

            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)

            # Use temporary directory for Chroma to avoid tenant error
            chroma_temp_dir = tempfile.mkdtemp()
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            vectorstore = Chroma.from_documents(
                chunks,
                embedding=embeddings,
                persist_directory=chroma_temp_dir
            )

            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )

            st.success(" Document processed successfully! You can now ask questions below.")

            # --- Question Input ---
            question = st.text_input("Ask a question about your document:")
            if question:
                with st.spinner("Thinking..."):
                    result = qa_chain({"query": question})
                    st.markdown("### 💬 Answer:")
                    st.write(result["result"])

                    # Show referenced document sections
                    with st.expander(" View source text"):
                        for i, doc in enumerate(result["source_documents"]):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.text(doc.page_content[:600] + "...")
                            st.markdown("---")

        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            # Clean up temporary files to prevent Streamlit errors
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            if os.path.exists(chroma_temp_dir):
                shutil.rmtree(chroma_temp_dir)

else:
    st.info("""
    **How to use this assistant:**
    1. Upload any PDF file  
    2. Wait for it to process  
    3. Ask your questions freely  
    """)
