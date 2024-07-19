#!/usr/bin/env python
import sys
from crew_2.crew import Crew2Crew
# from dotenv import load_dotenv
import os


# load_dotenv()

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    # print(os.getenv("OPENAI_API_BASE"))
    # print(os.getenv("OPENAI_API_KEY"))

    Crew2Crew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        Crew2Crew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
