import click
import json
import os
from pathlib import Path
from loguru import logger
from analyzer.emt4j_wrapper import EMT4JAnalyzer
from planner.ai_planner import AIMigrationPlanner
from transformer.openrewrite_wrapper import OpenRewriteTransformer
from validator.compilation_validator import CompilationValidator
from utils.logging_config import setup_logging
from models.migration_plan import MigrationPlan

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose logging")
def cli(verbose):
    """Java Modernization Assistant CLI"""
    if verbose:
        os.environ["LOG_LEVEL"] = "DEBUG"
    setup_logging()

@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--from-version', default=8, help="Current Java version")
@click.option('--to-version', default=21, help="Target Java version")
@click.option('--output', default="analysis-report.json", help="Output file for report")
def analyze(project_path, from_version, to_version, output):
    """Analyze a legacy Java project."""
    analyzer = EMT4JAnalyzer()
    analyzer.install_emt4j()
    
    report = analyzer.analyze_project(project_path, from_version, to_version)
    
    with open(output, 'w') as f:
        f.write(report.model_dump_json(indent=2))
        
    logger.info(f"Analysis complete. Report saved to {output}")

@cli.command()
@click.argument('project_path')
@click.option('--analysis', required=True, help="Path to analysis report")
@click.option('--output', default="migration-plan.json", help="Output file for plan")
def plan(project_path, analysis, output):
    """Generate a migration plan using AI."""
    from models.analysis import AnalysisReport
    
    with open(analysis, 'r') as f:
        data = json.load(f)
        report = AnalysisReport(**data)
        
    planner = AIMigrationPlanner()
    migration_plan = planner.create_migration_plan(report)
    
    with open(output, 'w') as f:
        f.write(migration_plan.model_dump_json(indent=2))
        
    logger.info(f"Plan generated. Saved to {output}")
    print(f"Plan Summary: {migration_plan.total_phases} phases, {migration_plan.total_estimated_hours} hours estimated.")

@cli.command()
@click.argument('project_path')
@click.option('--plan', required=True, help="Path to migration plan")
@click.option('--phase', type=int, required=True, help="Phase number to execute")
@click.option('--dry-run', is_flag=True, help="Dry run mode")
def transform(project_path, plan, phase, dry_run):
    """Execute a transformation phase."""
    with open(plan, 'r') as f:
        data = json.load(f)
        migration_plan = MigrationPlan(**data)
        
    target_phase = next((p for p in migration_plan.phases if p.phase_number == phase), None)
    if not target_phase:
        logger.error(f"Phase {phase} not found in plan")
        return

    transformer = OpenRewriteTransformer()
    result = transformer.run_recipes(project_path, target_phase.openrewrite_recipes, dry_run)
    
    if result.success:
        logger.info("Transformation successful")
    else:
        logger.error(f"Transformation failed: {result.errors}")

@cli.command()
@click.argument('project_path')
def validate(project_path):
    """Validate project compilation and tests."""
    validator = CompilationValidator()
    result = validator.validate_project(project_path)
    
    if result.compilation_passed and result.unit_tests_passed:
        logger.success("Validation PASSED")
    else:
        logger.error("Validation FAILED")
        if not result.compilation_passed:
            logger.error("Compilation failed")
        if not result.unit_tests_passed:
            logger.error(f"Tests failed: {result.failed_tests}")

if __name__ == '__main__':
    cli()
