import getpass
import bs4
from flask import Flask, request
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import os
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from flask_cors import CORS  # Add this import


app=Flask(__name__)
CORS(app)

os.environ["GOOGLE_API_KEY"] = 'AIzaSyDwsn96yTHaNnDcVFPqFsaQNUZ4xtS_igs'
os.environ['USER_AGENT'] = "MyRagBot/1.0 (contact@example.com)"

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)

# AIzaSyDwsn96yTHaNnDcVFPqFsaQNUZ4xtS_igs


loader = WebBaseLoader(
    web_paths=("https://student.central.edu.gh/Studentmodule",),
    # bs_kwargs=dict(
    #     parse_only=bs4.SoupStrainer(
    #         class_=("post-content", "post-title", "post-header")
    #     )
    # ),
)
docs = loader.load()



text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index chunks
_ = vector_store.add_documents(documents=all_splits)

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke(
        {"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}



@app.route('/query', methods = ['POST', 'GET'])
def query():
 
    question = request.json.get('question')
    result = graph.invoke({"question": question})
    print('result')
    print(result)
    response = {
        "status": "success",
        "data": {
            "question": question,
            "answer": result["answer"]
        }
    }
    print('response')
    return response





# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


if __name__ == "__main__":
    app.run(port=4113, host='0.0.0.0', debug=True)
