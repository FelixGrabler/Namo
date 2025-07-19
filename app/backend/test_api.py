"""
Simple API testing script
Run this after starting the server to test the endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_api():
    """Test the main API endpoints."""
    print("Testing Namo API...")

    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please start the server first.")
        return

    # Test user registration
    print("\n1. Testing user registration...")
    user_data = {"username": "testuser123", "password": "testpassword123"}

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 200:
        print(f"User created: {response.json()}")
    else:
        print(f"Error: {response.text}")

    # Test user login
    print("\n2. Testing user login...")
    login_data = {"username": "testuser123", "password": "testpassword123"}

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print(f"Login successful. Token: {token[:50]}...")

        headers = {"Authorization": f"Bearer {token}"}

        # Test get random name
        print("\n3. Testing get random name...")
        response = requests.get(f"{BASE_URL}/names/random", headers=headers)
        print(f"Random name: {response.status_code}")
        if response.status_code == 200:
            name_data = response.json()
            print(f"Name: {name_data}")

            # Test voting
            print("\n4. Testing voting...")
            vote_data = {"name_id": name_data["id"], "vote": True}  # Like
            response = requests.post(
                f"{BASE_URL}/votes/", json=vote_data, headers=headers
            )
            print(f"Vote: {response.status_code}")
            if response.status_code == 200:
                print(f"Vote created: {response.json()}")

                # Test get vote stats
                print("\n5. Testing vote statistics...")
                response = requests.get(
                    f"{BASE_URL}/votes/{name_data['id']}/stats", headers=headers
                )
                print(f"Vote stats: {response.status_code}")
                if response.status_code == 200:
                    print(f"Stats: {response.json()}")

        # Test get my votes
        print("\n6. Testing get my votes...")
        response = requests.get(f"{BASE_URL}/votes/my-votes", headers=headers)
        print(f"My votes: {response.status_code}")
        if response.status_code == 200:
            print(f"Votes: {response.json()}")

    else:
        print(f"Login failed: {response.text}")


if __name__ == "__main__":
    test_api()
