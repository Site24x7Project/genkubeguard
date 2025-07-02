import subprocess

def run_kube_linter(yaml_bytes):
    with open("temp.yaml", "wb") as f:
        f.write(yaml_bytes)

    result = subprocess.run(["kube-linter", "lint", "temp.yaml"], capture_output=True, text=True)
    if result.returncode != 0:
        return result.stdout.strip().split('\n')
    return []
