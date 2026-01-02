from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class EMT4JIssue(BaseModel):
    file_path: str
    line_number: int = 0
    issue_code: str
    priority: str
    description: str
    suggestion: str
    category: str
    auto_fixable: bool = False

class AnalysisReport(BaseModel):
    project_name: str
    from_version: int
    to_version: int
    timestamp: str
    total_issues: int
    auto_fixable_count: int
    issues_by_category: Dict[str, List[EMT4JIssue]]
    issues_by_priority: Dict[str, List[EMT4JIssue]]
    raw_report: Optional[Dict[str, Any]] = None
