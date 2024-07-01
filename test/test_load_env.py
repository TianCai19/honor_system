import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')
print("Loading env from:", dotenv_path)  # Debug: Print the dotenv path
load_dotenv(dotenv_path=dotenv_path)
print(os.getenv("SPARKAI_APP_ID"))