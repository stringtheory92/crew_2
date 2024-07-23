#!/usr/bin/env python
import sys
import os
# from crew_2.crew import Crew2Crew
from dotenv import load_dotenv
import os
# from fastapi import FastAPI
# import sqlite3
from crew_2.crew import crew

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
# Load model directly
import torch
import transformers
# from transformers import AutoTokenizer, AutoModelForCausalLM


load_dotenv()
# app = FastAPI()




def run():

    inputs = {
        'topic': 'AI LLMs'
    }
    print(os.getenv("OPENAI_API_BASE"))
    print(os.getenv("OPENAI_API_KEY"))

    # Crew2Crew().crew().kickoff(inputs=inputs)
    return crew.kickoff()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        Crew2Crew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
