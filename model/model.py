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