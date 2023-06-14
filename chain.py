from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os
import textwrap
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from ingest import docs


persist_directory = "db"
embeddings = HuggingFaceEmbeddings()
if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
    print("Directory 'db' exists. Using existing vectordb")
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

else:
    # pass
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    print("Directory 'db' does not exist. Creating new vectordb")
    db.persist()


def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text


def process_llm_response(llm_response, scores):

    response = wrap_text_preserve_newlines(llm_response['result'])
    print(response)


    print('\n\nSources:')
    sources = []
    for idx, source in enumerate(llm_response["source_documents"]):
        print(source.page_content)
        print(source.metadata)
        print("\n----\n")
        source_data = {
            "page_content": source.page_content,
            "metadata": source.metadata,
            "score": scores[idx]
        }
        sources.append(source_data)
    #
    # return wrap_text_preserve_newlines(llm_response['result'])
    return {"generative_reply": response, "sources": sources}




def ask_llm(question: str):
    prompt_template = """Use the following texts from a database of cloud products and services to reply to the user question. Try to explain the advantages and disadvantages of each service you propose"
    Texts:
    {context}
    User question: {question}
    Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    desired_results = 4
    chain_type_kwargs = {"prompt": PROMPT}
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                           chain_type="stuff",
                                           retriever=db.as_retriever(search_kwargs={"k": desired_results}),
                                           return_source_documents=True,
                                           chain_type_kwargs=chain_type_kwargs)

    similarity = db.similarity_search_with_score(question, k=desired_results)  # The returned distance score is L2 distance. Therefore, a lower score is better.
    scores = [x[1] for x in similarity]

    llm_response = qa_chain(question)
    llm_response = process_llm_response(llm_response, scores)

    return llm_response


if __name__ == '__main__':
    if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
        print("Directory 'db' exists. Using existing vectordb")
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    else:
        # pass
        db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
        print("Directory 'db' does not exist. Creating new vectordb")
        db.persist()

    results = db.similarity_search_with_score("need backup service", k=4)
    print([x[1] for x in results])