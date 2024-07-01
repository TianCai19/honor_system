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
    print(f"Current rank: {honor_system.current_rank + 1}")
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