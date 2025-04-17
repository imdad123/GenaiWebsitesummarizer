import requests

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": "What is quantum computing?",
    "stream": False
})

if response.status_code == 200:
    # Print the entire response to understand the structure
    print(response.json()["response"])  # Check if 'response' key is there
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print raw error message
