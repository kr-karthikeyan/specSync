import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from src.utils.models import Blueprint
from src.utils.prompt_builder import build_blueprint_prompt


def generate_blueprint(prd_text: str, api_key: str) -> Blueprint:
    """
    The core function of SpecSync.
    Takes raw PRD text, sends it to OpenAI via LangChain,
    and returns a structured Blueprint object.
    
    prd_text: extracted text from the uploaded PRD
    api_key: OpenAI API key from .env
    returns: a validated Blueprint object
    """

    # Initialize the OpenAI model via LangChain
    # ChatOpenAI is LangChain's wrapper around OpenAI's chat models
    # temperature=0 means deterministic output — no randomness
    # we want consistent, structured JSON not creative responses
    llm = ChatOpenAI(
        model="gpt-4o-mini",   # fast and cheap — perfect for structured output
        temperature=0,          # 0 = focused, 1 = creative
        api_key=api_key         # your key from .env
    )

    # Build the prompt using our prompt builder
    prompt = build_blueprint_prompt(prd_text)

    # Create a HumanMessage — LangChain wraps prompts in message objects
    # This mimics a conversation where the user sends a message
    messages = [
        SystemMessage(content="You are a senior software architect who returns only valid JSON."),
        HumanMessage(content=prompt)
    ]

    # Send the messages to OpenAI and wait for response
    # This is the actual API call — costs a tiny amount of API credits
    response = llm.invoke(messages)

    # response.content is the raw text OpenAI returned
    # We expect it to be a JSON string
    raw_json = response.content

    # Clean the response — sometimes OpenAI adds ```json at start
    # even when we tell it not to. This handles that edge case.
    # strip() removes whitespace from both ends
    raw_json = raw_json.strip()

    # If it starts with a code block marker, remove it
    if raw_json.startswith("```"):
        # splitlines() splits by newline
        # [1:-1] removes first and last lines (the ``` markers)
        # join() combines lines back into one string
        raw_json = "\n".join(raw_json.splitlines()[1:-1])

    # Parse the JSON string into a Python dictionary
    # json.loads() converts a JSON string → Python dict
    blueprint_dict = json.loads(raw_json)

    # Validate and convert the dict into our Blueprint Pydantic model
    # model_validate() checks every field matches our defined structure
    # If anything is wrong, Pydantic raises a clear error
    blueprint = Blueprint.model_validate(blueprint_dict)

    return blueprint