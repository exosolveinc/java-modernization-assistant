import pytest
from pathlib import Path
from src.models.analysis import AnalysisReport, EMT4JIssue

@pytest.fixture
def sample_analysis_report():
    return AnalysisReport(
        project_name="Test Project",
        from_version=8,
        to_version=21,
        timestamp="2024-05-14T10:00:00Z",
        total_issues=1,
        auto_fixable_count=1,
        issues_by_category={
            "removed_api": [
                EMT4JIssue(
                    file_path="src/main/java/App.java",
                    issue_code="jdk.removed.api",
                    priority="P1",
                    description="Removed API",
                    suggestion="Fix it",
                    category="removed_api",
                    auto_fixable=True
                )
            ]
        },
        issues_by_priority={"P1": []}
    )

@pytest.fixture
def sample_project_path(tmp_path):
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()
    (project_dir / "pom.xml").touch()
    return str(project_dir)
