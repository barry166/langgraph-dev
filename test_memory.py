#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.store.memory import InMemoryStore, BaseStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnableConfig
import uuid
import os

# 加载环境变量
load_dotenv()

# 初始化聊天模型
chat_model = ChatOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL'),
    model=os.getenv('MODEL_NAME')
)

# 定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 初始化存储
embedding_model_name = os.getenv("EMBEDDING_NAME")
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
print(f"Using embedding model: {embedding_model_name}, API Key: {api_key}, Base URL: {base_url}")

store = InMemoryStore(
    index={
        "dims": 1024,
        "embed": OpenAIEmbeddings(
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=embedding_model_name,
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
    }
)

def call_model(state: State, config: RunnableConfig, *, store: BaseStore):
    # 从存储中检索用户信息
    user_id = config["configurable"]["user_id"]
    # 从存储中检索用户信息
    namespace = ("memories", user_id)
    memories = store.search(namespace, query=str(state["messages"][-1].content))
    info = "\n".join([d.value["data"] for d in memories])
    system_msg = f"你是一个正在与用户交谈的小助手。用户信息：{info}"
    
    # 如果用户要求模型记住信息，则存储新的记忆
    last_message = state["messages"][-1]
    if "记住" in last_message.content or "remember" in last_message.content.lower():
        # 提取用户想要记住的信息
        content = last_message.content
        if "我的名字是" in content:
            name = content.split("我的名字是")[1].strip()
            memory = f"用户的名字是{name}"
        elif "我喜欢" in content:
            hobby = content.split("我喜欢")[1].strip()
            memory = f"用户喜欢{hobby}"
        else:
            memory = content  # 如果无法解析，就存储原始内容
        store.put(namespace, str(uuid.uuid4()), {"data": memory})
    
    response = chat_model.invoke(
        [{"role": "system", "content": system_msg}] + state["messages"]
    )
    return {"messages": response}

# 构建图
builder = StateGraph(State)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", END)
graph = builder.compile(store=store)

# 测试长期记忆功能
def test_memory_graph(user_input: str, user_id: str = "user123"):
    print(f"User: {user_input}")
    print(f"==================\n")
    
    config = {"configurable": {"user_id": user_id}}
    
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config
    ):
        for value in event.values():
            if "messages" in value:
                last_message = value["messages"]
                if hasattr(last_message, 'content'):
                    print("Assistant:", last_message.content)
                elif isinstance(last_message, list) and len(last_message) > 0:
                    print("Assistant:", last_message[-1].content)
                else:
                    print("Assistant:", str(last_message))
    print("\n")

if __name__ == "__main__":
    # 测试序列
    print("=== 长期记忆测试 ===")
    test_memory_graph("你好，请记住我的名字是Barry", "user123")
    test_memory_graph("我叫什么名字？", "user123")
    test_memory_graph("请记住我喜欢编程", "user123")
    test_memory_graph("你知道我的兴趣爱好吗？", "user123")
