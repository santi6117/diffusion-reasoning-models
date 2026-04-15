from model import query_model
from load_dataset import get_dataset, extract_answer 
import re 

# PROMPTS

# baseline prompt 
def run_baseline(question: str) -> str:
    prompt = f"""Solve the following problem.

{question}

Give only the final answer.

Format:
Final Answer: <number>
"""
    return query_model(prompt)

# CoT prompt 
def run_cot(question: str) -> str:
    prompt = f"""Solve the following problem step by step.

{question}

Show your reasoning clearly, then give the final answer.

Format: Reasoning: Final Answer:
"""
    return query_model(prompt)

# Iterative refinement prompt 
def run_iter(question:str) -> str:
    # step 1
    prompt = f"""Solve the following problem step by step.

{question}

Format: Reasoning:

Final Answer:
"""
    answer = query_model(prompt)


# TESTING PIPELINE

# helper: define which reasoning method to use 
def get_method_function(method: str):
    if method == "baseline":
        return run_baseline
    elif method == "cot":
        return run_cot
    elif method == "iterative":
        return "iterative"
    elif method == "diffusion":
        return "diffusion"
    else:
        raise ValueError(f"Unknown method: {method}")


def run_experiment(method: str, dataset) -> list:
    method_fn = get_method_function(method)

    results = []

    for example in dataset:
        question = example["question"]
        true_answer = extract_answer(example["answer"])

        model_output = method_fn(question)

        results.append({
            "question": question,
            "true_answer": true_answer,
            "model_output": model_output,
            "method": method
        })

    return results 

""" def main():
    dataset = get_dataset(2) 

    results1 = run_experiment("baseline", dataset)
    results2 = run_experiment("cot", dataset)

    for r in results1:
        print(r)

    for r in results2:
        print(r)

main() """


# Experiment 1 

# Prompt: 
def get_reasoning(question: str) -> str:
    prompt = f"""
    System Prompt:
        "You are a logical reasoning engine. Solve the following math problem. 
        You must break your reasoning into clear, numbered steps. Start each step with the tag [STEP N] and end it with a newline. 
        After all steps are complete, provide the final answer in the format: 'Final Answer: [number]'."
    User Prompt:
        {question} \n\n Please solve this step-by-step."
    """

    return query_model(prompt)


def split_reasoning(reasoning: str) -> list:
    return [line.strip() for line in reasoning.splitlines() if "[STEP" in line]

def pass_partial(question: str, steps: list) -> str:
    formatted_steps = "\n".join(steps)

    prompt = f"""
    You are a completion engine.
    Problem: {question}
    
    Partial Reasoning:
    {formatted_steps}
    
    Task: Based ONLY on the partial reasoning above, finish the calculation in your head and provide the final numerical answer.
    Do not provide any further reasoning steps.
    Final Answer:"""
       

    return query_model(prompt, token_limit=16)

def run_experiment_1(question: str):
    # Given a question, get the full reasoning and final answer from the model. Then test how well the model can complete the answer  given increasingly more of the reasoning steps.
    reasoning = get_reasoning(question)
    steps = split_reasoning(reasoning)

    # loop through steps and test the model's ability to complete the answer with partial reasoning
    zero_shot_answer = pass_partial(question, [])
    print("Zero-Shot Answer (no steps):", zero_shot_answer)

    # test passing only the first step
    one_step_answer = pass_partial(question, steps[:1])
    print("Answer with first step only:", one_step_answer)

    # test with two steps 
    two_step_answer = pass_partial(question, steps[:2])
    print("Answer with two steps:", two_step_answer)

    # test with three steps
    three_step_answer = pass_partial(question, steps[:3])
    print("Answer with three steps:", three_step_answer)

    # test with four steps 
    four_step_answer = pass_partial(question, steps[:4])
    print("Answer with four steps:", four_step_answer)

    print("Full Reasoning:\n", reasoning)

def main():
    dataset = get_dataset(10)
    question = dataset[3]["question"]
    answer = dataset[3]["answer"]

    print(f"Question: {question}\n")
    print(f"Answer: {extract_answer(answer)}\n")

    run_experiment_1(question)

if __name__ == "__main__":    main()
