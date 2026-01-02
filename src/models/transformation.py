from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class TransformationResult(BaseModel):
    success: bool
    changed_files: List[str]
    diff: str
    errors: List[str]
    compilation_success: bool
    test_results: Optional[Dict[str, Any]] = None

class ValidationResult(BaseModel):
    compilation_passed: bool
    unit_tests_passed: bool
    failed_tests: List[str]
    code_coverage_delta: float
    new_issues_found: List[str]
