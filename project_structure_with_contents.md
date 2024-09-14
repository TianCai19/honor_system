# Project File Structure with File Contents

- **./**
    - run_honor_system.sh
    Path: `./run_honor_system.sh`
    **Content:**
```text
    cd /Users/zz/code/honor_system
python main.py
```

    - logger.py
    Path: `./logger.py`
    **Content:**
```text
    import os
import json
from datetime import datetime

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logs = []

        # Load existing logs
        self.load_logs()

    def load_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                self.logs = json.load(file)
        else:
            self.logs = []

    def save_logs(self):
        with open(self.log_file, 'w') as file:
            json.dump(self.logs, file, indent=4)

    def log_rank(self, rank):
        log_entry = {
            'type': 'rank',
            'rank': rank,
            'timestamp': datetime.now().isoformat()
        }
        self.logs.append(log_entry)
        self.save_logs()

    def log_score_adjustment(self, score):
        #only save one score after every 30
        if score % 30 != 0:
            return
        log_entry = {
            'type': 'score',
            'score': score,
            'timestamp': datetime.now().isoformat()
        }
        self.logs.append(log_entry)
        self.save_logs()
    # a function to get the how many times rank was achieved
    def get_rank_count(self):
        count = 0
        for log in self.logs:
            if log['type'] == 'rank' :
                count += 1
        return count
```

    - todo.md
    Path: `./todo.md`
    **Content:**
```text
    # Project TODO List

## Features to Implement
- [*] a better progress bar for the next rank 
- [ ] a class to better organize the badge
- [ ] use chatgpt to add a auto generated badge
- [*] use chatgpt to give more human like feedback
- [*] need feed back and 45 rest feedback in the terminal ,all ask the feeling and give feedback
- [ ] move to online on the aws machine ,so that i can directly share with my friends and encourage each othere 
- [x] Feature 3 (completed)

## Bugs to Fix
- [ ] Bug 1
- [ ] Bug 2

## Improvements
- [ ] Improvement 1
- [ ] Improvement 2

## Notes
- Remember to review the feature list with the team on YYYY-MM-DD.
```

    - encouragement_llm.py
    Path: `./encouragement_llm.py`
    **Content:**
```text
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


# a function that shows with the ecougement and feedback
def show_encouragement(work_time_sec=1500,rank=4):
    work_time_min=work_time_sec/60
    student_name="Cody"
    
    
 # Ask the player how they feel and what they did in the past time
    player_feeling = input("How do you feel right now? ")
    player_activity = input("What did you do in the past time? ")

    # print(f"You said you're feeling {player_feeling} and you did {player_activity}.")
        
    
    # promt ,you are a enournging person,u should encourage a students who is studying 
    # i will tell you how long he has been studying and what level he is in
    # give hime feedback and encourage him, tell him some nice words and give care to him
    # 
    prompt=f"""you are a encouraging person,u should encourage a students who is studying,
      he has been studying for {work_time_min} minutes and he is in level {rank},
      he is feeling{player_feeling},and he did :{player_activity}.
        give him feedback and encourage him, tell him some nice words and give care to him
        student name is {student_name}
        u can quote some famous words to encourage him,like chinese poem ,famous people words,
        mutiple lines are allowed but be breif
        show with more care and love using !! and some emojis in terminal 
        """
    #return chatbot(prompt)
    botanswer=chatbot(prompt)
    print(botanswer)
    

    # 保存每次的输出到一个文件夹里 chathistory 的一个文件，按照日期命名
    #包含时间，恢复，rank 什么的情况
        
    # Modify the part where you call save_chat_history to include the new parameters
    # Assuming the variables work_time_min, level, player_feeling, player_activity, student_name, and rank are defined above
    botanswer = chatbot(prompt)
    print(botanswer)
    save_chat_history(botanswer, work_time_min,  player_feeling, player_activity, student_name, rank)
        


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
```

    - project_structure_with_contents.md
    Path: `./project_structure_with_contents.md`
    **Content:**
```text
    
```

    - key.env
    Path: `./key.env`
    **Content:**
```text
    SPARKAI_APP_ID=112c1287
SPARKAI_API_SECRET=M2U4NGU2NDc0MDE3YTIwOTZjZjBlZjc2
SPARKAI_API_KEY=9bf8ed4ddc98699e78a9d7121b042062
```

    - honor_system.py
    Path: `./honor_system.py`
    **Content:**
```text
    import os
import pygame
from PIL import Image
import time
import json
from tqdm import tqdm
import threading
from logger import Logger
import time
import subprocess

def activate_terminal():
    subprocess.run(["osascript", "-e", 'tell application "Terminal" to activate'])

# add llm enouragement chatbot
from encouragement_llm import show_encouragement

class HonorSystem:
    def __init__(self, thresholds, badge_dir, music_dir, data_file, log_file):
        self.thresholds = thresholds
        self.badge_dir = badge_dir
        self.music_dir = music_dir
        self.data_file = data_file
        self.logger = Logger(log_file)

        pygame.mixer.init()

        # Load data from file
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.score = data.get('score', 0)
                self.current_rank = data.get('current_rank', -1)

        else:
            self.score = 0
            self.current_rank = 0

    def save_data(self):
        data = {
            'score': self.score,
            'current_rank': self.current_rank
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def adjust_score(self, points):
        self.score += points
        self.logger.log_score_adjustment(self.score)
        self.check_for_badge()
        self.save_data()

    def check_for_badge(self):
        for i, threshold in enumerate(self.thresholds):
            if self.score >= threshold and i > self.current_rank:
                self.award_badge(i)
                self.current_rank = i
                self.save_data()
# a new strategy for badge ,get 1 badge at 5 scores and then 10 mins after and 15 and 30 ,always
        


    def award_badge(self, rank):
        print(f"Congratulations! You've reached rank {rank + 1}! with score {self.score}")
        self.logger.log_rank(rank + 1)
        #self.display_badge_and_play_music(0)
        threading.Thread(target=show_encouragement(self.score,self.current_rank)).start()
        threading.Thread(target=activate_terminal).start()

    def display_badge_and_play_music(self, rank):
        badge_image_path = os.path.join(self.badge_dir, f"badge{rank + 1}.png")
        badge_image = Image.open(badge_image_path)
        badge_image.show()

        music_file_path = os.path.join(self.music_dir, f"music{rank + 1}.wav")
        threading.Thread(target=self.play_music, args=(music_file_path,)).start()

    def play_music(self, music_file_path):
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def adjust_score_over_time(self, duration_seconds):
        # for _ in tqdm(range(duration_seconds), desc="Adjusting Score"):
        #     self.adjust_score(1)
        #     time.sleep(1)
        while(1):
            time_for_next_rank=self.thresholds[self.current_rank+1]-self.score
            for _ in tqdm(range(time_for_next_rank), desc="Adjusting Score"):
                self.adjust_score(1)
                time.sleep(1)
            if self.current_rank==len(self.thresholds)-1:
                break


```

    - main.py
    Path: `./main.py`
    **Content:**
```text
    from honor_system import HonorSystem
import datetime
import logger

if __name__ == "__main__":
    threshold=0
    mins_intervals = [0,1, 5, 10,15,30]
    thresholds = []
    for i in range(1, 20):
        if i <len(mins_intervals):
            interval=mins_intervals[i-1]*60
        else:
            interval=mins_intervals[-1]*60
        threshold+=interval
        thresholds.append(threshold)
    print(thresholds)
  
    badge_dir = "badges"
    music_dir = "music"
    today = datetime.date.today()
    data_file = f"data/honor_system_data_{today.strftime('%b_%d')}.json"
    log_file = f"data/honor_system_log_{today.strftime('%b%d')}.json"

    
    honor_system = HonorSystem(thresholds, badge_dir, music_dir, data_file, log_file)

    # output the current score and rank and badge/rank number
    # get the data from the log file
    print(f"Current score: {honor_system.score}")
    print(f"Current rank: {honor_system.current_rank }")
    print(f"Current rank count: {honor_system.logger.get_rank_count()}")
    # calulate the score needed for the next rank
    next_rank = honor_system.current_rank + 1
    if next_rank < len(thresholds):
        score_needed = thresholds[next_rank] - honor_system.score
        print(f"Score needed for next rank: {score_needed}")
        # each score is 1 second,caculate the minutes needed for the next rank
        print(f"Time needed for next rank: {score_needed/60} minutes")
    else:
        print("You've reached the highest rank!")


    # Adjust the score over a duration of time (e.g., 50 seconds)
    honor_system.adjust_score_over_time(thresholds[-1])  # Adjust score for 50 seconds

    # Print out the current score and rank
    print(f"Current score: {honor_system.score}")
    print(f"Current rank: {honor_system.current_rank + 1}")
```

    - **music/**
        - music2.wav
        Path: `./music/music2.wav`
        **Error reading file:** 'utf-8' codec can't decode byte 0xb1 in position 5: invalid start byte

        - music3.wav
        Path: `./music/music3.wav`
        **Error reading file:** 'utf-8' codec can't decode byte 0xfa in position 4: invalid start byte

        - music1.wav
        Path: `./music/music1.wav`
        **Error reading file:** 'utf-8' codec can't decode byte 0xd7 in position 458: invalid continuation byte

    - **test/**
        - progress_example.py
        Path: `./test/progress_example.py`
        **Content:**
```text
        from progress.bar import Bar
import time

bar = Bar('Processing', max=300)
for i in range(300):
    time.sleep(0.1)
    bar.next()
bar.finish()
```

        - tempCodeRunnerFile.py
        Path: `./test/tempCodeRunnerFile.py`
        **Content:**
```text
        bar = Bar('Processing', max=300)
for i in range(300):
    time.sleep(0.1)
    bar.next()
bar.finish()
```

        - test_music_play.py
        Path: `./test/test_music_play.py`
        **Content:**
```text
        import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Load the music file
music_file = "music/music1.wav"

try:
    pygame.mixer.music.load(music_file)
    print(f"Playing {music_file}...")
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    print("Music playback finished.")
except pygame.error as e:
    print(f"Could not play {music_file}: {e}")
```

        - tqdm_example.py
        Path: `./test/tqdm_example.py`
        **Content:**
```text
        import random
from tqdm import tqdm
import time



with tqdm(total=100) as pbar:
    # random time consuming loop
    
    jump_time = random.randint(1, 10)
    sum=0
    while sum<100:
        pbar.update(jump_time)
        time.sleep(0.5)
        jump_time = random.randint(1, 10)
        sum+=jump_time
        print(jump_time)
        
```

        - store_in_markdown.py
        Path: `./test/store_in_markdown.py`
        **Content:**
```text
        import os

# 跳过这些文件夹
WHITELIST_DIRS = ['data', 'chathistory']  # 替换为你想跳过的目录名称

def is_whitelisted(directory):
    """
    判断文件夹是否在白名单中
    """
    for whitelist_dir in WHITELIST_DIRS:
        if whitelist_dir in directory:
            return True
    return False

def list_files_in_project(start_path, output_md):
    with open(output_md, 'w', encoding='utf-8') as md_file:
        md_file.write("# Project File Structure with File Contents\n\n")
        for root, dirs, files in os.walk(start_path):
            # 跳过白名单中的文件夹
            if is_whitelisted(root):
                continue
            
            # 跳过隐藏文件夹（以'.'开头的文件夹）
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * 4 * level
            md_file.write(f"{indent}- **{os.path.basename(root)}/**\n")
            sub_indent = ' ' * 4 * (level + 1)

            for f in files:
                # 跳过隐藏文件（以'.'开头的文件）
                if f.startswith('.'):
                    continue

                file_path = os.path.join(root, f)
                md_file.write(f"{sub_indent}- {f}\n{sub_indent}Path: `{file_path}`\n")

                # 读取文件内容并写入 Markdown 文件
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        content = file_content.read()
                        md_file.write(f"{sub_indent}**Content:**\n")
                        md_file.write(f"```text\n{sub_indent}{content}\n```\n\n")
                except Exception as e:
                    md_file.write(f"{sub_indent}**Error reading file:** {str(e)}\n\n")

if __name__ == "__main__":
    project_directory = '.'  # 当前目录，也可以指定其他目录
    output_markdown = 'project_structure_with_contents.md'  # 输出 Markdown 文件的名称
    list_files_in_project(project_directory, output_markdown)
    print(f"文件结构和内容已保存到 {output_markdown}")
```

        - enumerate_example.py
        Path: `./test/enumerate_example.py`
        **Content:**
```text
        
for i, threshold in enumerate([1, 2, 3, 4, 5]):
    print(i, threshold)

# expalin enumerate
# enumerate is a built-in function of Python. It allows us to loop over something and have an automatic counter. Here is an example:
#explain the output
# The enumerate object yields pairs containing a count (from start, which defaults to zero) and a value yielded by the iterable argument.
for threshold in enumerate([1, 2, 3, 4, 5]):
    print(threshold)
```

        - tkinter_prograss_example.py
        Path: `./test/tkinter_prograss_example.py`
        **Content:**
```text
        import tkinter as tk
from tkinter import ttk
import time
import threading

def start_countdown():
    def countdown():
        for i in range(30, -1, -1):
            time_var.set(i)
            progress_var.set((30 - i) / 30 * 100)
            root.update_idletasks()
            time.sleep(1)

    # Start the countdown in a separate thread to keep the GUI responsive
    threading.Thread(target=countdown).start()

root = tk.Tk()
root.title("Countdown Timer")

time_var = tk.IntVar(value=30)
progress_var = tk.DoubleVar(value=0)

time_label = tk.Label(root, textvariable=time_var, font=("Helvetica", 48))
time_label.pack(pady=20)

progress = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress.pack(fill=tk.X, expand=1, pady=20)

start_button = tk.Button(root, text="Start Countdown", command=start_countdown)
start_button.pack(pady=20)

root.mainloop()
```

        - test_load_env.py
        Path: `./test/test_load_env.py`
        **Content:**
```text
        import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'key.env')
print("Loading env from:", dotenv_path)  # Debug: Print the dotenv path
load_dotenv(dotenv_path=dotenv_path)
print(os.getenv("SPARKAI_APP_ID"))
```

    - **__pycache__/**
        - honor_system.cpython-311.pyc
        Path: `./__pycache__/honor_system.cpython-311.pyc`
        **Error reading file:** 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte

        - logger.cpython-311.pyc
        Path: `./__pycache__/logger.cpython-311.pyc`
        **Error reading file:** 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte

        - encouragement_llm.cpython-311.pyc
        Path: `./__pycache__/encouragement_llm.cpython-311.pyc`
        **Error reading file:** 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte

        - tqdm.cpython-311.pyc
        Path: `./__pycache__/tqdm.cpython-311.pyc`
        **Error reading file:** 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte

        - tqdm_example.cpython-311.pyc
        Path: `./__pycache__/tqdm_example.cpython-311.pyc`
        **Error reading file:** 'utf-8' codec can't decode byte 0xa7 in position 0: invalid start byte

    - **badges/**
        - badge1.png
        Path: `./badges/badge1.png`
        **Error reading file:** 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte

        - badge3.png
        Path: `./badges/badge3.png`
        **Error reading file:** 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte

        - badge2.png
        Path: `./badges/badge2.png`
        **Error reading file:** 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte

