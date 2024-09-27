#!/usr/bin/env python3
# chatbot.py
# A multi-model chatbot that generates encouraging messages for students.
# Supports SparkAI and OpenAI models with easy extensibility for additional models.

import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# ---------------------------
# Configuration Management
# ---------------------------

# Load environment variables from key.env
load_dotenv('key.env')

class Config:
    """
    Centralized configuration class.
    """
    # SparkAI Configuration
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    SPARKAI_APP_ID = os.getenv("SPARKAI_APP_ID")
    SPARKAI_API_SECRET = os.getenv("SPARKAI_API_SECRET")
    SPARKAI_API_KEY = os.getenv("SPARKAI_API_KEY")
    SPARKAI_DOMAIN = 'generalv3.5'

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
    
    # Moonshot AI 配置
    MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
    MOONSHOT_API_URL = 'https://api.moonshot.cn/v1'  # 根据需要调整

    # General Configuration
    DEFAULT_TEMPERATURE = 0.9 # temperature for model sampling,higher value means more randomness
    HISTORY_FOLDER = "chathistory"

    # Validation to ensure required environment variables are set
    REQUIRED_VARS = [
        'SPARKAI_APP_ID',
        'SPARKAI_API_SECRET',
        'SPARKAI_API_KEY',
        # 'OPENAI_API_KEY'
    ]

    @classmethod
    def validate(cls):
        missing_vars = [var for var in cls.REQUIRED_VARS if not getattr(cls, var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Validate configuration on import
Config.validate()

# ---------------------------
# AI Model Abstraction
# ---------------------------

class ChatModel(ABC):
    """
    Abstract base class for AI models.
    """
    @abstractmethod
    def generate_response(self, messages: List[dict]) -> str:
        """
        Generate a response based on input messages.
        """
        pass

# ---------------------------
# SparkAI Model Implementation
# ---------------------------

try:
    from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
    from sparkai.core.messages import ChatMessage
except ImportError:
    raise ImportError("sparkai package not found. Please install it or check your environment.")

class SparkAIModel(ChatModel):
    """
    Implementation of the SparkAI model.
    """
    def __init__(self):
        self.spark = ChatSparkLLM(
            spark_api_url=Config.SPARKAI_URL,
            spark_app_id=Config.SPARKAI_APP_ID,
            spark_api_key=Config.SPARKAI_API_KEY,
            spark_api_secret=Config.SPARKAI_API_SECRET,
            spark_llm_domain=Config.SPARKAI_DOMAIN,
            streaming=False,
            temperature=Config.DEFAULT_TEMPERATURE
        )

    def generate_response(self, messages: List[dict]) -> str:
        chat_messages = [ChatMessage(role=msg['role'], content=msg['content']) for msg in messages]
        handler = ChunkPrintHandler()
        generations = self.spark.generate([chat_messages], callbacks=[handler])
        return generations.generations[0][0].message.content

# ---------------------------
# OpenAI Model Implementation
# ---------------------------

import openai

class OpenAIModel(ChatModel):
    """
    Implementation of the OpenAI model.
    """
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def generate_response(self, messages: List[dict]) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=Config.DEFAULT_TEMPERATURE
        )
        return response.choices[0].message['content'].strip()
    
    
# ---------------------------
# Moonshot AI 模型实现
# ---------------------------

# 假设 Moonshot AI 的 API 与 OpenAI 类似，但需要自定义基础 URL。
# 由于 OpenAI 的官方库不支持自定义 base_url，因此我们需要使用 requests 或类似库来实现。
import requests

class MoonshotAIModel(ChatModel):
    """
    Moonshot AI 模型的实现。
    """
    def __init__(self):
        self.api_key = Config.MOONSHOT_API_KEY
        self.base_url = Config.MOONSHOT_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(self, messages: List[dict]) -> str:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": "moonshot-v1-8k",
            "messages": messages,
            "temperature": Config.DEFAULT_TEMPERATURE
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Moonshot AI API 请求失败: {response.status_code} - {response.text}")
        data = response.json()
        return data['choices'][0]['message']['content'].strip()




# ---------------------------
# Prompt Template
# ---------------------------

def get_encouragement_prompt(work_time_min, rank, player_feeling, player_activity, student_name):
    """
    Constructs the prompt for generating encouragement messages.
    """
    prompt = f"""
You are an encouraging and compassionate mentor. Provide feedback to a student named {student_name} who has been studying diligently.

Details:
- Study Duration: {work_time_min} minutes
- Level: {rank}
- Current Feeling: {player_feeling}
- Recent Activity: {player_activity}

Your response should:
- Encourage and motivate the student.
- Include kind words and show genuine care.
- Incorporate quotes from famous people or Chinese poems to inspire.
- Use emojis and expressive punctuation (like !!) to convey warmth.
- Keep the message brief yet impactful.
- give a psychological hint to the student

Example Response:
"Great job, {student_name}! 🌟 You've been studying for {work_time_min} minutes at level {rank}. Remember, '学海无涯苦作舟' 🚀 Keep up the fantastic work! !!"
"""
    return prompt

# ---------------------------
# Utility Functions
# ---------------------------

def save_chat_history(response, work_time_min, player_feeling, player_activity, student_name, rank):
    """
    Saves the chat history to a text file with a timestamp.
    """
    folder_path = os.path.join(os.getcwd(), Config.HISTORY_FOLDER)
    os.makedirs(folder_path, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"Time: {current_time}, Response: {response}, Work Time: {work_time_min} minutes, "
        f"Level: {rank}, Feeling: {player_feeling}, Activity: {player_activity}, "
        f"Student Name: {student_name}\n"
    )

    file_name = datetime.now().strftime("%Y-%m-%d") + ".txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)

# ---------------------------
# ChatBot Class
# ---------------------------

class ChatBot:
    """
    Core chatbot class supporting multiple AI models.
    """
    def __init__(self, model_name='sparkai'):
        self.model = self._initialize_model(model_name)

    def _initialize_model(self, model_name):
        """
        Initializes the AI model based on the provided model name.
        """
        model_name = model_name.lower()
        if model_name == 'sparkai':
            return SparkAIModel()
        elif model_name == 'openai':
            return OpenAIModel()
        elif model_name == 'moonshot':
            return MoonshotAIModel()
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def show_encouragement(self, work_time_sec=1500, rank=4, player_feeling="", player_activity="", student_name="Cody"):
        """
        Generates and displays an encouragement message.
        """
        work_time_min = work_time_sec / 60

        # Construct the prompt using the template
        prompt = get_encouragement_prompt(
            work_time_min=work_time_min,
            rank=rank,
            player_feeling=player_feeling,
            player_activity=player_activity,
            student_name=student_name
        )

        # Prepare messages for the model
        messages = [
            {"role": "user", "content": prompt}
        ]

        try:
            # Generate the response
            bot_response = self.model.generate_response(messages)
            print(bot_response)

            # Save chat history
            save_chat_history(bot_response, work_time_min, player_feeling, player_activity, student_name, rank)

            return bot_response
        except Exception as e:
            print(f"An error occurred while generating the response: {e}")
            return None

# ---------------------------
# Main Function
# ---------------------------

def main():
    """
    Entry point for testing and running the chatbot.
    """
    # Initialize the chatbot with the desired model ('sparkai' or 'openai')
    bot = ChatBot(model_name='moonshot')  # Change to 'openai' to use OpenAI model

    # Test parameters
    work_time_sec = 1500  # 25 minuteså
    rank = 4
    player_feeling = "a bit tired"
    player_activity = "completed math exercises"
    student_name = "Cody"

    # Show encouragement
    bot.show_encouragement(
        work_time_sec=work_time_sec,
        rank=rank,
        player_feeling=player_feeling,
        player_activity=player_activity,
        student_name=student_name
    )

if __name__ == "__main__":
    main()