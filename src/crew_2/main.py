#!/usr/bin/env python
import sys
from crew_2.crew import Crew2Crew
from dotenv import load_dotenv
import os
# from fastapi import FastAPI
# import sqlite3


# Load model directly
import torch
import transformers
# from transformers import AutoTokenizer, AutoModelForCausalLM


load_dotenv()
# app = FastAPI()




def run():

    # model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

    # pipeline = transformers.pipeline(
    #     "text-generation",
    #     model=model_id,
    #     model_kwargs={"torch_dtype": torch.bfloat16},
    #     device_map="auto",
    # )

    # messages = [
    #     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    #     {"role": "user", "content": "Who are you?"},
    # ]

    # terminators = [
    #     pipeline.tokenizer.eos_token_id,
    #     pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    # ]

    # outputs = pipeline(
    #     messages,
    #     max_new_tokens=256,
    #     eos_token_id=terminators,
    #     do_sample=True,
    #     temperature=0.6,
    #     top_p=0.9,
    # )
    # print(outputs[0]["generated_text"][-1])
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    print(os.getenv("OPENAI_API_BASE"))
    print(os.getenv("OPENAI_API_KEY"))

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
