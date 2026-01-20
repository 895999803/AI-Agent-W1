
def load_text_data(data_path):
    with open(data_path, 'r', encoding="utf-8") as file:
        content = file.read()
    return content
