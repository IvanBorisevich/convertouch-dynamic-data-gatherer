import asyncio
from contextlib import asynccontextmanager
import functools

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from controller.currency_rate_routes import currency_rate_router as CurrencyRateRouter
import service.gatherer as gatherer

DELAY_BETWEEN_JOBS_START_IN_SECONDS = 30 * 60

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Convertouch Gatherer is starting up...')
    await start_jobs()

    yield
    
    print('Convertouch Gatherer finished')

app = FastAPI(lifespan=lifespan)
app.include_router(CurrencyRateRouter, tags=["CurrencyRates"], prefix="/currency-rates")


async def start_jobs():
    for job in gatherer.gathering_jobs:
        repeat_every_in_sec = 24 * 60 * 60 / job["run_times_per_day"]
        
        task_with_args = functools.partial(gatherer.start_gathering_job, job)

        repeated_func = repeat_every(seconds=repeat_every_in_sec)(task_with_args)
        
        # Run each wrapped function as a background task
        asyncio.create_task(repeated_func())

        await asyncio.sleep(DELAY_BETWEEN_JOBS_START_IN_SECONDS)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome!"}
