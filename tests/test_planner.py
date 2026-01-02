import pytest
from unittest.mock import MagicMock, patch
from src.planner.ai_planner import AIMigrationPlanner

@patch("src.planner.ai_planner.anthropic.Anthropic")
def test_create_plan_fallback(mock_anthropic, sample_analysis_report):
    # Mocking failure to trigger fallback
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = Exception("API Error")
    mock_anthropic.return_value = mock_client
    
    planner = AIMigrationPlanner()
    plan = planner.create_migration_plan(sample_analysis_report)
    
    assert plan.project_name == "Test Project"
    # Should use fallback plan
    assert plan.phases[0].name == "Automated Update"
