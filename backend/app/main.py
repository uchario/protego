from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import engine, get_db, Base
from .exceptions import DatabaseError, NotFoundError
from .services import PageVisitService
from .schemas import PageVisitCreate, PageVisitResponse

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized error handlers
@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc: DatabaseError):
    return JSONResponse(
    status_code=500,
    content={"detail": f"Database error: {str(exc)}"}
    )
@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc: NotFoundError):
    return JSONResponse(
    status_code=404,
    content={"detail": f"Not found: {str(exc)}"}
    )

@app.post("/store", response_model=PageVisitResponse)
def store_visit(visit: PageVisitCreate, db: Session = Depends(get_db)):
    try:
        return PageVisitService.create_visit(db, visit)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def get_metrics(url: str, db: Session = Depends(get_db)):
    try:
        return PageVisitService.get_latest_metrics(db, url)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(url: str, db: Session = Depends(get_db)):
    try:
        return PageVisitService.get_visit_history(db, url)
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))