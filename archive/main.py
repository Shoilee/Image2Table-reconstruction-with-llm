import json
import os
import time

import fire
from tqdm import tqdm

from LLM import call_LLM
from calculate_sim import get_similarity_imagePathList
from dataSet import DataSet
from metric import TEDS
from parse import extract_json, move_ae_to_front, extract_HTML, format_td
from prompt import tsr_getToolsChain, tsr_html_prompt, few_shot_tsr_html, html_repair, image_reflection
from tools import Tools


def repair_html(html):
    prompt_str = html_repair.replace("{error_html}", html)
    after_html = call_LLM(prompt_str, "gpt-4o")
    after_html = extract_HTML(after_html)
    return after_html


def process_reflection(before, after):
    tools = Tools()
    before_base64 = tools.encode_image(before)
    after_base64 = tools.encode_image(after)
    prompt = [
        {
            "type": "text",
            "text": image_reflection
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{before_base64}"
            }
        },
        {
            "type": "text",
            "text": "\nBelow is the second image\n"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{after_base64}"
            }
        },
        {
            "type": "text",
            "text": "\n## Result\n```json"
        }
    ]
    response = call_LLM(prompt, "gpt-4o")
    return extract_json(response)


def main(model_name="gpt-4o", dataset_name="scitsr", desc="NGTR", data_path="D:/dataset", sim_n=1, tool_num=3,
         path_n=3,start_id = 0, end_id = 100):
    dataset = DataSet(dataset_name, data_path)
    tools = Tools()
    teds = TEDS(structure_only=False)
    teds_struct = TEDS(structure_only=True)
    data = dataset.getData(start_id, end_id)

    with open(f"example/{dataset_name}/context.json", 'r', encoding='utf-8') as f:
        context_label = json.load(f)

    for index, item in enumerate(tqdm(data)):
        index = index + start_id
        image_name = item["image_id"]
        image_path = item["image_path"]
        label_html = item["html"]
        difficulty = item["type"]
        # Similarity search
        sim_image_pathList = get_similarity_imagePathList(dataset_name, image_path, sim_n)
        # Multiple toolchain generation
        tool_chainList = []
        for sim_image in sim_image_pathList:
            base64_image = tools.encode_image(sim_image)
            prompt_str = tsr_getToolsChain.replace("{path_n}", str(path_n)).replace("{tool_num}", str(tool_num))
            prompt = [
                {
                    "type": "text",
                    "text": prompt_str
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
            llm_json = None
            max_try = 5
            while llm_json is None:
                try:
                    llm_response = call_LLM(prompt, model_name, temperature=0.8)
                    llm_json = extract_json(llm_response)
                except:
                    llm_json = None
                    time.sleep(5)
                    max_try -= 1
                    if max_try > 0:
                        continue
                    else:
                        llm_json = {
                            "path": ""
                        }
                        break
            for chain in llm_json:
                if chain != "chain_of_thought":
                    tool_chainList.append(llm_json[chain])
        tool_chainList.append("")
        unique_tool_chainList = list(set([item.lower() for item in tool_chainList]))

        chain_score = {}
        # Toolchain handling
        for sim_image in sim_image_pathList:
            for chain in unique_tool_chainList:
                chain = move_ae_to_front(chain)
                now_path = sim_image
                for tool in chain:
                    if tool in tools.toolBox:
                        now_path = tools.toolBox[tool](now_path, index)
                    else:
                        print(f"Tool {tool} not found!")
                base64_image = tools.encode_image(now_path)
                get_html_prompt = [
                    {
                        "type": "text",
                        "text": tsr_html_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
                max_try = 5
                llm_sim_html = None
                while llm_sim_html is None:
                    try:
                        llm_sim_html = call_LLM(get_html_prompt, model_name)
                        llm_sim_html = extract_HTML(llm_sim_html)
                    except:
                        llm_sim_html = None
                        time.sleep(5)
                        max_try -= 1
                        if max_try > 0:
                            continue
                        else:
                            llm_sim_html = ""
                            break

                llm_sim_html = format_td(llm_sim_html)
                sim_image_name = os.path.basename(sim_image)
                label_sim_html = context_label[sim_image_name]["html"]
                label_sim_html = format_td(label_sim_html)

                max_try = 3
                sim_teds = None
                while sim_teds is None:
                    try:
                        sim_teds = teds.evaluate(label_sim_html, llm_sim_html)
                        sim_teds_struct = teds_struct.evaluate(label_sim_html, llm_sim_html)
                    except:
                        llm_sim_html = repair_html(llm_sim_html)
                        max_try -= 1
                        if max_try > 0:
                            continue
                        else:
                            sim_teds = 0
                            sim_teds_struct = 0
                            break

                if chain not in chain_score:
                    chain_score[chain] = sim_teds + sim_teds_struct
                else:
                    chain_score[chain] += sim_teds + sim_teds_struct

        highest_chain = max(chain_score, key=chain_score.get)
        highest_chain = move_ae_to_front(highest_chain)
        now_path = image_path
        real_chain = ""

        for tool in highest_chain:
            if tool in tools.toolBox:
                now_path_cache = tools.toolBox[tool](now_path, index + 100000)
                max_try = 3
                llm_reflection_response = None
                while llm_reflection_response is None:
                    try:
                        llm_reflection_response = process_reflection(now_path, now_path_cache)
                    except:
                        max_try -= 1
                        if max_try > 0:
                            continue
                        else:
                            llm_reflection_response = {"choice": 1}
                            break
                if str(llm_reflection_response["choice"]) == "2":
                    now_path = tools.toolBox[tool](now_path, index)
                    real_chain += tool
            else:
                print(f"Tool {tool} not found!")
        base64_image = tools.encode_image(now_path)

        now_path = sim_image_pathList[0]
        for tool in real_chain:
            if tool in tools.toolBox:
                now_path = tools.toolBox[tool](now_path, index)
            else:
                print(f"Tool {tool} not found!")
        base64_context_image = tools.encode_image(now_path)
        context_image_name = os.path.basename(sim_image_pathList[0])
        context_image_label = context_label[context_image_name]["html"]
        context_image_label = format_td(context_image_label)

        prompt = [
            {
                "type": "text",
                "text": few_shot_tsr_html
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_context_image}"
                }
            },
            {
                "type": "text",
                "text": "```html\n" + context_image_label + "\n```  \n\n\n## task\n"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        llm_html = None
        max_try = 5
        while llm_html is None:
            try:
                llm_html = call_LLM(prompt, model_name)
                llm_html = extract_HTML(llm_html)
            except:
                llm_html = None
                time.sleep(5)
                max_try -= 1
                if max_try > 0:
                    continue
                else:
                    llm_html = ""
                    break

        llm_html = format_td(llm_html)
        label_html = format_td(label_html)

        max_try = 3
        teds_score = None
        teds_struct_score = None
        while teds_score is None:
            try:
                teds_score = teds.evaluate(label_html, llm_html)
                teds_struct_score = teds_struct.evaluate(label_html, llm_html)
            except:
                llm_html = repair_html(llm_html)
                max_try -= 1
                if max_try > 0:
                    continue
                else:
                    teds_score = 0
                    teds_struct_score = 0
                    break
        output_json = {
            "id": index,
            "image_id": image_name,
            "TEDS_score": teds_score,
            "TEDS_struct": teds_struct_score,
            "llm_prompt": llm_html,
            "label": label_html,
            "chain": highest_chain,
            "type": difficulty
        }
        output_path = f"output/{dataset_name}/{model_name}"
        output_name = "/" + desc + ".jsonl"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        with open(output_path + output_name, 'a', encoding='utf-8') as f:
            f.write(json.dumps(output_json) + "\n")


if __name__ == '__main__':
    fire.Fire(main)
