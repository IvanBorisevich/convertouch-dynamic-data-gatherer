from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from routes import router as CurrencyRateRouter
import gatherer

app = FastAPI()
app.include_router(CurrencyRateRouter, tags=["CurrencyRates"], prefix="/currency-rates")

refresh_times_per_day = 4320
refresh_interval_sec = 24 * 60 * 60 / refresh_times_per_day

@app.on_event("startup")
@repeat_every(seconds = refresh_interval_sec, wait_first = True)
async def app_startup():
    gatherer.gather_currency_rates()


@app.on_event("shutdown")
async def app_shutdown():
    print('Convertouch Gatherer finished')


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome!"}
