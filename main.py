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
        posts = Parser(data['companyName'],  data['queries'])
        logger.info(posts)
        return {"res": f"{data['companyName']}"}
    else:
        return {"error": "Ошибка"}


if __name__ == "__main__":
    run()
