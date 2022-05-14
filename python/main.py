import os
import logging
import pathlib
import db 
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)
db.init()

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_items():
    items = db.get_items()

    return {"items": items}

@app.get("/search")
def search_item(keyword: str = ""):
    items = db.find_item(keyword)
    
    return {"items": items}

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...), image: str = Form(...)):
    logger.info(f"Receive item: {name}")

    db.add_item(name, category, image)
    
    return {"message": f"item received: {name}"}

@app.get("/items/{item_id}")
def get_item_details(item_id):
    return db.find_item(int(item_id))

@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.info(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
