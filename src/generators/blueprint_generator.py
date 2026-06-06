import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.models import Blueprint, APIContract, DatabaseSchema, ComponentTree
from src.utils.prompt_builder import (
    build_api_prompt,
    build_schema_prompt,
    build_component_prompt,
    build_flow_prompt
)


def get_llm(provider: str, api_key: str):
    """
    Returns the appropriate LLM based on provider choice.
    Separated into its own function so it's reusable.
    
    provider: "openai" or "groq"
    api_key: the API key for the chosen provider
    """
    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            # 70b is more reliable for structured JSON than 8b
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=api_key,
            # Each small call needs max 1500 tokens — well within limit
            max_tokens=1500
        )
    else:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=api_key,
            max_tokens=2000
        )


def call_llm(llm, prompt: str) -> dict:
    """
    Makes one AI call and returns parsed JSON dict.
    Handles cleaning and parsing in one place.
    
    llm: the language model instance
    prompt: the prompt string to send
    returns: parsed Python dictionary
    """
    messages = [
        SystemMessage(content="You are a senior software architect. Return only valid compact JSON. No explanation. No markdown."),
        HumanMessage(content=prompt)
    ]

    # Make the API call
    response = llm.invoke(messages)
    raw = response.content.strip()

    # Print for debugging — remove later
    print(f"\n=== RAW RESPONSE ===\n{raw}\n=== END ===\n")

    # Remove markdown code blocks if model added them
    if raw.startswith("```"):
        lines = raw.splitlines()
        # Remove first line (```json) and last line (```)
        raw = "\n".join(lines[1:-1])

    # Parse JSON
    return json.loads(raw)


def generate_blueprint(prd_text: str, api_key: str, provider: str = "openai") -> Blueprint:
    """
    Generates a complete blueprint using 3 separate focused AI calls.
    Smaller calls = no truncation = reliable JSON every time.
    
    prd_text: extracted text from PRD
    api_key: API key for chosen provider
    provider: "openai" or "groq"
    returns: validated Blueprint object
    """

    # Get the language model
    llm = get_llm(provider, api_key)

    # ---- Call 1: API Contract ----
    # Small focused call — only asks for endpoints
    api_dict = call_llm(llm, build_api_prompt(prd_text))
    api_contract = APIContract(**api_dict)

    # ---- Call 2: Database Schema ----
    # Small focused call — only asks for tables
    schema_dict = call_llm(llm, build_schema_prompt(prd_text))
    database_schema = DatabaseSchema(**schema_dict)

    # ---- Call 3: Component Tree ----
    # Small focused call — only asks for components
    component_dict = call_llm(llm, build_component_prompt(prd_text))
    component_tree = ComponentTree(**component_dict)

    # ---- Call 4: User Flow ----
    # Returns a plain string not JSON — smallest call of all
    messages = [
        SystemMessage(content="You are a software architect. Return only a valid Mermaid.js diagram string. No explanation."),
        HumanMessage(content=build_flow_prompt(prd_text))
    ]
    flow_response = llm.invoke(messages)
    user_flow = flow_response.content.strip()

    # Remove markdown if present
    if user_flow.startswith("```"):
        lines = user_flow.splitlines()
        user_flow = "\n".join(lines[1:-1])

    # Combine all 4 outputs into one Blueprint
    return Blueprint(
        api_contract=api_contract,
        database_schema=database_schema,
        component_tree=component_tree,
        user_flow_diagram=user_flow
    )