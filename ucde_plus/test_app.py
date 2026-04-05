from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fnol():
    print("\n--- TEST 1: RAW FRAUD CLAIM (High amounts, Suspicious Text) ---")
    payload = {
        "policyId": "CLAIM-A",
        "policyholderId": "PERSON-X",
        "vehicleVin": "VEH-1",
        "description": "fraud and suspicious intent entirely staged",
        "images": [],
        "claimAmount": 19000.0,
        "claimHistoryCount": 8,
        "timeSinceLastClaim": 10.0,
        "metadata": {}
    }
    r = client.post("/v1/fnol?mode=debug", json=payload)
    print("Response:", r.json())
    assert r.status_code == 200

    print("\n--- TEST 2: EXTREMELY CLEAN claim ---")
    payload_clean = {
        "policyId": "CLAIM-B",
        "policyholderId": "PERSON-Y",
        "vehicleVin": "VEH-2",
        "description": "minor scratch on bumper nothing serious",
        "images": [],
        "claimAmount": 200.0,
        "claimHistoryCount": 0,
        "timeSinceLastClaim": 1000.0,
        "metadata": {}
    }
    r_c = client.post("/v1/fnol?mode=debug", json=payload_clean)
    print("Response:", r_c.json())

    print("\n--- TEST 3: GRAPH CONTAGION ABUSING NEW VARIABLES ---")
    payload_prop = {
        "policyId": "CLAIM-C",
        "policyholderId": "PERSON-Y",  
        "vehicleVin": "VEH-1",         # Contagion Link
        "description": "normal accident perfectly clean", 
        "images": [],
        "claimAmount": 18000.0,
        "claimHistoryCount": 2,
        "timeSinceLastClaim": 30.0,
        "metadata": {}
    }
    r_p = client.post("/v1/fnol?mode=debug", json=payload_prop)
    print("Response:", r_p.json())
    print("\n--- TEST 4: BATCH LEARNING DATA FEEDBACK PIPELINE ---")
    trace_id = r_p.json()["trace_id"]
    feedback_payload = {
        "trace_id": trace_id,
        "human_action": "INVESTIGATE",
        "verified_fraud": True,
        "confidence": "HIGH",
        "comment": "Adjuster independently validated contagion bounds matching LLM outputs logically"
    }
    
    headers = {"Authorization": "Bearer adjuster-api-token"}
    r_f = client.post("/v1/feedback", json=feedback_payload, headers=headers)
    print("Feedback Submission Response:", r_f.json())
    assert r_f.status_code == 200
    
    # Test Idempotency natively handling duplicated logic bounds gracefully mapping poison
    r_f_dup = client.post("/v1/feedback", json=feedback_payload, headers=headers)
    assert r_f_dup.status_code == 409
    print("Idempotency Constraint Confirmed:", r_f_dup.json())
    
    print("\n[✔] Test Suite Passed. DB Persistence logged globally.")

if __name__ == "__main__":
    test_fnol()
