import pytest
from src.analyzer.emt4j_wrapper import EMT4JAnalyzer

def test_analyze_project_structure(sample_project_path):
    analyzer = EMT4JAnalyzer()
    report = analyzer.analyze_project(sample_project_path, 8, 21)
    
    assert report.from_version == 8
    assert report.to_version == 21
    assert report.project_name == "sample-project"
    assert report.total_issues > 0
