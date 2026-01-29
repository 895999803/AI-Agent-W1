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

