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

