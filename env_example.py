#!/usr/bin/env python3
"""
环境变量加载示例
演示如何在Python中加载和使用环境变量
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 方法1: 使用 python-dotenv 加载 .env 文件
def load_env_with_dotenv():
    """使用 python-dotenv 加载环境变量"""
    # 加载 .env 文件中的环境变量
    load_dotenv()
    
    # 获取环境变量
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 提供默认值
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    
    print("=== 使用 python-dotenv 加载的环境变量 ===")
    print(f"OpenAI API Key: {openai_api_key[:10]}..." if openai_api_key else "未设置")
    print(f"OpenAI Base URL: {openai_base_url}")
    print(f"Model Name: {model_name}")
    print(f"Temperature: {temperature}")
    
    return {
        "api_key": openai_api_key,
        "base_url": openai_base_url,
        "model_name": model_name,
        "temperature": temperature
    }

# 方法2: 直接从系统环境变量读取
def load_env_from_system():
    """直接从系统环境变量读取"""
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    # 使用 os.getenv() 提供默认值
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    # 使用 os.environ[] 会在变量不存在时抛出异常
    try:
        required_key = os.environ["OPENAI_API_KEY"]
        print("✓ 必需的环境变量已设置")
    except KeyError:
        print("✗ 缺少必需的环境变量: OPENAI_API_KEY")
        return None
    
    print("=== 从系统环境变量读取 ===")
    print(f"OpenAI API Key: {openai_api_key[:10]}..." if openai_api_key else "未设置")
    print(f"Model Name: {model_name}")
    
    return {
        "api_key": openai_api_key,
        "model_name": model_name
    }

# 方法3: 指定 .env 文件路径
def load_env_with_custom_path():
    """从指定路径加载 .env 文件"""
    # 可以指定不同的 .env 文件
    env_files = [".env.local", ".env.development", ".env"]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"加载环境变量文件: {env_file}")
            load_dotenv(env_file)
            break
    else:
        print("未找到任何 .env 文件")

# 方法4: 环境变量验证和类型转换
def validate_and_convert_env():
    """验证和转换环境变量类型"""
    load_dotenv()
    
    # 字符串类型
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY 环境变量是必需的")
    
    # 数值类型转换
    try:
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        if not 0 <= temperature <= 2:
            raise ValueError("TEMPERATURE 必须在 0-2 之间")
    except ValueError as e:
        print(f"温度参数错误: {e}")
        temperature = 0.7
    
    # 整数类型转换
    try:
        max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        if max_tokens <= 0:
            raise ValueError("MAX_TOKENS 必须大于 0")
    except ValueError as e:
        print(f"最大令牌数错误: {e}")
        max_tokens = 1000
    
    # 布尔类型转换
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() in ["true", "1", "yes"]
    
    print("=== 验证和转换后的环境变量 ===")
    print(f"API Key: {'✓ 已设置' if api_key else '✗ 未设置'}")
    print(f"Temperature: {temperature} (类型: {type(temperature).__name__})")
    print(f"Max Tokens: {max_tokens} (类型: {type(max_tokens).__name__})")
    print(f"Tracing Enabled: {tracing_enabled} (类型: {type(tracing_enabled).__name__})")
    
    return {
        "api_key": api_key,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "tracing_enabled": tracing_enabled
    }

# 实际使用示例：初始化 ChatOpenAI
def initialize_chatgpt():
    """使用环境变量初始化 ChatOpenAI"""
    load_dotenv()
    
    # 获取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    
    if not api_key:
        raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")
    
    # 初始化 ChatOpenAI
    llm_config = {
        "model": model_name,
        "temperature": temperature,
        "api_key": api_key,
    }
    
    # 如果设置了自定义 base_url，添加到配置中
    if base_url:
        llm_config["base_url"] = base_url
    
    llm = ChatOpenAI(**llm_config)
    
    print("=== ChatOpenAI 初始化成功 ===")
    print(f"模型: {model_name}")
    print(f"温度: {temperature}")
    print(f"Base URL: {base_url or '默认'}")
    
    return llm

if __name__ == "__main__":
    print("环境变量加载示例\n")
    
    # 检查是否存在 .env 文件
    if not os.path.exists(".env"):
        print("⚠️  未找到 .env 文件")
        print("请复制 .env.example 为 .env 并填入您的配置")
        print("cp .env.example .env")
        print()
    
    try:
        # 演示不同的加载方法
        print("1. 使用 python-dotenv 加载:")
        env_vars = load_env_with_dotenv()
        print()
        
        print("2. 从系统环境变量读取:")
        system_vars = load_env_from_system()
        print()
        
        print("3. 验证和类型转换:")
        validated_vars = validate_and_convert_env()
        print()
        
        print("4. 初始化 ChatOpenAI:")
        if os.getenv("OPENAI_API_KEY"):
            llm = initialize_chatgpt()
        else:
            print("跳过 ChatOpenAI 初始化 - 未设置 API Key")
            
    except Exception as e:
        print(f"错误: {e}")
