from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based on the following context:

{context}

------

Answer the question based on the above context: {question}

"""

def get_embeddings():
    """Returns an embedding model (Hugging Face) compatible with Chroma."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def query_database(db, query_text, k=3):
    """Queries the Chroma database for the most relevant documents."""
    try:
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        return results if results else None
    except Exception as e:
        print(f"Error querying database: {str(e)}")
        return None

def generate_response(model, prompt):
    """Generates a response using the Llama3 model."""
    try:
        return model.invoke(prompt)
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

def process_query(query_text="Where is the school located?"):
    """Main function that processes a query text using a RAG system."""
    try:
        embedding_functions = get_embeddings()
        if not embedding_functions:
            return

        try:
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_functions)
        except Exception as e:
            print(f"Error connecting to Chroma database: {str(e)}")
            return

        results = query_database(db, query_text)
        
        # FIXED: Handle case where results are empty before accessing elements
        if not results:
            print("No relevant results found.")
            return
        
        print("----RESULTS----")
        print(results)
        print("----RESULTS[0]----")
        print(results[0])

        # FIXED: Ensure tuple unpacking is correct
        first_result = results[0]
        if isinstance(first_result, tuple) and len(first_result) >= 2:
            first_score = first_result[1]
        else:
            print("Unexpected result format.")
            return

        print("----RESULTS[0][1]----")
        print(first_score)

        # FIXED: Validate that score threshold is met before proceeding
        if first_score > 0.7:
            print("No results with sufficient relevance found.")
            return

        # FIXED: Ensure doc.page_content exists
        context_text = "\n\n---".join([doc.page_content if hasattr(doc, "page_content") else str(doc) for doc, _score in results])

        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        model = Ollama(model="llama3.2")
        response_text = generate_response(model, prompt)

        # FIXED: Ensure response is valid before printing
        if not response_text:
            print("Failed to generate a response.")
            return

        # FIXED: Ensure sources list is properly formatted
        sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]

        formatted_response = f"Response: {response_text}\nSource: {sources}"
        print(formatted_response)
        return response_text

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
