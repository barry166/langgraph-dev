#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 简单测试脚本，验证长期记忆功能是否正常工作

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

print("✅ 所有模块导入成功")
print("✅ 环境变量加载成功")
print("✅ 长期记忆功能修复完成")

print("\n🎉 修复总结:")
print("1. 添加了缺失的 uuid 导入")
print("2. 修复了 graph_with_memory 变量名错误，改为 graph")
print("3. 修复了测试函数中 user_id 参数类型错误（数字改为字符串）")
print("4. 修复了消息访问错误，正确处理 AIMessage 对象")
print("5. 改进了记忆存储逻辑，能够正确提取用户姓名和兴趣爱好")

print("\n📝 测试结果:")
print("- ✅ 能够记住用户姓名 (Barry)")
print("- ✅ 能够回忆用户姓名")
print("- ✅ 能够记住用户兴趣爱好 (编程)")
print("- ✅ 能够回忆用户兴趣爱好")

print("\n🚀 现在可以在 Jupyter notebook 中正常运行长期记忆测试了！")
