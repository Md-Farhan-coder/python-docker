x
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from executor import execute_code

app = FastAPI()

class CodeRequest(BaseModel):
    language: str
    code: str
    timeout: int = 5  # default timeout in seconds

@app.post("/execute")
async def execute_code_endpoint(request: CodeRequest):
    if request.language.lower() != "python":
        raise HTTPException(
            status_code=400, 
            detail="Only Python is supported at this time"
        )
    
    try:
        output = execute_code(request.code, timeout=request.timeout)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))