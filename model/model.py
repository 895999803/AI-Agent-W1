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