import subprocess
import os
from pathlib import Path
from typing import List
from loguru import logger
from utils.config import settings
from utils.file_utils import detect_build_tool
from models.transformation import TransformationResult

class OpenRewriteTransformer:
    def __init__(self):
        self.maven_plugin_version = settings.OPENREWRITE_MAVEN_PLUGIN_VERSION

    def run_recipes(self, project_path: str, recipes: List[str], dry_run: bool = False) -> TransformationResult:
        """Run OpenRewrite recipes on the project."""
        build_tool = detect_build_tool(project_path)
        
        logger.info(f"Detected build tool: {build_tool}")
        logger.info(f"Applying recipes: {recipes}")
        
        recipes_arg = ",".join(recipes)
        
        try:
            if build_tool == "maven":
                self._run_maven(project_path, recipes_arg, dry_run)
            elif build_tool == "gradle":
                self._run_gradle(project_path, recipes_arg, dry_run)
            else:
                return TransformationResult(
                    success=False,
                    changed_files=[],
                    diff="",
                    errors=["Unsupported build tool"],
                    compilation_success=False
                )
                
            return TransformationResult(
                success=True,
                changed_files=[], # In real impl, parse output
                diff="", # In real impl, generate patch
                errors=[],
                compilation_success=True
            )
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Transformation failed: {e.output}")
            return TransformationResult(
                success=False,
                changed_files=[],
                diff="",
                errors=[str(e)],
                compilation_success=False
            )

    def _run_maven(self, project_path: str, recipes: str, dry_run: bool):
        cmd = [
            "./mvnw" if (Path(project_path) / "mvnw").exists() else "mvn",
            "rewrite:run" if not dry_run else "rewrite:dryRun",
            f"-Drewrite.activeRecipes={recipes}"
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=project_path, check=True, capture_output=True, text=True)

    def _run_gradle(self, project_path: str, recipes: str, dry_run: bool):
        cmd = [
            "./gradlew" if (Path(project_path) / "gradlew").exists() else "gradle",
            "rewriteRun" if not dry_run else "rewriteDryRun",
            f"-Drewrite.activeRecipes={recipes}"
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=project_path, check=True, capture_output=True, text=True)
