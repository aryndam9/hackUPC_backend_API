from fastapi import FastAPI
import openai
import uvicorn
import os

app = FastAPI()
story = ""
# get api from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/start")
def start_game():
    global story
    story = "Once upon a time in Barcelona..."
    return {"message": "The game has started."}


@app.get("/generate")
def generate_story(player_id: int, player_input: str):
    global story
    
    # Call the OpenAI Chat GPT API and generate the next part of the story based on the player's input
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a storyteller in Barcelona."},
            {"role": "user", "content": player_input},
            {"role": "assistant", "content": story},
        ],
    )
    
    # Extract the generated text from the API response
    generated_text = completion.choices[0].message["content"]
    
    # Update the story based on the generated text and the player's input
    story += f"\n{player_input}\n{generated_text}\n"
    
    return {"story": story}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
