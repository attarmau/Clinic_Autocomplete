from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import signal
import sys
import uvicorn
import argparse
import yaml
from routers import autocomplete_router
from utils import global_settings
import os
from dotenv import load_dotenv

# Determine environment
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="./config/default.yml")
parser.add_argument("-p", "--port", default=8588)
parser.add_argument("-d", "--debug", default=0)

args = parser.parse_args()
port = int(args.port)
try:
    debug = bool(int(args.debug))
except:
    debug = False

print(f"debug={debug}")
config = args.config.lower()
print(f"port={port}, config={config}")

# Load Config
CONFIG = yaml.safe_load(open(config))

load_dotenv()
ELASTIC_HOST = os.getenv('ELASTIC_HOST')
if ELASTIC_HOST:
    print(f"Setting elastic host from Environment=>{ELASTIC_HOST}")
    CONFIG["elastic_host"]=ELASTIC_HOST
else:
    print(f"Getting elastic host from Yaml=>{CONFIG["elastic_host"]}")

# Initialize global settings
global_settings.init('search', CONFIG, True)

# Global Logger
_logger = global_settings._logger

# AutoComplete Manager
_autocomplete_mgr = global_settings._autocomplete_mgr

# Define a signal handler to catch SIGINT (Ctrl+C) and exit gracefully.
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # cleanup
    _autocomplete_mgr.cleanup()
    sys.exit(0)

# Create an instance of FastAPI to serve as the main application.
app = FastAPI(
    title=CONFIG['title'],
    version=CONFIG['version'],
    description=CONFIG['description'],
)

# Create an instance of APIRouter to define the autocomplete routes.
# Add the autocomplete routes to the main application.
# Add the item routes to the main application.
router = APIRouter()
app.include_router(autocomplete_router.router, prefix=f"{CONFIG['prefix']}/autocomplete")

# Configure CORS middleware to allow all origins, enabling cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Define a liveness check endpoint.
@app.get("/liveness")
def liveness():
    """
    Define a liveness check endpoint.

    This route is used to verify that the API is operational and responding to requests.

    Returns:
        A simple string message indicating the API is working.
    """
    return 'API Works!'

# Start the FastAPI application using Uvicorn.
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    _logger.info(f"{CONFIG['title']} {CONFIG['version']} started on {CONFIG['port']}")
    #uvicorn.run(app, host="0.0.0.0", port=CONFIG['port'])
    uvicorn.run("api_server:app", host="0.0.0.0", port=CONFIG['port'], reload=debug)
