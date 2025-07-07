import yaml
from src import yaml_patcher

sample_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
      - name: main
        image: nginx
"""

def test_patch_should_return_yaml():
    patched = yaml_patcher.generate_patch(sample_yaml)
    parsed = list(yaml.safe_load_all(patched))
    
    # Find the Deployment document
    deployment_doc = next((doc for doc in parsed if doc.get("kind") == "Deployment"), None)
    assert deployment_doc is not None, "No Deployment found in patched YAML"

    container = deployment_doc["spec"]["template"]["spec"]["containers"][0]
    
    # Check that patching was applied
    assert "securityContext" in container
    assert "runAsNonRoot" in container["securityContext"]
    assert any(k in container for k in ["resources", "limits"]), "Resources block not found in container"


