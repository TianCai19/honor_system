
#!/bin/bash

# setup_chatbot.sh
# This script sets up the multi-model chatbot project structure with necessary files and content.
# Usage: ./setup_chatbot.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Function to create directories
create_directories() {
    echo "Creating project directories..."
    mkdir -p chatbot/models
    mkdir -p chatbot/utils
    echo "Directories created successfully."
}

# Function to create files with content
# create_files() {
    echo "Creating and writing files..."

    # 1. config.py
    cat <<EOL > chatbot/config.py
# config.py
# Centralized configuration for the chatbot, including environment variables.

from dotenv import load_dotenv
import os

# Load environment variables from key.env
load_dotenv('key.env')

class Config:
    # SparkAI Configuration
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    SPARKAI_APP_ID = os.getenv("SPARKAI_APP_ID")
    SPARKAI_API_SECRET = os.getenv("SPARKAI_API_SECRET")
    SPARKAI_API_KEY = os.getenv("SPARKAI_API_KEY")
    SPARKAI_DOMAIN = 'generalv3.5'

    # OpenAI Configuration (Example for another model)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

    # General Configuration
    DEFAULT_TEMPERATURE = 0.7
    HISTORY_FOLDER = "chathistory"
EOL

    # 2. models/__init__.py
    touch chatbot/models/__init__.py

    # 3. models/base.py
    cat <<EOL > chatbot/models/base.py
# models/base.py
# Abstract base class for AI models.

from abc import ABC, abstractmethod
from typing import List

class ChatModel(ABC):
    @abstractmethod
    def generate_response(self, messages: List[dict]) -> str:
        pass
EOL

    # 4. models/sparkai.py
    cat <<EOL > chatbot/models/sparkai.py
# models/sparkai.py
# Implementation of the SparkAI model.

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from typing import List
from .base import ChatModel
from chatbot.config import Config

class SparkAIModel(ChatModel):
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
EOL

    # 5. models/openai.py
    cat <<EOL > chatbot/models/openai.py
# models/openai.py
# Implementation of the OpenAI model.

import openai
from typing import List
from .base import ChatModel
from chatbot.config import Config

class OpenAIModel(ChatModel):
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def generate_response(self, messages: List[dict]) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=Config.DEFAULT_TEMPERATURE
        )
        return response.choices[0].message['content']
EOL

    # 6. utils/__init__.py
    touch chatbot/utils/__init__.py

    # 7. utils/history.py
    cat <<EOL > chatbot/utils/history.py
# utils/history.py
# Utility functions for managing chat history.

import os
from datetime import datetime
from chatbot.config import Config

def save_chat_history(response, work_time_min, player_feeling, player_activity, student_name, rank):
    folder_path = os.path.join(os.getcwd(), Config.HISTORY_FOLDER)
    
    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Define the details to be saved
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = (
        f"Time: {current_time}, Response: {response}, Work Time: {work_time_min} minutes, "
        f"Level: {rank}, Feeling: {player_feeling}, Activity: {player_activity}, "
        f"Student Name: {student_name}\n"
    )
    
    # Save the content to the file
    file_name = datetime.now().strftime("%Y-%m-%d") + ".txt"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)
EOL

    # 8. prompt_template.py
    cat <<EOL > chatbot/prompt_template.py
# prompt_template.py
# Template for generating encouragement prompts.

def get_encouragement_prompt(work_time_min, rank, player_feeling, player_activity, student_name):
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

Example Response:
"Great job, {student_name}! 🌟 You've been studying for {work_time_min} minutes at level {rank}. Remember, '学海无涯苦作舟' 🚀 Keep up the fantastic work! !!"
"""
    return prompt
EOL

    # 9. chatbot.py
    cat <<EOL > chatbot/chatbot.py
# chatbot.py
# Core chatbot logic supporting multiple AI models.

from models.sparkai import SparkAIModel
from models.openai import OpenAIModel
from prompt_template import get_encouragement_prompt
from utils.history import save_chat_history

class ChatBot:
    def __init__(self, model_name='sparkai'):
        self.model = self._initialize_model(model_name)
    
    def _initialize_model(self, model_name):
        if model_name.lower() == 'sparkai':
            return SparkAIModel()
        elif model_name.lower() == 'openai':
            return OpenAIModel()
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    
    def show_encouragement(self, work_time_sec=1500, rank=4, player_feeling="", player_activity="", student_name="Cody"):
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
        
        # Generate the response
        bot_response = self.model.generate_response(messages)
        print(bot_response)
        
        # Save chat history
        save_chat_history(bot_response, work_time_min, player_feeling, player_activity, student_name, rank)
        
        return bot_response
EOL

    # 10. main.py
    cat <<EOL > chatbot/main.py
# main.py
# Entry point for testing and running the chatbot.

from chatbot import ChatBot

def main():
    # Initialize the chatbot with the desired model ('sparkai' or 'openai')
    bot = ChatBot(model_name='sparkai')  # Change to 'openai' to use OpenAI model
    
    # Test parameters
    work_time_sec = 1500  # 25 minutes
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
EOL

    # 11. key.env
    cat <<EOL > chatbot/key.env
# key.env
# Environment variables for API keys. Replace the placeholder values with your actual keys.

SPARKAI_APP_ID=your_sparkai_app_id
SPARKAI_API_SECRET=your_sparkai_api_secret
SPARKAI_API_KEY=your_sparkai_api_key
OPENAI_API_KEY=your_openai_api_key
EOL

    # 12. requirements.txt
    cat <<EOL > chatbot/requirements.txt
# requirements.txt
# Python dependencies required for the chatbot.

sparkai
dotenv
openai
EOL

    # 13. README.md
    cat <<EOL > chatbot/README.md
# Multi-Model Chatbot

This chatbot supports multiple AI models, including SparkAI and OpenAI, to generate encouraging messages for students.

## Features

- **Modular Design**: Easily add or switch AI models.
- **Configurable Prompts**: Use templates to customize prompts.
- **Chat History**: Save chat interactions with timestamps.
- **Flexible Configuration**: Manage settings via environment variables.

## Project Structure

```
chatbot/
│
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── sparkai.py
│   └── openai.py
│
├── utils/
│   ├── __init__.py
│   └── history.py
│
├── config.py
├── prompt_template.py
├── chatbot.py
├── main.py
├── key.env
├── requirements.txt
└── README.md
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/chatbot.git
   cd chatbot
   ```

2. **Install Dependencies**

   Ensure you have Python installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   Create a `key.env` file in the project root with the following content:

   ```env
   SPARKAI_APP_ID=your_sparkai_app_id
   SPARKAI_API_SECRET=your_sparkai_api_secret
   SPARKAI_API_KEY=your_sparkai_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

   Replace the placeholder values with your actual API keys.

4. **Run the Chatbot**

   Execute the main script to test the chatbot:

   ```bash
   python main.py
   ```

## Adding a New AI Model

1. **Create a New Model Class**

   Add a new Python file in the `models/` directory (e.g., `newmodel.py`) and implement the `ChatModel` interface. For example:

   ```python
   # models/newmodel.py
   import newmodelsdk
   from typing import List
   from .base import ChatModel
   from chatbot.config import Config

   class NewModel(ChatModel):
       def __init__(self):
           self.client = newmodelsdk.Client(api_key=Config.NEW_MODEL_API_KEY)

       def generate_response(self, messages: List[dict]) -> str:
           response = self.client.get_response(messages)
           return response.text
   ```

2. **Update `chatbot.py`**

   Modify the `_initialize_model` method to include the new model:

   ```python
   def _initialize_model(self, model_name):
       if model_name.lower() == 'sparkai':
           return SparkAIModel()
       elif model_name.lower() == 'openai':
           return OpenAIModel()
       elif model_name.lower() == 'newmodel':
           return NewModel()
       else:
           raise ValueError(f"Unsupported model: {model_name}")
   ```

3. **Update `main.py`**

   Initialize the `ChatBot` with the new model name:

   ```python
   bot = ChatBot(model_name='newmodel')
   ```

4. **Update `key.env`**

   Add any new environment variables required by the new model:

   ```env
   NEW_MODEL_API_KEY=your_newmodel_api_key
   ```

5. **Install Additional Dependencies**

   If the new model requires additional packages, add them to `requirements.txt` and install them:

   ```bash
   pip install -r requirements.txt
   ```

## Suggestions for Further Improvements

1. **Logging**: Implement logging instead of using `print` statements for better monitoring and debugging.
2. **Error Handling**: Add comprehensive error handling to manage API failures, invalid inputs, etc.
3. **Unit Testing**: Write unit tests for each module to ensure reliability.
4. **Dynamic Configuration**: Use a configuration management tool or framework for more complex configurations.
5. **Asynchronous Support**: If supported by the AI models, implement asynchronous calls to improve performance.

## License

MIT License

EOL

    echo "Files created and written successfully."
}
