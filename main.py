from contextlib import asynccontextmanager

from fastapi import FastAPI
from controller.currency_rate_routes import currency_rate_router as CurrencyRateRouter
from service.job_manager import start_jobs

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Convertouch Gatherer is starting up...')
    await start_jobs()

    yield
    
    print('Convertouch Gatherer finished')

app = FastAPI(lifespan=lifespan)
app.include_router(CurrencyRateRouter, tags=["CurrencyRates"], prefix="/currency-rates")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome!"}
