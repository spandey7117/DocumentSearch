from PyPDF2 import PdfReader
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from docx import Document
from langchain.chains.question_answering import load_qa_chain
from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
from langchain.agents import *
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
import psycopg2


load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


def connect_to_db():
    db = SQLDatabase.from_uri(f"postgresql://naardic:password@localhost:5432/template1")
    return db


def chat_with_db(query):
    print(query)
    db = SQLDatabase.from_uri(f"postgresql://naardic:password@localhost:5432/template1")
    llm = OpenAI(model_name="gpt-4")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    result = agent_executor.run(query)
    return result


def read_pdf(file_path):
    raw_text = ''
    pdf_reader = PdfReader(file_path)
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text


def read_doc(file_path):
    raw_text = ''
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        raw_text += paragraph.text + '\n'
    return raw_text


def read_txt(file_path):
    raw_text = ''
    with open(file_path, 'r') as f:
        raw_text += f.read()
    return raw_text


def respond_to_query(raw_text, query):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    embeddings = OpenAIEmbeddings()
    document_search = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    docs = document_search.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    return result

# def get_response_from_file(file_name, query):
#     if