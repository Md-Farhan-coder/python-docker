from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    language = data.get("language", "").lower()
    code = data.get("code", "")

    if language != "python":
        return jsonify({"output": "", "error": f"Language '{language}' not supported"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as temp:
        temp.write(code)
        temp_path = temp.name

    try:
        result = subprocess.run(
            ["python3", temp_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        error = result.stderr
    except subprocess.TimeoutExpired:
        output = ""
        error = "Execution timed out."
    except Exception as e:
        output = ""
        error = str(e)

    os.remove(temp_path)

    return jsonify({
        "output": output,
        "error": error if error else None
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
