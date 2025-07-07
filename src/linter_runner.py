import subprocess
import uuid
import os

def run_kube_linter(yaml_bytes: bytes):
    temp_file = f"temp-{uuid.uuid4().hex}.yaml"
    with open(temp_file, "wb") as f:
        f.write(yaml_bytes)

    try:
        kube_linter_path = os.path.abspath(os.path.join("tools", "kube-linter.exe"))

        result = subprocess.run(
            [kube_linter_path, "lint", temp_file],
            capture_output=True,
            text=True,
            check=False
        )

        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        issues = []
        for line in lines:
            if line.lower().startswith("kubelinter"):
                continue
            if ":" not in line:
                continue
            issues.append(line)

        return issues if issues else [" No lint issues found."]

    except Exception as e:
        return [f"Error running kube-linter: {str(e)}"]

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
