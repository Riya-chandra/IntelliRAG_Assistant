import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

# NEW import for HuggingFace LLM
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

load_dotenv()
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "db")

# 1) Load embeddings (correct)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2) Load Vector DB
vector_db = Chroma(persist_directory=CHROMA_DB_PATH,embedding_function=embeddings)
retriever = vector_db.as_retriever()

# 3) Initialize HuggingFace LLM (THIS WAS MISSING)
hf_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",      # LLM
    max_new_tokens=200,
    temperature=0.2
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# 4) Create QA chain
qa_chain = load_qa_chain(llm, chain_type="stuff")

rag = RetrievalQA(
    retriever=retriever,
    combine_documents_chain=qa_chain
)

# 5) Ask a question
query = "What are my meeting notes?"
answer = rag.run(query)

print("Answer:", answer)

def get_response(query):
    docs = retriever.get_relevant_documents(query)
    return qa_chain.run(input_documents=docs, question=query)
