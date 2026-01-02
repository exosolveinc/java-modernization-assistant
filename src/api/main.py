from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from analyzer.emt4j_wrapper import EMT4JAnalyzer
from planner.ai_planner import AIMigrationPlanner
from models.analysis import AnalysisReport
from models.migration_plan import MigrationPlan

app = FastAPI(title="Java Modernization Assistant API")

class AnalyzeRequest(BaseModel):
    project_path: str
    from_version: int = 8
    to_version: int = 21

class PlanRequest(BaseModel):
    analysis_report: AnalysisReport

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Java Modernization Assistant"}

@app.post("/api/analyze", response_model=AnalysisReport)
def analyze_project(request: AnalyzeRequest):
    """Analyze a project and return the report."""
    try:
        analyzer = EMT4JAnalyzer()
        report = analyzer.analyze_project(request.project_path, request.from_version, request.to_version)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan", response_model=MigrationPlan)
def generate_plan(request: PlanRequest):
    """Generate a migration plan from an analysis report."""
    try:
        planner = AIMigrationPlanner()
        plan = planner.create_migration_plan(request.analysis_report)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
