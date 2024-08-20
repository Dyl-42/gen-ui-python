import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from fastapi.staticfiles import StaticFiles


from gen_ui_backend.chain import create_graph
from gen_ui_backend.custom_types import ChatInputType
from gen_ui_backend.custom_types import GenericOutputType
from gen_ui_backend.tools.code_interpreter import CodeExecutionResult as CodeExecutionOutput

def start() -> None:
    app = FastAPI(
        title="Gen UI Backend",
        version="1.0",
        description="A simple API server using Langchain's Runnable interfaces",
    )

    # Configure CORS
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount the charts directory
    charts_dir = "/Users/dylangoode/Documents/Research/edd/testy/backend/charts"
    app.mount("/charts", StaticFiles(directory=charts_dir), name="charts")

    graph = create_graph()

    # runnable = graph.with_types(input_type=ChatInputType, output_type=dict)
    runnable = graph.with_types(input_type=ChatInputType, output_type=GenericOutputType)

    add_routes(app, runnable, path="/chat", playground_type="chat")
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
