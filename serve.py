from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

generic_template="Translate the following into {language}: "

prompt = ChatPromptTemplate.from_messages(
    [('system',generic_template),('user','{text}')]
)

parser=StrOutputParser()

chain=prompt|model|parser

app=FastAPI(title="Langchain Server",version="1.0",description="Simple server")

# APP DEFINITION

add_routes(
    app,
    chain,
    path='/chain'
)

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000)
