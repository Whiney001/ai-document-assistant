import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import tempfile
import os

# Page setup
st.set_page_config(page_title="AI Document Assistant", page_icon="📄")
st.title("📄 AI Document Assistant")
st.write("Upload a PDF and ask questions about it!")

# Get API key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        
        with st.spinner("Reading your document..."):
            try:
                # Load and process PDF
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()
                
                # Split into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, 
                    chunk_overlap=200
                )
                chunks = text_splitter.split_documents(documents)
                
                # Create vector store
                embeddings = OpenAIEmbeddings()
                vectorstore = Chroma.from_documents(chunks, embeddings)
                
                # Create retriever
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                
                # Create LLM
                llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                
                st.success("✅ Document loaded! Ask your questions below.")
                
                # Question input
                question = st.text_input("Ask a question about your document:")
                
                if question:
                    with st.spinner("Thinking..."):
                        # Get relevant chunks
                        relevant_docs = retriever.invoke(question)
                        context = "\n\n".join([doc.page_content for doc in relevant_docs])
                        
                        # Create prompt
                        prompt = f"""Based on the following context, answer the question.
                        
Context: {context}

Question: {question}

Answer:"""
                        
                        # Get answer
                        response = llm.invoke(prompt)
                        st.write("**Answer:**")
                        st.write(response.content)
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
else:
    st.info("👆 Enter your OpenAI API key to get started")