from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

loader = DirectoryLoader("knowledge_base", glob="**/*.pdf", loader_cls=PyPDFLoader)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embedding = OpenAIEmbeddings()
db = Chroma.from_documents(chunks, embedding, persist_directory="./vectorstore")
db.persist()



retriever = db.as_retriever()
relevant_docs = retriever.get_relevant_documents("How do I answer 'Tell me about yourself'?")



#send this through to gpt
messages = [
  {"role": "system", "content": "You are a job interview expert. Use the context to help the user."},
  {"role": "user", "content": "How do I answer the 'strengths and weaknesses' question?"},
  {"role": "assistant", "content": "Relevant context:\n" + relevant_docs}
]
