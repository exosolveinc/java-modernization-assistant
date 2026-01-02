import json
from typing import Dict, Any
import anthropic
from loguru import logger
from utils.config import settings
from models.analysis import AnalysisReport
from models.migration_plan import MigrationPlan, MigrationPhase

class AIMigrationPlanner:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEE, base_url=settings.ANTHROPIC_BASE_URL)
        self.model = settings.AI_MODEL

    def create_migration_plan(self, report: AnalysisReport) -> MigrationPlan:
        """Generate a migration plan using Claude."""
        logger.info("Generating migration plan with Claude...")
        logger.info("Using ANTHROPIC API KEY: ", settings.ANTHROPIC_API_KEE)
        prompt = self._build_planning_prompt(report)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=settings.AI_MAX_TOKENS,
                temperature=0,
                system="You are an expert Java Architect specializing in legacy migrations. "
                       "Create a phased migration plan in JSON format.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text
            return self._parse_response(response_text, report)
            
        except Exception as e:
            logger.error(f"Failed to generate plan: {e}")
            # Return a fallback plan for robustness
            return self._create_fallback_plan(report)

    def _build_planning_prompt(self, report: AnalysisReport) -> str:
        return f"""
        Analyze this Java project report and create a migration plan from Java {report.from_version} to {report.to_version}.
        
        Project: {report.project_name}
        Total Issues: {report.total_issues}
        Categories: {list(report.issues_by_category.keys())}
        
        Please generate a JSON response with the following structure:
        {{
            "phases": [
                {{
                    "phase_number": 1,
                    "name": "Phase Name",
                    "description": "What this phase achieves",
                    "openrewrite_recipes": ["recipe.name (e.g., org.openrewrite.java.migrate.Java8toJava11)"],
                    "manual_steps": ["step description"],
                    "risk_level": "LOW|MEDIUM|HIGH",
                    "estimated_effort_hours": 4
                }}
            ],
            "testing_strategy": "Description",
            "rollback_plan": "Description",
            "risk_summary": "Description"
        }}

        CONTEXT: VALID OPENREWRITE RECIPES (Use ONLY these or known valid ones)
        
        Version Migration:
        - org.openrewrite.java.migrate.Java8toJava11
        - org.openrewrite.java.migrate.UpgradeToJava17
        - org.openrewrite.java.migrate.UpgradeToJava21

        Cleanup & Refactoring:
        - org.openrewrite.java.format.AutoFormat
        - org.openrewrite.java.RemoveUnusedImports
        - org.openrewrite.staticanalysis.RemoveUnusedPrivateFields
        - org.openrewrite.staticanalysis.CommonStaticAnalysis
        - org.openrewrite.java.cleanup.UnnecessaryCloseInTryWithResources
        - org.openrewrite.java.cleanup.ExplicitInitialization
        """

    def _parse_response(self, response: str, report: AnalysisReport) -> MigrationPlan:
        # Simple extraction of JSON
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            data = json.loads(json_str)
            
            phases = [MigrationPhase(**p) for p in data.get("phases", [])]
            
            return MigrationPlan(
                project_name=report.project_name,
                from_version=str(report.from_version),
                to_version=str(report.to_version),
                total_phases=len(phases),
                total_estimated_hours=sum(p.estimated_effort_hours for p in phases),
                phases=phases,
                testing_strategy=data.get("testing_strategy", "Standard unit testing"),
                rollback_plan=data.get("rollback_plan", "Git revert"),
                risk_summary=data.get("risk_summary", "Standard migration risks")
            )
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return self._create_fallback_plan(report)

    def _create_fallback_plan(self, report: AnalysisReport) -> MigrationPlan:
        """Create a default plan if AI fails."""
        return MigrationPlan(
            project_name=report.project_name,
            from_version=str(report.from_version),
            to_version=str(report.to_version),
            total_phases=1,
            total_estimated_hours=8,
            phases=[
                MigrationPhase(
                    phase_number=1,
                    name="Automated Update",
                    description="Standard OpenRewrite migration",
                    openrewrite_recipes=["org.openrewrite.java.migrate.UpgradeJavaVersion"],
                    manual_steps=["Verify compilation"],
                    risk_level="MEDIUM",
                    estimated_effort_hours=8
                )
            ],
            testing_strategy="Run existing tests",
            rollback_plan="Git revert",
            risk_summary="Automated fallback plan due to AI error"
        )
