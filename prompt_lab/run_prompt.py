import data.load_data as data
import model.model as m
import analysis_prompt as ap


def run_prompt_with_text(prompt_name, data_path):

    prompt = ap.get_prompt(prompt_name)[0]
    text = data.load_text_data(data_path)
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

    response = m.model(messages)
    # print(response)
    return response


if __name__ == '__main__':

    run_prompt_with_text("summary", "./data/story.txt")



