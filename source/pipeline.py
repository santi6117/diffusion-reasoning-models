from model import query_model
from load_dataset import get_dataset, extract_answer 

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

def main():
    dataset = get_dataset(2) 

    results1 = run_experiment("baseline", dataset)
    results2 = run_experiment("cot", dataset)

    for r in results1:
        print(r)

    for r in results2:
        print(r)

main()


