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