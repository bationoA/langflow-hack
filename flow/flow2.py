import os

from typing import List

from langflow.graph.schema import RunOutputs
from langflow.load import run_flow_from_json
from dotenv import load_dotenv

load_dotenv(".env")

flow_file_path = os.path.join("database", "General task.json")

TWEAKS = {
    "ChatInput-oLlfo": {},
    "OpenAIModel-ibL7G": {"openai_api_key": os.environ['OPENAI_API_KEY']},
    "ChatOutput-MOySD": {}
}


def get_flow2_response(user_message: str) -> list[RunOutputs]:
    return run_flow_from_json(flow=flow_file_path,
                              input_value=user_message,
                              fallback_to_env_vars=True,  # False by default
                              tweaks=TWEAKS)
