from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


def analyse_file(filename: str):
    loader = PyPDFLoader(filename)
    documents = loader.load()
    embeddings = OpenAIEmbeddings()
    pdfsearch = Chroma.from_documents(documents, embeddings, )
    chain = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=0.9),
        retriever=pdfsearch.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=True,
    )
    return chain


def generate_response(question: str, chain: ConversationalRetrievalChain):
    response = chain({'question': question, 'chat_history': ''}, return_only_outputs=True)
    return response['answer']
