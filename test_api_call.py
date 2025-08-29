import requests
import json
import subprocess

def copy_to_clipboard(text):
    """Copy text to clipboard using macOS pbcopy"""
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

def test_subscriptions_api():
    # Your API access key (replace with your actual key)
    api_key = "80d06c01ec7f96ba3fcf22493acdccd0e899d2f87767c80e1bc46acaa0887eec"
    
    # Set up headers with API key
    headers = {
        "Hydrus-Client-API-Access-Key": api_key
    }
    
    try:
        # Make GET request to the subscriptions endpoint
        # The endpoint is registered directly under manage_subscriptions/get_subscriptions
        response = requests.get(
            'http://127.0.0.1:45869/manage_subscriptions/get_subscriptions',
            headers=headers
        )
        
        # Print status code and raw response
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # If successful, format and copy JSON to clipboard
        if response.status_code == 200:
            try:
                # Parse JSON and format it nicely
                json_data = response.json()
                formatted_json = json.dumps(json_data, indent=2)
                
                # Copy to clipboard
                copy_to_clipboard(formatted_json)
                print("\n✅ Formatted JSON response copied to clipboard!")
                
            except json.JSONDecodeError:
                # If not JSON, copy raw text
                copy_to_clipboard(response.text)
                print("\n✅ Raw response copied to clipboard!")
                
        else:
            # Copy error response to clipboard too
            copy_to_clipboard(f"Status: {response.status_code}\nResponse: {response.text}")
            print("\n📋 Error response copied to clipboard!")
            
    except requests.exceptions.ConnectionError:
        error_msg = "Error: Could not connect to the Hydrus client. Make sure it's running and the API is enabled."
        print(error_msg)
        copy_to_clipboard(error_msg)
        print("📋 Error message copied to clipboard!")
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred: {str(e)}"
        print(error_msg)
        copy_to_clipboard(error_msg)
        print("📋 Error message copied to clipboard!")

if __name__ == '__main__':
    test_subscriptions_api()
