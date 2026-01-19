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
  print(completion.choices[0].message.content)