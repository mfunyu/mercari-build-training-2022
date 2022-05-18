import os
import logging
import pathlib
import db 
import hashlib
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "images"
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

    return items

@app.get("/search")
def search_item(keyword: str = ""):
    items = db.find_item(keyword)
    
    return {"items": items}

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...), image: UploadFile = File(...)):
    logger.info(f"Receive item: {name}")
    
    try:
        contents = image.file.read()
    except:
        logger.error("File read error")

    image_name = hashlib.sha256(image.filename.replace(".jpg", "").encode('utf-8')).hexdigest() + ".jpg"
    db.add_item(name, category, image_name)
    
    # save under image/
    path = images / image_name
    with open(path, "wb") as f:
        f.write(contents)

    return {"message": f"item received: {name}"}

@app.get("/items/{item_id}")
def get_item_details(item_id):
    return db.find_item(int(item_id))

@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.info(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)