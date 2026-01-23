from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)


def model(messages):
    completion = client.chat.completions.create(
        model="allenai/molmo-2-8b:free",
        messages=messages
    )
    return completion.choices[0].message.content

