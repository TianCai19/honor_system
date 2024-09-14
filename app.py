from flask import Flask, render_template, request, redirect, url_for, flash
from honor_system import HonorSystem
from logger import Logger
from encouragement_llm import show_encouragement
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息，可以更换为更安全的密钥

# 加载环境变量
load_dotenv('key.env')

# 初始化 HonorSystem
threshold = 0
mins_intervals = [0, 1, 5, 10, 15, 30]
thresholds = []
for i in range(1, 20):
    if i < len(mins_intervals):
        interval = mins_intervals[i - 1] * 60
    else:
        interval = mins_intervals[-1] * 60
    threshold += interval
    thresholds.append(threshold)

badge_dir = "static/badges"
music_dir = "music"
today = datetime.today()
data_file = f"data/honor_system_data_{today.strftime('%b_%d')}.json"
log_file = f"data/honor_system_log_{today.strftime('%b%d')}.json"

honor_system = HonorSystem(thresholds, badge_dir, music_dir, data_file, log_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    current_score = honor_system.score
    current_rank = honor_system.current_rank + 1
    rank_count = honor_system.logger.get_rank_count()

    next_rank = honor_system.current_rank + 1
    if next_rank < len(thresholds):
        score_needed = thresholds[next_rank] - honor_system.score
        time_needed = score_needed / 60  # 分钟
    else:
        score_needed = None
        time_needed = None

    return render_template('dashboard.html',
                           score=current_score,
                           rank=current_rank,
                           rank_count=rank_count,
                           score_needed=score_needed,
                           time_needed=time_needed,
                           badges=honor_system.current_rank)

@app.route('/adjust_score', methods=['POST'])
def adjust_score():
    try:
        points = int(request.form.get('points', 0))
        honor_system.adjust_score(points)
        flash(f"成功增加了 {points} 分！", "success")
    except ValueError:
        flash("请输入有效的分数！", "danger")
    return redirect(url_for('dashboard'))

@app.route('/encourage', methods=['GET', 'POST'])
def encourage():
    if request.method == 'POST':
        try:
            work_time_sec = int(request.form.get('work_time_sec', 1500))
            rank = int(request.form.get('rank', 4))
            player_feeling = request.form.get('player_feeling', "").strip()
            player_activity = request.form.get('player_activity', "").strip()
            
            if not player_feeling or not player_activity:
                flash("请填写所有必填字段！", "danger")
                return redirect(url_for('encourage'))
            
            # 调用 show_encouragement 并捕获 botanswer
            botanswer = show_encouragement(work_time_sec, rank, player_feeling, player_activity)
            
            # 通过 flash 传递 botanswer 到前端
            flash(botanswer, "info")  # 使用 "info" 类别来区分不同类型的消息
        except ValueError:
            flash("请输入有效的数字！", "danger")
        except Exception as e:
            flash(f"发生错误：{str(e)}", "danger")
        return redirect(url_for('dashboard'))
    return render_template('encourage.html')

if __name__ == "__main__":
    app.run(debug=False)