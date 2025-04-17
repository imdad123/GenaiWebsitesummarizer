from  pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
file_path = Path(__file__).parent / "nodesjs.pdf"
loader = PyPDFLoader(file_path=file_path)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_doc = text_splitter.split_documents(documents=docs)


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key="sk-proj-"
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)
# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="rag_collection",
#     embedding=embeddings,
# )
# vector_store.add_documents(documents=split_doc)
print("injectionDone")
retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="rag_collection",
    embedding=embeddings,
)
user_input ="What is nodejs?"
search_result = retriver.similarity_search(
    query=user_input
    
)
SYTEM_PROMPT = f"""YOU are a helpful assistant. Answer the question based on the context provided." 
If you don't know the answer, say 'I don't know'give the result in heading and paragraph format .content:{search_result}"""


client = OpenAI(
    api_key="sk-proj-",
   
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYTEM_PROMPT},
        {
            "role": "user",
            "content": user_input,
        },
    ],
)

print(completion.choices[0].message.content)