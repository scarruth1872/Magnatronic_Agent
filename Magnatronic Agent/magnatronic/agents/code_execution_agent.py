from magnatronic.core.agent import Agent
from magnatronic.core.tasks import Task
from typing import Dict, Any, List, Tuple
import asyncio
import sys
import io
import ast
import inspect
import traceback
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import dataclass
from memory_profiler import profile

class CodeExecutionAgent(Agent):
    def __init__(self):
        super().__init__("code_execution_agent")
        self.supported_libraries = [
            "numpy",
            "pandas",
            "scikit-learn",
            "matplotlib",
            "tensorflow",
            "torch",
            "seaborn",
            "statsmodels",
            "xgboost",
            "lightgbm",
            "nltk",
            "scipy"
        ]
        self.execution_history = []
        self.memory_threshold = 1024 * 1024 * 1024  # 1GB

    def validate_code(self, code: str) -> bool:
        """Validate code for security concerns before execution."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Check for potentially dangerous operations
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    module = node.names[0].name.split('.')[0]
                    if module not in self.supported_libraries:
                        raise ValueError(f"Import of {module} is not allowed")
                # Prevent file operations
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in ['open', 'eval', 'exec']:
                        raise ValueError(f"Use of {node.func.id}() is not allowed")
            return True
        except Exception as e:
            raise ValueError(f"Code validation failed: {str(e)}")

    async def execute_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute Python code in a controlled environment."""
        # Validate code before execution
        self.validate_code(code)

        # Capture stdout and stderr
        output = io.StringIO()
        error = io.StringIO()

        try:
            # Execute code with timeout
            with redirect_stdout(output), redirect_stderr(error):
                # Create a local namespace for execution
                local_ns = {}
                exec(code, {}, local_ns)

            return {
                "success": True,
                "output": output.getvalue(),
                "error": error.getvalue(),
                "result": local_ns.get('result', None)
            }

        except Exception as e:
            return {
                "success": False,
                "output": output.getvalue(),
                "error": f"{str(e)}\n{error.getvalue()}",
                "result": None
            }

    @profile
    async def execute_with_memory_check(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute code with memory usage monitoring."""
        result = await self.execute_code(code, timeout)
        self.execution_history.append({
            "code": code,
            "result": result,
            "timestamp": asyncio.get_event_loop().time()
        })
        return result

    def explain_code(self, code: str) -> Dict[str, Any]:
        """Analyze and explain code for educational purposes."""
        try:
            tree = ast.parse(code)
            explanation = {
                "imports": [],
                "functions": [],
                "variables": [],
                "operations": [],
                "complexity": self._analyze_complexity(tree)
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    explanation["imports"].extend(n.name for n in node.names)
                elif isinstance(node, ast.FunctionDef):
                    explanation["functions"].append({
                        "name": node.name,
                        "args": [a.arg for a in node.args.args],
                        "docstring": ast.get_docstring(node)
                    })
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            explanation["variables"].append(target.id)

            return {
                "success": True,
                "explanation": explanation,
                "suggestions": self._generate_suggestions(explanation)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    def _analyze_complexity(self, tree: ast.AST) -> Dict[str, int]:
        """Analyze code complexity metrics."""
        complexity = {
            "cyclomatic": 0,
            "nesting_depth": 0
        }
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.FunctionDef)):
                complexity["cyclomatic"] += 1
        return complexity

    def _generate_suggestions(self, explanation: Dict) -> List[str]:
        """Generate improvement suggestions based on code analysis."""
        suggestions = []
        if len(explanation["functions"]) == 0:
            suggestions.append("Consider organizing code into functions for better reusability")
        if len(explanation["imports"]) > 10:
            suggestions.append("Consider organizing imports to reduce dependencies")
        return suggestions

    async def process_task(self, task: Task) -> Any:
        """Process incoming tasks based on their type."""
        task_type = task.task_type
        task_data = task.data

        if task_type == "execute_code":
            return await self.execute_with_memory_check(
                code=task_data["code"],
                timeout=task_data.get("timeout", 30)
            )
        elif task_type == "explain_code":
            return self.explain_code(task_data["code"])
        elif task_type == "get_execution_history":
            return {"history": self.execution_history}
        else:
            raise ValueError(f"Unsupported task type: {task_type}")