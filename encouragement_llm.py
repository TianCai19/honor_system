from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

from dotenv import load_dotenv
import os

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
    )
    messages = [ChatMessage(
        role="user",
        content=prompt
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0][0].message.content


# a function that shows with the ecougement and feedback
def show_encouragement(work_time_sec,rank):
    work_time_sec=1500
    work_time_min=work_time_sec/60
    level=4
    student_name="Cody"
    
    # promt ,you are a enournging person,u should encourage a students who is studying 
    # i will tell you how long he has been studying and what level he is in
    # give hime feedback and encourage him, tell him some nice words and give care to him
    # 
    prompt=f"""you are a encouraging person,u should encourage a students who is studying,
      he has been studying for {work_time_min} minutes and he is in level {level}
        give him feedback and encourage him, tell him some nice words and give care to him
        student name is {student_name}
        u can quote some famous words to encourage him
        mutiple lines are allowed but be breif
        show with more care and love using !! and some emojis in terminal 
        """
    return chatbot(prompt)


# a test in if main

if __name__ == "__main__":
    #test the chatbot
    #prompt="I am a student, I want to know how to get a badge"
    #print(chatbot(prompt))

    work_time_sec=1500
    
    rank=4
    
    print(show_encouragement(work_time_sec,rank))