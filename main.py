from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel 
import requests
import re
from typing import Optional, List 
import uvicorn 
import os 
