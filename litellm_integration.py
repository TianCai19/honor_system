from litellm import completion
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

response = completion(
    model="deepseek/deepseek-chat", 
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
   api_key=os.getenv('DEEPSEEK_API_KEY')
)
print(response['choices'][0]['message']['content'])
