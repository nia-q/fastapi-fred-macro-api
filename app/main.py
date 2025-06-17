from fastapi import FastAPI
from app.api import macro

app = FastAPI(title="Macroeconomic Insight API")

app.include_router(macro.router, prefix="/macro")
