#!/usr/bin/env python3
"""
Daily request script that:
1. Retrieves MIKEY_SECRET from environment variables
2. Sends GET request to meltingscales.github.io with Bearer token
3. Saves response to text file and prints it
"""

import os
import requests
import sys
from datetime import datetime

def main():
    # 1. Retrieve MIKEY_SECRET from environment
    mikey_secret = os.getenv('MIKEY_SECRET')
    
    if not mikey_secret:
        print("Error: MIKEY_SECRET environment variable not set")
        sys.exit(1)
    
    print(f"Retrieved MIKEY_SECRET: {mikey_secret[:8]}...")  # Only show first 8 chars for security
    
    # 2. Send GET request with Bearer token
    url = "https://meltingscales.github.io"
    headers = {
        'Authorization': f'Bearer {mikey_secret}',
        'User-Agent': 'GitHub-Actions-Daily-Request/1.0'
    }
    
    try:
        print(f"Sending GET request to: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Get response content
        response_text = response.text
        response_status = response.status_code
        
        print(f"Request successful! Status code: {response_status}")
        print(f"Response length: {len(response_text)} characters")
        
        # 3. Save response to text file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"response.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Request URL: {url}\n")
            f.write(f"Request Time: {datetime.now().isoformat()}\n")
            f.write(f"Status Code: {response_status}\n")
            f.write(f"Response Headers:\n")
            for key, value in response.headers.items():
                f.write(f"  {key}: {value}\n")
            f.write(f"\nResponse Body:\n")
            f.write(response_text)
        
        print(f"Response saved to: {filename}")
        
        # Print response (first 500 characters to avoid overwhelming output)
        print("\n" + "="*50)
        print("RESPONSE PREVIEW (first 500 characters):")
        print("="*50)
        print(response_text[:500])
        if len(response_text) > 500:
            print(f"\n... (truncated, total length: {len(response_text)} characters)")
        print("="*50)
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 