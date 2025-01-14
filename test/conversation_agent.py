from litellm import completion
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a good company with brief sentences, "
                "who is good at talking. "
                "You are a 23-year-old girl who is a student "
                "and a good person."
            )
        }
    ]

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user input to chat history
        messages.append({"role": "user", "content": user_input})

        # Get response from the model
        try:
            response = completion(
                model="deepseek/deepseek-chat",
                messages=messages,
            )

            response_content = response['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": response_content})
            print(f"Bot: {response_content}")
        except Exception as e:
            print(f"An error occurred: {e}")
