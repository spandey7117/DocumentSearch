from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from docx import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "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"


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