from pydantic import BaseModel, Field
from typing import Optional, List, Union
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

class ChatInputType(BaseModel):
    input: List[Union[HumanMessage, AIMessage, SystemMessage]]

class CodeExecutionOutput(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    artifacts: Optional[List[str]] = None

    class Config:
        arbitrary_types_allowed = True

class GenericOutputType(BaseModel):
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    artifacts: Optional[List[str]] = None
    result: Optional[str] = None  # For plain text or other results

    class Config:
        arbitrary_types_allowed = True
