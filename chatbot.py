from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from prompt import (
    programming_answer_prompt,
    programming_summary_prompt,
    math_answer_prompt,
    math_summary_prompt,
    general_answer_prompt,
    general_summary_prompt,
    structured_output_prompt,
    classification_prompt,
)

from schema import AIResponse


# ==========================================
# Environment
# ==========================================

load_dotenv()


# ==========================================
# Groq Model
# ==========================================

model = ChatGroq(
    model="openai/gpt-oss-120b",
)


# ==========================================
# Output Parser
# ==========================================

str_parser = StrOutputParser()


# ==========================================
# Classification Chain
# ==========================================

classification_chain = (
    classification_prompt
    | model
    | str_parser
    | RunnableLambda(lambda x: x.strip().lower())
)


# ==========================================
# Programming Chain
# ==========================================

programming_chain = RunnableParallel(
    answer=programming_answer_prompt | model | str_parser,
    summary=programming_summary_prompt | model | str_parser,
    category=RunnableLambda(lambda _: "Programming"),
)


# ==========================================
# Math Chain
# ==========================================

math_chain = RunnableParallel(
    answer=math_answer_prompt | model | str_parser,
    summary=math_summary_prompt | model | str_parser,
    category=RunnableLambda(lambda _: "Math"),
)


# ==========================================
# General Chain
# ==========================================

general_chain = RunnableParallel(
    answer=general_answer_prompt | model | str_parser,
    summary=general_summary_prompt | model | str_parser,
    category=RunnableLambda(lambda _: "General"),
)


# ==========================================
# Prepare Question + Classification
# ==========================================

prepare_input = RunnableParallel(
    question=RunnablePassthrough(),
    classification=classification_chain,
)


# ==========================================
# RunnableBranch
# ==========================================

branch_chain = RunnableBranch(
    (
        lambda x: x["classification"] == "programming",
        programming_chain,
    ),
    (
        lambda x: x["classification"] == "math",
        math_chain,
    ),
    general_chain,
)


# ==========================================
# Pydantic Structured Output
# ==========================================

structured_llm = model.with_structured_output(AIResponse)

structured_output_chain = (
    structured_output_prompt
    | structured_llm
)


# ==========================================
# Complete Chatbot Chain
# ==========================================

chatbot_chain = (
    prepare_input
    | branch_chain
    | structured_output_chain
)


# ==========================================
# Public Function
# ==========================================

def get_response(question: str) -> AIResponse:
    return chatbot_chain.invoke(question)


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":
    question = "What is the capital of Bangladesh?"

    result = get_response(question)

    print("Question:", question)
    print("Answer:", result.answer)
    print("Summary:", result.summary)
    print("Category:", result.category)
    print("Confidence:", result.confidence)
    print("Keywords:", result.keywords)
    print("Structured Output:", result.model_dump())