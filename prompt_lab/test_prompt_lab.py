import sys
import run_prompt as rp
import compare_prompt as cp


if __name__ == '__main__':

    if len(sys.argv) == 3:
        prompt_name = sys.argv[1]
        data_path = sys.argv[2]
        response = rp.run_prompt_with_text(prompt_name, data_path)
        print(response)

    elif len(sys.argv) > 3:
        prompt_name = sys.argv[1]
        data_path = sys.argv[-1]
        other_prompts = []
        for i in range(2, len(sys.argv)-1):
            other_prompts.append(sys.argv[i])
        responses = cp.compare_prompt_with_text(prompt_name, other_prompts, data_path)
        for response in responses:
            print(response)
    else:
        print("Usage: python test_prompty_lab.py prompt_name, [other_prompt_names], data_path")
        sys.exit(1)

