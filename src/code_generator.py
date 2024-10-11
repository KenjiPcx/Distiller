from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def generate_code(question, context):
    llm = ChatOpenAI(temperature=0, model="o1-mini", base_url="https://api.aimlapi.com/v1")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a coding assistant with expertise in LangGraph. Answer the user's question based on the provided documentation. Ensure any code you provide can be executed with all required imports and variables defined."),
        ("human", "Documentation:\n{context}\n\nQuestion: {question}\n\nProvide a code solution:")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"context": context, "question": question})
    
    return response.content