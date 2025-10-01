import base64
import os
from openai import OpenAI

IMAGE_FILE = "jazz-quintet.jpg"
PROMPT = "How many people are in this image?"
SERVER_URL = "http://localhost:8081/v1"

# Convert image to base64 representation
def image_to_base64_url(image_path):
    """Converts an image file to a base64 data URL."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"

def main():
    """
    Sends an image and prompt to a locally served RamaLama model.
    """
    if not os.path.exists(IMAGE_FILE):
        print(f"Error: Image file not found at '{IMAGE_FILE}'")
        return

    print(f"Querying local model served by RamaLama...")
    print(f"Prompt: {PROMPT}")

    try:
        # Point the OpenAI client to your local RamaLama server
        client = OpenAI(
            base_url=SERVER_URL,
            api_key="ramalama"
        )

        base64_url = image_to_base64_url(IMAGE_FILE)

        response = client.chat.completions.create(
            model="qwen2.5vl:3b", # The model being served
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": base64_url},
                        },
                    ],
                }
            ],
            max_tokens=100,
        )

        print("\nResponse from model:")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Is the 'ramalama serve' command running in another terminal?")

if __name__ == "__main__":
    main()
