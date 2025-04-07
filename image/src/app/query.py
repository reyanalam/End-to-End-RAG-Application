from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain import hub
import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "file.env"))
load_dotenv(dotenv_path)

import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
sys.path.append(parent_dir)
from populate_datbase import docsearch



def query_retrieval(query):
    try:
        template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {input}
        Helpful Answer:"""
        retrieval_qa_chat_prompt = PromptTemplate.from_template(template)
        retriever = docsearch.as_retriever()
        
        
        
        llm = Ollama(model="mistral", temperature=0.0)

        combine_docs_chain = create_stuff_documents_chain(
            llm, retrieval_qa_chat_prompt
        )

        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        answer1_without_knowledge = llm.invoke(query)
        answer_with_knowledge = retrieval_chain.invoke({"input": query})

        print("Query:", query)
        print("\nAnswer without knowledge:\n", answer1_without_knowledge)
        print("\nAnswer with knowledge:\n", answer_with_knowledge)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return answer_with_knowledge  

if __name__ == "__main__":
    query_retrieval("How much does a landing page cost to develop?")