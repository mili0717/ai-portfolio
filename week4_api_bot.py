import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载.env密钥文件
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

from openai import OpenAI

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"

def get_client():
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        print("错误：未读取到 DEEPSEEK_API_KEY")
        sys.exit(1)
    _client = OpenAI(api_key=key, base_url=BASE_URL)
    return _client

def ask(question, temperature=0.7, max_tokens=512):
    client = get_client()
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system", "content":"你是对外汉语教师，回答对外汉语教学问题。"},
            {"role":"user", "content": question}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    ans = r.choices[0].message.content
    return ans

def save_log(q, a):
    log_path = BASE_DIR / "chat_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"【用户】{q}\n【AI】{a}\n---------\n")

if __name__ == "__main__":
    print("对外汉语问答机器人，输入quit退出")
    while True:
        user_q = input("请输入问题：")
        if user_q.strip().lower() == "quit":
            break
        res = ask(user_q)
        print("\nAI回答：", res, "\n")
        save_log(user_q, res)
