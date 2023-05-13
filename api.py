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
    regex = r"\{\{[0-9]+\}\}(.*)"
    matches = re.finditer(regex, text, re.MULTILINE)
    options = []
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            option = match.group(groupNum)
            option = option[:33]
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
            {"role": "system", "content": "I want you to act as an engaging storyteller, the story would be set in Barcelona, including all the popular places Barcelona has. You will come up with entertaining stories that are engaging, imaginative, and captivating for the user. It can be suspense or thriller or any other type of story which has the potential to capture people's attention and imagination.\
            Your response should be in the format of\
            AI - Here it would give context. \
            \
            AI - Will ask a question and give probable options to choose from by the user.\
            Rules for how the options should be \
            - options should look like this {{Num}} Option, where Num is the serial number\
            - options should not be more than 3 words.\
            -There only can be a maximum of 5 choices but try to keep 3 choices mostly.\
            \
            Wait for the user to choose an option. \
            My first request is “I need an engaging choice-based story set in Barcelona."},
                    ],
                    stop=["User:"],
            )

    start_text = completion.choices[0].message["content"]
    story += f"\n{start_text}\n"
    # get text after AI - and '{{' from start_text
    start_text_clean = start_text[start_text.find("AI -") + 5 : start_text.find("{{")].strip()
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
        ],
    )
    
    # Extract the generated text from the API response
    generated_text = completion.choices[0].message["content"]
    print(generated_text)
    
    # Update the story based on the generated text and the player's input
    story += f"\nUser chose {player_input}\n{generated_text}\n"
    # get the line after User chose Num using regex
    generated_text[generated_text.find("User chose") + 12 : generated_text.find("AI -")].strip()
    # split generated_text into 299 character chunks with full words
    generated_text_chunks = split_paragraph(generated_text, 299)
    options = get_options(generated_text)

    
    return {
        "Text": generated_text_chunks,
        "Options": options
    }




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
