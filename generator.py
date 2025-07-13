from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def get_qa_chain(retriever):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain
