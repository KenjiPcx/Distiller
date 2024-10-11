import asyncio
import json
from typing import TypedDict, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnablePassthrough
from scraper import get_scraped_content
from question_generator import generate_questions
from code_generator import generate_code
from code_critic import critique_code
from code_validator import validate_code
from test_generator import generate_tests

class State(TypedDict):
    context: str
    questions: list
    current_question: str
    code: str
    critique: str
    is_code_valid: bool
    validation_result: str
    tests: str
    is_tests_valid: bool
    test_validation_result: str
    results: list

def scrape_and_generate_questions(state: State) -> State:
    context = asyncio.run(get_scraped_content())
    questions = generate_questions(context)
    return {"context": context, "questions": questions}

def process_question(state: State) -> State:
    if not state["questions"]:
        return {"current_question": END}
    current_question = state["questions"].pop(0)
    return {"current_question": current_question}

def generate_code_for_question(state: State) -> State:
    code = generate_code(state["current_question"], state["context"])
    return {"code": code}

def critique_generated_code(state: State) -> State:
    critique = critique_code(state["code"])
    return {"critique": critique}

def validate_generated_code(state: State) -> State:
    is_valid, validation_result = validate_code(state["code"])
    return {"is_code_valid": is_valid, "validation_result": validation_result}

def generate_tests_for_code(state: State) -> State:
    tests = generate_tests(state["code"])
    return {"tests": tests}

def validate_generated_tests(state: State) -> State:
    is_valid, test_validation_result = validate_code(state["tests"])
    return {"is_tests_valid": is_valid, "test_validation_result": test_validation_result}

def save_results(state: State) -> State:
    result = {
        "question": state["current_question"],
        "code": state["code"],
        "critique": state["critique"],
        "tests": state["tests"]
    }
    state["results"].append(result)
    return {"results": state["results"]}

def should_continue(state: State) -> str:
    if state["current_question"] == END:
        return "end"
    elif not state["is_code_valid"]:
        print(f"Code validation failed: {state['validation_result']}")
        return "process_question"
    elif not state["is_tests_valid"]:
        print(f"Test validation failed: {state['test_validation_result']}")
        return "process_question"
    else:
        return "save_results"

async def main():
    workflow = StateGraph(State)

    workflow.add_node("scrape_and_generate_questions", scrape_and_generate_questions)
    workflow.add_node("process_question", process_question)
    workflow.add_node("generate_code", generate_code_for_question)
    workflow.add_node("critique_code", critique_generated_code)
    workflow.add_node("validate_code", validate_generated_code)
    workflow.add_node("generate_tests", generate_tests_for_code)
    workflow.add_node("validate_tests", validate_generated_tests)
    workflow.add_node("save_results", save_results)

    workflow.set_entry_point("scrape_and_generate_questions")

    workflow.add_edge("scrape_and_generate_questions", "process_question")
    workflow.add_edge("process_question", "generate_code")
    workflow.add_edge("generate_code", "critique_code")
    workflow.add_edge("critique_code", "validate_code")
    workflow.add_edge("validate_code", "generate_tests")
    workflow.add_edge("generate_tests", "validate_tests")

    workflow.add_conditional_edges(
        "validate_tests",
        should_continue,
        {
            "process_question": "process_question",
            "save_results": "save_results",
            "end": END,
        },
    )

    workflow.add_edge("save_results", "process_question")

    app = workflow.compile()

    result = await app.arun(
        {
            "context": "",
            "questions": [],
            "current_question": "",
            "code": "",
            "critique": "",
            "is_code_valid": False,
            "validation_result": "",
            "tests": "",
            "is_tests_valid": False,
            "test_validation_result": "",
            "results": []
        }
    )

    # Save results to JSON file
    with open("data/output.json", "w") as f:
        json.dump(result["results"], f, indent=2)

    print("Process completed. Results saved to data/output.json")

if __name__ == "__main__":
    asyncio.run(main())