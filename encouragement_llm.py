from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

from dotenv import load_dotenv
import os

from datetime import datetime

# Load .env file


def chatbot(prompt):
    load_dotenv('key.env')
    #星火认知大模型Spark3.5 Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
    SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
    #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
    SPARKAI_APP_ID = os.getenv("SPARKAI_APP_ID")
    SPARKAI_API_SECRET = os.getenv("SPARKAI_API_SECRET")
    SPARKAI_API_KEY = os.getenv("SPARKAI_API_KEY")
    #星火认知大模型Spark3.5 Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
    SPARKAI_DOMAIN = 'generalv3.5'
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
        temperature=0.7
    )
    messages = [ChatMessage(
        role="user",
        content=prompt
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0][0].message.content

def show_encouragement(work_time_sec=1500, rank=4, player_feeling="", player_activity=""):
    work_time_min = work_time_sec / 60
    student_name = "Cody"
    
    # 构建提示信息
    prompt = f"""you are an encouraging person, you should encourage a student who is studying,
      he has been studying for {work_time_min} minutes and he is in level {rank},
      he is feeling {player_feeling}, and he did: {player_activity}.
        give him feedback and encourage him, tell him some nice words and give care to him
        student name is {student_name}
        you can quote some famous words to encourage him, like Chinese poems, famous people's words,
        multiple lines are allowed but be brief
        show with more care and love using !! and some emojis in terminal 
        """
    botanswer = chatbot(prompt)
    print(botanswer)
    
    return botanswer

    save_chat_history(botanswer, work_time_min, player_feeling, player_activity, student_name, rank)

def save_chat_history(response, work_time_min,  player_feeling, player_activity, student_name, rank):
    folder_name = "chathistory"
    file_name = datetime.now().strftime("%Y-%m-%d") + ".txt"
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Ensure the directory exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the details to be saved
    current_time = datetime.now().strftime("%H:%M:%S")
    content = (f"Time: {current_time}, Response: {response}, Work Time: {work_time_min} minutes, "
               f"Level: {rank}, Feeling: {player_feeling}, Activity: {player_activity}, "
               f"Student Name: {student_name}, Rank: {rank}\n")

    # Save the content to the file
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "a") as file:
        file.write(content)

          
# a test in if main

if __name__ == "__main__":
    #test the chatbot
    #prompt="I am a student, I want to know how to get a badge"
    #print(chatbot(prompt))

    work_time_sec=1500
    
    rank=4
    
    show_encouragement(work_time_sec,rank)