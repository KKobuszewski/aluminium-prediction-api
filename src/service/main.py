
# set python path?
import os
import sys
sys.path.append(os.getcwd())

import logging
from pathlib import Path

from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.routing import APIRouter
#from fastapi.exception_handlers import request_validation_exception_handler
#from fastapi.exceptions import RequestValidationError

import uvicorn

# imports from project repo
import src.service.middlewares.correlation # import CorrelationIdMiddleware
import src.utils.logging
import src.utils.errors
import src.databases.redisutil

# set logging with unique process id (correlation_id)
src.utils.logging.setup_logging_with_correlation_id()

# -------- loading secrets
# load .env file to environment
#from dotenv import load_dotenv  # <--------------- Poetry does not support dotenv
#load_dotenv()
#API = os.getenv('API_VAR')
#print(API)
# in .env API_VAR=Test123APIkey


# ---------------------- startup & shutdown
# lifespan events instead of @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    https://fastapi.tiangolo.com/advanced/events/
    """
    logging.info("# Starting API and initializing all objects")
    
    redis_connector = src.databases.redisutil.RedisConnector(
        host='localhost',
        port=6379,          #os.getenv('REDIS_PORT'),
        password="12345",
    )
    app.state.redis_connector = redis_connector
    
    # Load the ML model
    # ...
    yield
    # Shutdown
    # Clean up the ML models and release the resources
    logging.info("# Closing connection to redis database.")
    app.state.redis_connector.redis_connector.close()
    logging.info("# Closing API.")
    


app = FastAPI(lifespan=lifespan)
app.add_middleware(src.service.middlewares.correlation.CorrelationIdMiddleware)

prefix_router = APIRouter(prefix="/alupred") # to be included after all @prefix_router calls


# -------------------- exception handlers

@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception):
    logging.critical(f"Unhandled error occured in the API.", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal server error"},
    )


# -------------------- API links

@prefix_router.get("/")
def welcome_page() -> PlainTextResponse:
    return PlainTextResponse("Aluminium Prediction API")




@prefix_router.get("/readiness")
def ready_check(request: Request) -> PlainTextResponse:
    request.app.state.redis_connector.is_alive()
    return PlainTextResponse("Ready")


@prefix_router.get("/health")
def health_check() -> PlainTextResponse:
    return PlainTextResponse("Healthy")



app.include_router(prefix_router) # have to be added after all @prefix_router calls



#parser = argparse.ArgumentParser()
#parser.add_argument('source', type=conn_string_type)
#parser.add_argument('destination', type=conn_string_type)
#options = parser.parse_args()


if __name__ == "__main__":
    print('# Before running uvicorn server.\n')
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
        workers=1,
        reload=False,
    )
    print('\n# After closing uvicorn server.')
