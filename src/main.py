from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.database import engine, Base
from src.routes import demands, elevators

# Create the database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Elevator Demand Prediction System",
    description="API for collecting elevator demand data to train prediction models for optimal resting floors",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(elevators.router, prefix="/elevators", tags=["elevators"])
app.include_router(demands.router, prefix="/demands", tags=["demands"])

@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "title": "Elevator Demand Prediction System",
        "version": "1.0.0",
        "description": "API for collecting elevator demand data to train prediction models for optimal resting floors"
    }

@app.get("/health")
def health_check():
    """Health check endpoint to verify the API and database are working."""
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
