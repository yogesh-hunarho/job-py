from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import jobs, ai
from services.db import cache
from services.cleanup_service import cleanup_old_records

app = FastAPI(
    title="AI Job API",
    description="Job scraping + Gemini resume generator",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

@app.get("/")
def read_root():
    return {
        "AI": "This API fetches jobs from multiple job boards using JobSpy.",
        "endpoints": ["/api/jobs", "/status"],
    }

# ROUTES
app.include_router(jobs.router, prefix="/api")
app.include_router(ai.router, prefix="/api")


@app.get("/api/status")
def status():
    return {"status": "ok", "cached_records": cache.count_documents({})}

@app.get("/project-docs", include_in_schema=False)
async def custom_docs():
    return FileResponse("static/custom_docs.html")
