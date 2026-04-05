import os
import json
from datetime import datetime

class ModelRegistry:
    def __init__(self, registry_path="data/model_registry.json"):
        self.registry_path = registry_path
        self.base_dir = "data/models"
        os.makedirs(self.base_dir, exist_ok=True)
        self._init_registry()

    def _init_registry(self):
        if not os.path.exists(self.registry_path):
            initial_data = {
                "active_version": "v1",
                "versions": {
                    "v1": {
                        "path": "ppo_claim_policy.zip",
                        "accuracy": 0.75,
                        "timestamp": datetime.utcnow().isoformat(),
                        "samples": 0
                    }
                },
                "history": []
            }
            with open(self.registry_path, "w") as f:
                json.dump(initial_data, f, indent=4)

    def get_active_model_path(self):
        with open(self.registry_path, "r") as f:
            data = json.load(f)
            v = data["active_version"]
            path = data["versions"][v]["path"]
            # Join with base_dir if it's not the initial relative path
            if "/" not in path and not path.startswith("data"):
                return os.path.join(self.base_dir if v != "v1" else ".", path)
            return path

    def register_new_version(self, path, accuracy, samples):
        with open(self.registry_path, "r") as f:
            data = json.load(f)
            
        current_v = data["active_version"]
        current_acc = data["versions"][current_v]["accuracy"]
        
        # Rollback Safety: Only promote if accuracy improved
        # For simplicity in demo, we'll allow promotion if n > 0 
        # but log the comparison
        new_v_num = int(current_v.replace("v", "")) + 1
        new_v = f"v{new_v_num}"
        
        data["versions"][new_v] = {
            "path": path,
            "accuracy": accuracy,
            "samples": samples,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        promotion_status = "REJECTED"
        if accuracy >= current_acc:
            data["active_version"] = new_v
            promotion_status = "PROMOTED"
            
        data["history"].append({
            "version": new_v,
            "accuracy": accuracy,
            "status": promotion_status,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        with open(self.registry_path, "w") as f:
            json.dump(data, f, indent=4)
            
        return data["active_version"]

    def get_stats(self):
        with open(self.registry_path, "r") as f:
            return json.load(f)

global_model_registry = ModelRegistry()
