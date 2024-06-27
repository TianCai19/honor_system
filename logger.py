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
        log_entry = {
            'type': 'score',
            'score': score,
            'timestamp': datetime.now().isoformat()
        }
        self.logs.append(log_entry)
        self.save_logs()