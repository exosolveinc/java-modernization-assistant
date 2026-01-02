from typing import List, Dict, Optional
from pydantic import BaseModel

class MigrationPhase(BaseModel):
    phase_number: int
    name: str
    description: str
    openrewrite_recipes: List[str]
    manual_steps: List[str]
    risk_level: str
    estimated_effort_hours: int
    dependencies: List[int] = []

class MigrationPlan(BaseModel):
    project_name: str
    from_version: str
    to_version: str
    total_phases: int
    total_estimated_hours: int
    phases: List[MigrationPhase]
    testing_strategy: str
    rollback_plan: str
    risk_summary: str
