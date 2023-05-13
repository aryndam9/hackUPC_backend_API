from fastapi import FastAPI
import openai
import uvicorn

app = FastAPI()
story = ""
openai.api_key = "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"

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/start")
def start_game():
    global story
    story = "Once upon a time..."
    return {"message": "The game has started."}


@app.get("/generate")
def generate_story(player_id: int, player_input: str):
    global story
    
    # Call the OpenAI Chat GPT API and generate the next part of the story based on the player's input
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a funny comedian who tells dad jokes."},
            {"role": "user", "content": "Write a dad joke related to numbers."},
            {"role": "assistant", "content": "Q: How do you make 7 even? A: Take away the s."},
            {"role": "user", "content": "Write one related to programmers."},
        ],
    )
    
    # Extract the generated text from the API response
    generated_text = completion.choices[0].message["content"]
    
    # Update the story based on the generated text and the player's input
    story += f"{generated_text}\n"
    
    return {"story": story}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
