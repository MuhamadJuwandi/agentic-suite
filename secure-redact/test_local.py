from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_redaction():
    print("Running Local Validation for SecureRedact API...")
    
    # Test Case 1: Standard PII (Email & Phone)
    text_sample = "Contact me at 08123456789 or john.doe@example.com."
    print(f"\n[Test 1] Input: {text_sample}")
    
    response = client.post("/api/redact", json={
        "text": text_sample,
        "anonymize": True,
        "mask_char": "*" 
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: SUCCESS ({response.status_code})")
        print(f"Redacted Text: {data['redacted_text']}")
        print(f"Entities Found: {len(data['entities_detected'])}")
        for ent in data['entities_detected']:
            print(f" - {ent['type']}: {ent['text']}")
    else:
        print(f"Status: FAILED ({response.status_code})")
        print(response.text)

    # Test Case 2: Health Check
    print("\n[Test 2] Health Check")
    health = client.get("/health")
    print(f"Response: {health.json()}")

if __name__ == "__main__":
    test_redaction()
