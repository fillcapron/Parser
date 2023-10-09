from fastapi import FastAPI, Body
from src.parser import Parser
import logging

app = FastAPI()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@app.post('/parser')
def run(data = Body()):

    if data['companyName'] and data['queries']:
        parser = Parser(data['companyName'],  data['queries'])
        posts = parser.parser()
        return {"res": f"{posts}"}
    else:
        return {"error": "Ошибка"}


if __name__ == "__main__":
    #uvicorn main:app --reload
    run()
