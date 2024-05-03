from fastapi import FastAPI

from routes import router as CurrencyRateRouter

app = FastAPI()

app.include_router(CurrencyRateRouter, tags=["CurrencyRates"], prefix="/currency-rates")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome!"}