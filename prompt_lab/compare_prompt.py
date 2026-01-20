import model.model as m
import prompt_lab.analysis_prompt as ap
import prompt_lab.data.load_data as data


def compare_prompt_with_text(prompt_name, other_prompt_names, data_path):
    responses = []
    prompts = ap.get_prompt(prompt_name, compare=True, other_prompt_names=other_prompt_names)
    text = data.load_text_data(data_path)
    for prompt in prompts:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]

        responses.append(m.model(messages))
    #  response in responses:
    #    print(response)
    return responses


if __name__ == '__main__':
    compare_prompt_with_text("summary", ["other_prompt"], "./data/story.txt")
