import json
import logging
import httpx
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = [],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)


