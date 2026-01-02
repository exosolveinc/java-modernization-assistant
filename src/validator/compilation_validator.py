import subprocess
from pathlib import Path
from loguru import logger
from utils.file_utils import detect_build_tool
from models.transformation import ValidationResult

class CompilationValidator:
    def validate_project(self, project_path: str) -> ValidationResult:
        """Run compilation and tests to validate the project."""
        build_tool = detect_build_tool(project_path)
        logger.info(f"Validating project using {build_tool}")
        
        compilation_passed = False
        tests_passed = False
        failed_tests = []
        
        try:
            if build_tool == "maven":
                # Compile
                subprocess.run(["mvn", "clean", "compile"], cwd=project_path, check=True, capture_output=True)
                compilation_passed = True
                
                # Test
                subprocess.run(["mvn", "test"], cwd=project_path, check=True, capture_output=True)
                tests_passed = True
                
            elif build_tool == "gradle":
                # Compile
                subprocess.run(["./gradlew", "classes"], cwd=project_path, check=True, capture_output=True)
                compilation_passed = True
                
                # Test
                subprocess.run(["./gradlew", "test"], cwd=project_path, check=True, capture_output=True)
                tests_passed = True
                
        except subprocess.CalledProcessError as e:
            logger.error("Validation failed")
            # In a real impl, parse output to get failed tests
            failed_tests = ["Simulation: Test failed"]
            
        return ValidationResult(
            compilation_passed=compilation_passed,
            unit_tests_passed=tests_passed,
            failed_tests=failed_tests if not tests_passed else [],
            code_coverage_delta=0.0,
            new_issues_found=[]
        )
