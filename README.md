# Choice-based Role Playing Game

This repository contains the code for a choice-based role-playing game developed for the HackUPC 2023 hackathon, sponsored by Vueling. The game is built as a REST API using FastAPI and utilizes OpenAI's GPT-3 for text generation.

## Introduction

The choice-based role-playing game allows players to engage in an interactive storytelling experience. The game is set in Barcelona and incorporates popular places as part of the narrative. Players make choices that influence the direction and outcome of the story.

## Requirements

To run the game locally, you need the following:

- Python 3.9 or above
- FastAPI
- OpenAI Python SDK
- Pexels API key

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/choice-based-rpg.git
```

2.  Install the required Python packages:
    

```bash    
    pip install -r requirements.txt
```

3.  Set up environment variables:
    
    -   `OPENAI_API_KEY`: Your OpenAI API key
    -   `PEXELS_API_KEY`: Your Pexels API key

## Usage

1.  Start the FastAPI server:
    
```bash
    uvicorn main:app --reload
```

2.  Access the game API at `http://localhost:8000` using an API client or web browser.
    
3.  Use the following endpoints to interact with the game:
    
    -   `GET /start`: Initiates the game and generates the first part of the story. Returns the story text and available choices.
    -   `GET /generate`: Generates the next part of the story based on the player's input. Returns the updated story text and new choices.

## API Endpoints

### GET /

Root endpoint that returns a welcome message.

### GET /start

Initiates the game and generates the first part of the story. Returns the story text and available choices.

### GET /generate

Generates the next part of the story based on the player's input. Returns the updated story text and new choices.

### GET /image

Performs an image search based on a query and returns the URL of the resulting image.

### GET /download

Downloads the requested image file.

## License

This project is licensed under the [MIT License](https://chat.openai.com/LICENSE).

## Acknowledgments

-   [FastAPI](https://fastapi.tiangolo.com/) - Fast web framework for building APIs with Python.
-   [OpenAI GPT-3](https://openai.com/) - Natural language processing model for text generation.
-   [Pexels API](https://www.pexels.com/api/) - API for accessing a vast collection of free stock photos.

## Contributing

Contributions are welcome! If you'd like to contribute to this project.
