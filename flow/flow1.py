import os
import streamlit as st

from typing import List

from langflow.graph.schema import RunOutputs
from langflow.load import run_flow_from_json
from dotenv import load_dotenv

load_dotenv(".env")

flow_file_path = os.path.join("database", "TrustNode Care.json")


def get_flow1_response(user_message: str) -> list[RunOutputs]:
    if os.getenv('ASTRA_DB_ENDPOINT', None) is None or os.getenv('ASTRA_DB_TOKEN', None) is None:
        # If None, then we supposed this program is running on Streamlit. So, we get the environment
        # variables from Streamlit built-in env variables manager
        os.environ['ASTRA_DB_ENDPOINT'] = st.secrets["ASTRA_DB_ENDPOINT"]
        os.environ['ASTRA_DB_TOKEN'] = st.secrets["ASTRA_DB_TOKEN"]

    TWEAKS = {
        "ChatInput-UYsRC": {},
        "Prompt-pMN5s": {},
        "ChatOutput-gwqwX": {},
        "MistralModel-WeSs4": {"mistral_api_key": os.environ['AIML_API_KEY'],
                               "mistral_api_base": "https://api.aimlapi.com/",
                               "model_name": "mistralai/Mixtral-8x7B-Instruct-v0.1"},
        "OpenAIEmbeddings-SW8Bm": {"openai_api_key": os.getenv('OPENAI_API_KEY', None)},
        "ParseData-zoXIi": {},
        "AstraDB-dISi3": {"api_endpoint": os.environ['ASTRA_DB_ENDPOINT'], "token": os.environ['ASTRA_DB_TOKEN'],
                          "collection_name": "sexual_health_langflow_hack"}
    }
    return run_flow_from_json(flow=flow_file_path,
                              input_value=user_message,
                              fallback_to_env_vars=True,  # False by default
                              tweaks=TWEAKS)
