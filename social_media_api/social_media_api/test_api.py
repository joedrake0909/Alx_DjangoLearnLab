"""
Test script to verify the Social Media API endpoints.
Run this script after starting the Django development server.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/accounts"

def test_registration():
    """Test user registration endpoint."""
    print("\n" + "="*50)
    print("Testing User Registration")
    print("="*50)
    
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!",
        "bio": "This is a test user account"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✓ Registration successful!")
            return response.json()['token']
        else:
            print("✗ Registration failed!")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_login():
    """Test user login endpoint."""
    print("\n" + "="*50)
    print("Testing User Login")
    print("="*50)
    
    url = f"{BASE_URL}/login/"
    data = {
        "username": "testuser123",
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Login successful!")
            return response.json()['token']
        else:
            print("✗ Login failed!")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_get_profile(token):
    """Test get user profile endpoint."""
    print("\n" + "="*50)
    print("Testing Get User Profile")
    print("="*50)
    
    url = f"{BASE_URL}/profile/"
    headers = {
        "Authorization": f"Token {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Profile retrieved successfully!")
        else:
            print("✗ Failed to retrieve profile!")
    except Exception as e:
        print(f"Error: {e}")


def test_update_profile(token):
    """Test update user profile endpoint."""
    print("\n" + "="*50)
    print("Testing Update User Profile")
    print("="*50)
    
    url = f"{BASE_URL}/profile/"
    headers = {
        "Authorization": f"Token {token}"
    }
    data = {
        "bio": "Updated bio - This user loves coding!"
    }
    
    try:
        response = requests.patch(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✓ Profile updated successfully!")
        else:
            print("✗ Failed to update profile!")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to run all tests."""
    print("\n" + "#"*50)
    print("# Social Media API - Endpoint Testing")
    print("#"*50)
    print("\nMake sure the Django server is running on http://127.0.0.1:8000")
    print("Press Ctrl+C to cancel or Enter to continue...")
    input()
    
    # Test registration
    token = test_registration()
    
    if token:
        # Test login
        login_token = test_login()
        
        # Test get profile
        if login_token:
            test_get_profile(login_token)
            
            # Test update profile
            test_update_profile(login_token)
    
    print("\n" + "="*50)
    print("Testing completed!")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()
