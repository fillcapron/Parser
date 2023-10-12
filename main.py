from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.companies import router as company_router
from models import companies
from models.database import engine

import logging

companies.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(
    router=company_router,
    prefix='/companies'
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())



#uvicorn main:app --reload
