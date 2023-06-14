from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import json
from pathlib import Path
import pprint

# loader = DirectoryLoader('./docs', glob="**/*.txt", show_progress=True)
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)


data = json.loads(Path("all_products.json").read_text())

def get_page_content(json_doc):
    page_content = f'''name: {json_doc["name"]}\ndescription: {json_doc["description"]}\nprice: {json_doc["price"]}'''
    return page_content


docs = [Document(page_content=get_page_content(x), metadata={"id": x["_id"], "url": x["url"]}) for x in data]

if __name__ == '__main__':
    print(data)
    print(docs[1].page_content)
    # print(len(docs))

