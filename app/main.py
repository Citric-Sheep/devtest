# from fastapi import FastAPI
# from . import models
# from .db import engine
# from .routes import router as api_router

from fastapi import FastAPI
import models
from db import engine
from routes import router as api_router

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Include the API routes
app.include_router(api_router)


@app.get('/')
async def root():
    return {"message": "Hello World!"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
