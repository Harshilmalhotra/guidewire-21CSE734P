from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fnol():
    print("\n--- TEST 1: RAW FRAUD CLAIM ---")
    payload = {
        "policyId": "CLAIM-A",
        "policyholderId": "PERSON-X",
        "vehicleVin": "VEH-1",
        "description": "fraud and suspicious intent",
        "images": [],
        "claimAmount": 15000.0,
        "metadata": {}
    }
    r = client.post("/fnol", json=payload)
    print("Response:", r.json())
    assert r.status_code == 200
    assert r.json()["decision"] == "INVESTIGATE"

    print("\n--- TEST 2: CLEAN DISJOINT NODE ---")
    payload_clean = {
        "policyId": "CLAIM-B",
        "policyholderId": "PERSON-Y",
        "vehicleVin": "VEH-2",
        "description": "minor scratch",
        "images": [],
        "claimAmount": 200.0,
        "metadata": {}
    }
    r_c = client.post("/fnol", json=payload_clean)
    print("Response:", r_c.json())
    assert r_c.json()["decision"] == "APPROVE"

    print("\n--- TEST 3: ANOMALY - SHARED VIN & PROPAGATION ---")
    payload_prop = {
        "policyId": "CLAIM-C",
        "policyholderId": "PERSON-Y",  # Person Y is clean
        "vehicleVin": "VEH-1",         # But VEH-1 was flagged in CLAIM-A
        "description": "normal accident perfectly clean", 
        "images": [],
        "claimAmount": 500.0,
        "metadata": {}
    }
    r_p = client.post("/fnol", json=payload_prop)
    print("Response:", r_p.json())
    assert r_p.status_code == 200
    # Because VEH-1 was flagged in CLAIM-A, it should have a high graph risk
    assert r_p.json()["graphRisk"] > 0.4
    assert r_p.json()["decision"] == "INVESTIGATE"
    assert "Shared vehicle across 2 claimants" in r_p.json()["graphSignals"]
    assert "Direct connection to flagged node" in r_p.json()["graphSignals"]

if __name__ == "__main__":
    test_fnol()
