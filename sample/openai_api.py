import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Cześć!",
    temperature=0.5,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

print(response["choices"][0]["text"])
