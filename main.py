from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from controller.currency_rate_routes import currency_rate_router as CurrencyRateRouter
import service.gatherer as gatherer

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Convertouch Gatherer is starting up...')
    await start_gathering_job()

    yield
    
    print('Convertouch Gatherer finished')

app = FastAPI(lifespan=lifespan)
app.include_router(CurrencyRateRouter, tags=["CurrencyRates"], prefix="/currency-rates")

refresh_times_per_day = 1
refresh_interval_sec = 24 * 60 * 60 / refresh_times_per_day


@repeat_every(seconds = refresh_interval_sec, wait_first = True)
async def start_gathering_job():
    gatherer.gather_currency_rates()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome!"}
