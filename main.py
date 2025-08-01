import os, json

from LLM import call_LLM
from LLM_key import llm_model
from parse import extract_HTML, format_td
from prompt import tsr_html_prompt, tsr_html_decomposition
from metric import TEDS

def save_response_to_file(output_path, image_name, response):
    html_response_path = os.path.join(output_path, os.path.splitext(image_name)[0]+".html")
    html_response = response
    
    with open(html_response_path, 'w+') as f:
        f.write(html_response)
    return  


def main(strategy : str, temp = 0):
    teds = TEDS(structure_only=False)
    teds_struct = TEDS(structure_only=True)

    image_name = "NL-HaNA_2.10.50_72_0036.jpg"
    image_path = "example/stamboeken/img/NL-HaNA_2.10.50_72_0036.jpg"

    with open(f"example/stamboeken/context.json", 'r', encoding='utf-8') as f:
        context_label = json.load(f)

    # label_html = item["html"]
    # difficulty = item["type"]

    if strategy == "chain_of_thought":
        llm_html = call_LLM(image_path, prompt=tsr_html_decomposition, model_name=llm_model, temperature=temp)
    else:
        llm_html = call_LLM(image_path, prompt=tsr_html_prompt, model_name=llm_model, temperature=temp)
    llm_html = extract_HTML(llm_html)

    llm_html = format_td(llm_html)
    image_name = os.path.basename(image_path)

    # TRUE HTML
    label_html = context_label[image_name]["html"]
    label_html = format_td(label_html)

    teds_score = teds.evaluate(label_html, llm_html)
    teds_struct_score = teds_struct.evaluate(label_html, llm_html)

    output_json = {
            "id": None,
            "image_id": image_name,
            "TEDS_score": teds_score,
            "TEDS_struct": teds_struct_score,
            "llm_prompt": llm_html,
            "label": label_html,
        }
    output_path = f"output/{llm_model.split('/')[-1]}/{strategy}"
    output_name = "/" + strategy + ".jsonl"

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(output_path + output_name, 'a', encoding='utf-8') as f:
        f.write(json.dumps(output_json) + "\n")

    save_response_to_file(output_path, image_name, llm_html)

if __name__ == "__main__":
    for i in range(10):
        main("chain_of_thought")