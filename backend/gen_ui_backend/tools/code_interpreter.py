import os
import json
from langchain.tools import E2BDataAnalysisTool
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, List



class CodeInterpreterToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")


class CodeExecutionResult(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    artifacts: Optional[List[str]] = None

def save_artifact(artifact):
    print("New chart generated:", artifact.name)
    file = artifact.download()
    
    # Ensure the charts directory exists
    charts_dir = "./charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # Extract the file name from the artifact name
    artifact_filename = os.path.basename(artifact.name)
    artifact_path = os.path.join(charts_dir, artifact_filename)
    
    with open(artifact_path, "wb") as f:
        f.write(file)
    
    return artifact_filename  # Return only the filename


# Initialize the E2B Data Analysis Tool with environment variables and callbacks
e2b_data_analysis_tool = E2BDataAnalysisTool(
    env_vars={"MY_SECRET": "secret_value"},  # Example of passing environment variables
    on_stdout=lambda stdout: print("stdout:", stdout),
    on_stderr=lambda stderr: print("stderr:", stderr),
    on_artifact=save_artifact,
)


@tool("code-interpreter", args_schema=CodeInterpreterToolInput, return_direct=True)
def code_interpreter_tool(code: str) -> CodeExecutionResult:
    """Executes the provided Python code in a sandbox environment using E2B Data Analysis Tool."""
    
    # Execute the code using the E2B data analysis tool and capture the result
    result = e2b_data_analysis_tool.invoke({"python_code": code})
    
    # Ensure result is a dictionary
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            return CodeExecutionResult(stdout=result, stderr="Failed to parse output as JSON.")

    # Handle any generated artifacts (e.g., plots)
    artifacts = []
    if "plot" in result:
        plot = result["plot"]
        artifact_filename = save_artifact(plot)
        artifacts.append(artifact_filename)  # Append only the filename
    
    return CodeExecutionResult(
        stdout=result.get('stdout'),
        stderr=result.get('stderr'),
        artifacts=artifacts
    )
