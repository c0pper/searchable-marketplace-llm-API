"""
Create a doc collection starting from a list of json objects (that might come from a db)
"""
import json
from pathlib import Path

from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os
from mongodb_connection import data

#  JSON data reading
# data = json.loads(Path("all_products.json").read_text())


def get_page_content(json_doc):
    #  Helper function to create the page_content property of Document class
    page_content = f'''name: {json_doc["name"]}\ndescription: {json_doc["description"]}\nprice per month: {json_doc["price"]}'''
    return page_content


docs = [Document(page_content=get_page_content(doc), metadata={"id": str(doc["_id"]), "url": doc["url"]}) for doc in data]

persist_directory = "db"
embeddings = HuggingFaceEmbeddings()

#  If embeddings database already exists > read it, else > create it
if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
    print("Directory 'db' exists. Using existing vectordb")
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

else:
    # pass
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    print("Directory 'db' does not exist. Creating new vectordb")
    db.persist()

if __name__ == '__main__':
    print(data)
    print(docs[1].page_content)
    # print(len(docs))

    if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
        print("Directory 'db' exists. Using existing vectordb")
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    else:
        # pass
        db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
        print("Directory 'db' does not exist. Creating new vectordb")
        db.persist()

    results = db.similarity_search_with_score("need backup service", k=4)
    print([x for x in results])
