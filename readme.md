
# Honor System

This project implements a motivational system to encourage productivity and rank achievements. Users can earn badges and receive encouragement through an integrated chatbot. The system logs and analyzes user performance over time.

## Features

- Score tracking and automatic badge awards.
- Integration with an encouragement chatbot that offers personalized motivational messages.
- Historical logging of ranks and scores.
- Badge and rank notifications with accompanying motivational messages and music.

## Getting Started

These instructions will help you get the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Pygame for music playback
- PIL for image handling
- tqdm for progress bar display
- dotenv for environment variable management

### Installation

1. Clone the repository:
   ```
   git clone https://yourrepositorylink.git
   ```
2. Install the necessary packages:
   ```
   pip install pygame Pillow tqdm python-dotenv
   ```

### Running the System

To run the system, execute the following script from the project's root directory:
```
bash run_honor_system.sh
```

This script initializes the `HonorSystem` and begins the score adjustment and badge awarding process based on user activity.

### Project Structure

- `run_honor_system.sh`: Script to start the system.
- `main.py`: Entry point of the application.
- `honor_system.py`: Core module that handles badge awards, score tracking, and music playback.
- `logger.py`: Module for logging ranks and score adjustments.
- `encouragement_llm.py`: Module that integrates with a chatbot for providing user encouragement.
- `todo.md`: Project tasks and roadmap.
- `music/`: Directory containing music files to be played upon earning badges.
- `badges/`: Directory containing badge images awarded to users.
- `test/`: Directory containing various test scripts to demonstrate system functionalities.
- `key.env`: Environment file storing necessary credentials for the chatbot.

### Configuration

The `key.env` file needs to be set up with the appropriate credentials:
- `SPARKAI_APP_ID`: App ID for the Spark AI.
- `SPARKAI_API_KEY`: API key for the Spark AI.
- `SPARKAI_API_SECRET`: API secret for the Spark AI.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Spark AI for the chatbot integration.
- Pygame community for the audio handling library.
- The Python Software Foundation for the comprehensive standard library.
