from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    print("Health check OK:", response.json())

def test_fnol():
    print("\n--- TEST 1: SUSPICIOUS CLAIM ---")
    payload = {
        "policyId": "POL-12345",
        "policyholderId": "USER-A",
        "vehicleVin": "VIN-123",
        "description": "Rear-ended by another driver. The word FRAUD might exist.",
        "images": ["url1"],
        "claimAmount": 15000.0,
        "metadata": {}
    }
    response = client.post("/fnol", json=payload)
    print("Response:", response.json())
    assert response.status_code == 200
    assert response.json()["decision"] == "INVESTIGATE"

    print("\n--- TEST 2: CLEAN CLAIM ---")
    payload2 = {
        "policyId": "POL-67890",
        "policyholderId": "USER-B",
        "vehicleVin": "VIN-456",
        "description": "Scratched bumper in parking lot",
        "images": ["url2"],
        "claimAmount": 800.0,
        "metadata": {}
    }
    response2 = client.post("/fnol", json=payload2)
    print("Response:", response2.json())
    assert response2.status_code == 200
    assert response2.json()["decision"] == "APPROVE"

    print("\n--- TEST 3: GRAPH ANOMALY (SAME VIN) ---")
    payload3 = {
        "policyId": "POL-99999",
        "policyholderId": "USER-C",
        "vehicleVin": "VIN-123",  # Shares VIN with POL-12345
        "description": "Just a small dent.",
        "images": ["url3"],
        "claimAmount": 500.0,
        "metadata": {}
    }
    response3 = client.post("/fnol", json=payload3)
    print("Response:", response3.json())
    assert response3.status_code == 200
    assert response3.json()["decision"] == "INVESTIGATE"
    assert "RULE_003_GRAPH_ANOMALY" in response3.json()["decisionTrace"][0]

if __name__ == "__main__":
    test_health()
    test_fnol()
