from fastapi import FastAPI
import openai
import psycopg2
import uvicorn
import random
import os

app = FastAPI()

openai.api_key='API_KEY'

url=os.getenv("DATABASE_URL")
connection=psycopg2.connect(url)

DROP_TABLE="DROP TABLE IF EXISTS response_table"
CREATE_TABLE="CREATE TABLE IF NOT EXISTS response_table (id SERIAL PRIMARY KEY, query TEXT, question TEXT, answer TEXT);"
INSERT_QUERY="INSERT INTO response_table (query, question, answer) VALUES (%s,%s, %s)"

@app.get("/")
async def root():
    return {"message": "Hello World"}


#get user text input
@app.get("/items/")
async def create_item(item: str):

    text = item
    processed_text = text.lower()

    ret=[]
    with connection:
        with connection.cursor() as cursor:
            #cursor.execute(DROP_TABLE)
            cursor.execute(CREATE_TABLE)
            #check if processed_text is already in the database
            cursor.execute("SELECT * FROM response_table WHERE query=%s",(processed_text,))
            result=cursor.fetchall()
            #add processed_text to the database if it's not already there
            #use openai to generate a response and add it to the database
            if result is not None:
                #append all the responses from result to ret
                for i in range(len(result)):
                    #ret.append(result[i][2])
                    #create a tuple of processed_text, question and answer and append it to ret
                    ret.append((result[i][1],result[i][2],result[i][3]))
                #select random 5 responses from ret
                k=5
                if len(ret)<5:
                    k=len(ret)
                ret=random.sample(ret,k)
            
            for i in range(5-len(ret)):
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Tell me an interview questions for "+processed_text+" with answer",
                    temperature=0.9,
                    max_tokens=3500,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0.6)
                response=response['choices'][0]['text']
                #split response into question and answer
                response=response.split("A: ")

                if len(response)==1:
                    #print('skipped')
                    continue

                q=response[0].replace("Q: ","")
                a=response[1]
                #check if question is already in the database
            #    cursor.execute("SELECT * FROM response_table WHERE question=%s",(q,))
            #    result=cursor.fetchall()
                #check if result is empty
            #    if len(result)!=0:
                    #append first result to ret
            #       ret.append((result[0][1],result[0][2],result[0][3]))
            #        response = openai.Completion.create(
            #        model="text-davinci-003",
            #        prompt="Tell me an interview questions for "+processed_text+" with answer, Do not include this question "+q+" in the response",
            #        temperature=0.9,
            #        max_tokens=3500,
            #        top_p=1,
            #        frequency_penalty=0,
            #        presence_penalty=0.6)
            #        response=response['choices'][0]['text']
                    #split response into question and answer
            #        response=response.split("A: ")
            #        if len(response)==1:
                        #print('skipped')
            #           continue
            #        q=response[0].replace("Q: ","")
            #        a=response[1]
                    #check if question is already in the database
            #        cursor.execute("SELECT * FROM response_table WHERE question=%s",(q,))
            #        result=cursor.fetchall()
            #        if len(result)!=0:
            #            ret.append((result[0][1],result[0][2],result[0][3]))
            #    else:
                #add processed_text, question and answer to the database
                ret.append((processed_text,q,a))
                cursor.execute(INSERT_QUERY,(processed_text,q,a))
                connection.commit()
                #create a tuple of processed_text, question and answer and append it to ret

            #create a json object to return
            json_ret={}
            for i in range(len(ret)):
                json_ret[i]={"query":ret[i][0],"question":ret[i][1],"answer":ret[i][2],"qna":ret[i][1][2:]+"\n\n"+ret[i][2]}
            return json_ret

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

