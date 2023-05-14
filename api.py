from fastapi import FastAPI
import openai
import uvicorn
import os
import re



app = FastAPI()
story = ""
# get api from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]



def split_paragraph(paragraph, chunk_size):
    words = paragraph.split()
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def get_options(text):
    # start with '}}' end end with \n
    
    lines = text.split('\n')
    options = []

    for line in lines:
        line = line.strip()
        if line.startswith('{{') and '}}' in line:
            option = line[line.index('}}') + 2:].strip()
            options.append(option)
    
    return options


@app.get("/")
def read_root():
    return {"HackUPC 2023": "Welcome to our HackUPC 2023 project!"}


@app.get("/start")
def start_game():
    global story
    story = ""
    
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are an engaging storyteller, the story would be set in Barcelona, it would include all the popular places in Barcelona. You will come up with entertaining stories that are engaging, and has immersive choices for the user. Genre of the story can be thriller, suspense or historical fiction.\
            Your response should be in the format of\
            AI - Here you will give buildup for a cohesive story. (Dont make it too long) \
            \
            After the buildup You Will always ask a immersive question and give immersive situations to choose from so that the user can choose and a story can be build around it.\
            Each choices should be less than 3 words \n \
             Example:\
            {{1}} Choice  \n \
            {{2}} Choice  \n \
            {{3}} Choice  \n \
            The number of choices ideally should be 3 but can be upto 5.\
            \
            Wait for the user to choose an option. \
            \
            My first request is “Start the immersive choice based story for me based in barcelona."},
                    ],
                    stop=["User", "User"],
            )

    start_text = completion.choices[0].message["content"]
    story += f"\n{start_text}\n"
    # get text after AI - and '{{' from start_text
    start_text_clean = start_text[: start_text.find("{{")].strip()
    # remove if start_text_clean contains 'AI -'
    if 'AI' in start_text_clean:
        start_text_clean = start_text_clean.replace('AI', '')
    # split start_text_clean into 299 character chunks with full words
    start_text_chunks = split_paragraph(start_text_clean, 299)
    options = get_options(start_text)
    return {
        "Text": start_text_chunks,
            "Options": options
            }



@app.get("/generate")
def generate_story(player_id: int, player_input: str):
    global story
    
    # Call the OpenAI Chat GPT API and generate the next part of the story based on the player's input
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": story},
            {"role": "user", "content": player_input},
            {"role": "assistant", "content": "Here you will give buildup for a cohesive story. (Dont make it too long) \
            After the buildup You Will always ask a immersive question and give immersive choices so that the user can choose and a story can be build around it.\
            Each choices should be less than 3 words \n \
             Example:\
            {{1}} Choice  \n \
            {{2}} Choice  \n \
            {{3}} Choice  \n \
            The number of choices ideally should be 3 but can be upto 5.\
            Wait for the user to choose an option."}
        ],
    )
    
    # Extract the generated text from the API response
    generated_text = completion.choices[0].message["content"]
    
    # Update the story based on the generated text and the player's input
    story += f"\nUser chose {player_input}\nAI- {generated_text}\n"
    # get the line after User chose Num using regex
    generated_text_ai_part = generated_text[ : generated_text.find("{{")].strip()
    # split generated_text into 299 character chunks with full words
    generated_text_chunks = split_paragraph(generated_text_ai_part, 299)
    options = get_options(generated_text)

    
    return {
        "Text": generated_text_chunks,
        "Options": options
    }




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
