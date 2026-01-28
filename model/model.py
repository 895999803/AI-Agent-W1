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

