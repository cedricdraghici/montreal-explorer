import requests
import time

SERVER_URL = "http://127.0.0.1:5000/gpt"

def chat_client():
    print("Travel Assistant Chat Client")
    print("Type 'exit' to quit\n")
    time.sleep(0.5)  # Gives time to read the header
    
    while True:
        try:
            message = input("You: ")
            if message.lower() == 'exit':
                print("Goodbye!")
                break
            if not message.strip():
                print("Please enter a valid message")
                continue

            # Send the message to the server
            response = requests.post(
                SERVER_URL,
                json={"user_message": message}
            )

            if response.status_code == 200:
                print("\nAssistant:", response.text)
            else:
                print(f"\nError: {response.status_code} - {response.text}")

            print()  # Add empty line between exchanges

        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to server. Make sure it's running!")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    chat_client()
