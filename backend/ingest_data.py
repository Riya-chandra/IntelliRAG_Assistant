import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import gdown


load_dotenv()
CHROMA_DB_PATH=os.getenv("CHROMA_DB_PATH","db")


# #load documents
documents=[
    Document(page_content="Meeting notes:Dicuss project X deliverables."),
    Document(page_content="Reminder: submit report by friday."),
    Document(page_content="upcoming event:tech confernce next wednesday.")
] 

# embeddings 
# beside teh chromaDB we can also stoe it to the pincode ..where we can visulaize the data but in chroma db we cant'
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 

text_splitter=RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=50)
docs=text_splitter.split_documents(documents)

vector_db = Chroma.from_documents(docs, embedding=embeddings, persist_directory=CHROMA_DB_PATH)
print("documents succesfully indexed!")