import requests
import time

SERVER_URL = "http://127.0.0.1:5000/gpt"
SESSION_ID = None

def chat_client():
    global SESSION_ID
    print("Travel Assistant Chat Client")
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            message = input("You: ")
            if message.lower() == 'exit':
                print("Goodbye!")
                break
            if not message.strip():
                print("Please enter a valid message")
                continue

            # Prepare request payload
            payload = {"user_message": message}
            if SESSION_ID:
                payload["session_id"] = SESSION_ID

            # Send request
            response = requests.post(SERVER_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                SESSION_ID = data['session_id']  # Update session ID
                print("\nAssistant:", data['response'])
            else:
                print(f"\nError: {response.status_code} - {response.text}")

            print()

        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to server. Make sure it's running!")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    chat_client()
