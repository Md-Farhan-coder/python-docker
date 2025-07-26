import subprocess
import tempfile
import os
import signal

def execute_code(code: str, timeout: int = 5) -> str:
    """
    Execute Python code in a subprocess with timeout.
    Returns the output or error message.
    """
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp:
        tmp.write(code.encode('utf-8'))
        tmp_path = tmp.name
    
    try:
        process = subprocess.Popen(
            ['python', tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.kill(process.pid, signal.SIGKILL)
            return "Error: Code execution timed out"
        
        if process.returncode != 0:
            return f"Error: {stderr}"
        
        return stdout
    finally:
        os.unlink(tmp_path)