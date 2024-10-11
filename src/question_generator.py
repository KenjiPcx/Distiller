from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def generate_questions(context):
    llm = ChatOpenAI(temperature=1, model="o1-preview", base_url="https://api.aimlapi.com/v1")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant tasked with generating complex questions that users might ask about LangGraph based on the provided documentation. Focus on implementation challenges and advanced use cases."),
        ("human", "Based on the following documentation, generate 10 complex questions or implementation challenges that users might face when working with LangGraph:\n\n{context}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({"context": context})
    
    # Assuming the response is a numbered list, split it into individual questions
    questions = response.content.split("\n")
    questions = [q.strip() for q in questions if q.strip()]
    
    return questions[:10]  # Ensure we return at most 10 questions