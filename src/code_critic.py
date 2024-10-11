from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def critique_code(code):
    llm = ChatOpenAI(temperature=0, model="o1-mini", base_url="https://api.aimlapi.com/v1")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a code reviewer. Analyze the given code and suggest improvements or point out potential issues."),
        ("human", "Review the following code and suggest improvements:\n\n{code}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"code": code})
    
    return response.content