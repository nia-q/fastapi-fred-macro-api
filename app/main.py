from fastapi import FastAPI
from app.api import macro

app = FastAPI(title="FRED Macro API")

app.include_router(macro.router, prefix="/macro")
