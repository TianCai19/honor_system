from honor_system import HonorSystem

if __name__ == "__main__":
    thresholds = [10, 40, 200, 300]  # Example thresholds
    badge_dir = "badges"
    music_dir = "music"
    data_file = "honor_system_data.json"
    log_file = "honor_system_log.json"

    honor_system = HonorSystem(thresholds, badge_dir, music_dir, data_file, log_file)

    # Adjust the score over a duration of time (e.g., 50 seconds)
    honor_system.adjust_score_over_time(50)  # Adjust score for 50 seconds

    # Print out the current score and rank
    print(f"Current score: {honor_system.score}")
    print(f"Current rank: {honor_system.current_rank + 1}")