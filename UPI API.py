import jwt  # PyJWT library
import time

# Replace with your Setu sandbox credentials
CLIENT_ID = "your_id"
CLIENT_SECRET = "your_key"

def generate_jwt():
    # JWT Header
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }

    # JWT Payload (including 'aud' claim)
    payload = {
        "iss": CLIENT_ID,  # Issuer - your client ID
        "aud": "https://sandbox.setu.co",  # Audience - Setu API
        "iat": int(time.time()),  # Issued at
        "exp": int(time.time()) + 600  # Expiry - 10 minutes from now
    }

    # Generate JWT token using HS256 algorithm
    token = jwt.encode(payload, CLIENT_SECRET, algorithm="HS256", headers=headers)
    return token

# Test JWT generation
#print("Generated JWT:", generate_jwt())
import requests
import uuid

BASE_URL = "https://uat.setu.co/api/upi/collect"

def create_upi_collect_request(upi_id, amount, note):
    txn_id = str(uuid.uuid4())  # Unique transaction ID

    # Generate JWT token
    token = generate_jwt()

    # Set headers with the JWT token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Prepare request payload
    data = {
        "amount": {
            "currencyCode": "INR",
            "value": int(amount * 100)  # Convert INR to paise
        },
        "direction": "DEBIT",
        "merchantTransactionId": txn_id,
        "merchantOrderId": txn_id,
        "note": note,
        "payer": {
            "vpa": upi_id
        },
        "expiryInSeconds": 600
    }

    # Make the API request
    response = requests.post(BASE_URL, json=data, headers=headers)

    if response.status_code == 200:
        print("UPI Collect Request Initiated Successfully!")
        print("Response:", response.json())
    else:
        print("Failed to Initiate UPI Collect Request.")
        print("Error:", response.json())

# Test the function
create_upi_collect_request("test@upi", 10.00, "Payment for Order #1234")
