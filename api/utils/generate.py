import subprocess, os
from models import Chat
import asyncio


def remove_matching_end(a, b):
    min_length = min(len(a), len(b))

    for i in range(min_length, 0, -1):
        if a[-i:] == b[:i]:
            return b[i:]

    return b


async def generate(
    model: str = "ggml-alpaca-13b-q4.bin",
    prompt: str = "The sky is blue because",
    n_predict: int = 128,
    temp: float = 0.05,
    top_k: int = 50,
    top_p: float = 0.95,
    repeast_last_n: int = 64,
    repeat_penalty: float = 1.3,
    chunk_size: int = 64,  # Define a chunk size (in bytes) for streaming the output bit by bit
):
    args = (
        "llama",
        "--model",
        "/usr/src/app/weights/" + model,
        "--n_predict",
        str(n_predict),
        "--temp",
        str(temp),
        "--top_k",
        str(top_k),
        "--top_p",
        str(top_p),
        "--repeat_last_n",
        str(repeast_last_n),
        "--repeat_penalty",
        str(repeat_penalty),
        "--threads",
        "4",
        "--prompt",
        f"{prompt}",
    )

    procLlama = await asyncio.create_subprocess_exec(
        *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, _ = await procLlama.communicate()

    for line in stdout.decode("utf-8"):
        yield line


async def get_full_prompt_from_chat(chat: Chat, simple_prompt: str):
    await chat.fetch_all_links()

    prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request. The response must be accurate, concise and evidence-based whenever possible. A complete answer is always ended by [end of text].

"""
    if chat.questions != None:
        for question in chat.questions:
            prompt += "### Instruction:\n" + question.question + "\n"
            prompt += "### Response:\n" + question.answer + "\n"

    prompt += "### Instruction:\n" + simple_prompt + "\n"
    prompt += "### Response:\n"

    return prompt
