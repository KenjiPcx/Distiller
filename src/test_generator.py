from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def generate_tests(code):
    llm = ChatOpenAI(temperature=0, model="o1-mini", base_url="https://api.aimlapi.com/v1")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a test writer. Generate pytest test cases for the given code."),
        ("human", "Write pytest test cases for the following code:\n\n{code}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"code": code})
    
    return response.content