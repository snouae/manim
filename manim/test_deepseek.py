import os
from dotenv import load_dotenv
import litellm

# Load environment variables
load_dotenv()

# Enable debug mode
litellm._turn_on_debug()

# Get API key from environment
api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY environment variable not set")

print(f"Using Deepseek API key: {api_key[:5]}...")

# Model names to try
model_names = [
    "deepseek/deepseek-reasoner",
]

# Try each model
for model_name in model_names:
    print(f"\nTrying model: {model_name}")
    try:
        response = litellm.completion(
            model=model_name, 
            messages=[
                {"role": "user", "content": "Tell me about the Pythagorean theorem"}
            ],
            api_key=api_key,
            max_tokens=100
        )
        print("Response:", response.choices[0].message.content)
        print("Success with model:", model_name)
        break
    except Exception as e:
        print(f"Error with model {model_name}: {e}")

# List available models in litellm
try:
    print("\nAvailable litellm models:")
    completion_models = litellm.utils.get_litellm_model_info()
    for name in completion_models:
        print(f"- {name}")
except Exception as e:
    print(f"Error listing models: {e}") 