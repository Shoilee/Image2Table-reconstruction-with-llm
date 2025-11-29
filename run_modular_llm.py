import re
import csv
import os
from multi_turn_conversation import call_LLM
from LLM_key import llm_model


def run_llm_extraction(image_path, temperature=0):
    return call_LLM(image_path, model_name=llm_model, temperature=temperature)

def extract_detected_cells(llm_response):
    block = re.search(r"coordinates.*?```plaintext(.*?)```", llm_response, re.S | re.I)
    if not block:
        return []
    return [line.strip() for line in block.group(1).splitlines() if line.strip()]

def extract_logical_sequence(llm_response):
    block = re.search(r"logical sequence.*?```plaintext(.*?)```", llm_response, re.S | re.I)
    if not block:
        return []
    return [line.strip() for line in block.group(1).splitlines() if line.strip()]


def save_coordinates(lines, output_path):
    with open(output_path, "w+", newline="") as f:
        writer = csv.writer(f)
        for line in lines:
            parts = line.split("#")
            polygon = parts[0].strip()
            cell_id = "#" + parts[1].strip() if len(parts) > 1 else ""
            writer.writerow([polygon, cell_id])

def save_logical_sequence(lines, output_path):
    with open(output_path, "w+", newline="") as f:
        writer = csv.writer(f)
        for line in lines:
            if line.startswith("</"): continue
            parts = line.split("#")
            sequence = parts[0].strip()
            sequence= sequence.split(",")
            sequence = [item.strip().strip('"') for item in sequence if item.strip()]
            writer.writerow(sequence)

from parse import extract_HTML, format_td
from bs4 import BeautifulSoup

def extract_and_save_html(llm_response, save_path):
    html = extract_HTML(llm_response)
    html = html.replace("<table>", "<table border='1'>")
    soup = BeautifulSoup(html, 'html.parser')
    with open(save_path, "w+", encoding="utf-8") as f:
        f.write(soup.prettify())
    return html

def run(DATA_DIR):
    for file in os.listdir(DATA_DIR): 
        if not file.endswith(".jpg"): 
            continue
        image_path =  os.path.join(DATA_DIR, file)
        img_name = os.path.basename(image_path)

        # 1. Run LLM
        llm_response = run_llm_extraction(image_path)

        # 2. Coordinates + logical mapping
        center_path = f"../data/tables/cells/center/{img_name}.txt"
        logi_path   = f"../data/tables/cells/logi/{img_name}.txt"

        save_coordinates(extract_detected_cells(llm_response), center_path)
        save_logical_sequence(extract_logical_sequence(llm_response), logi_path)

        # 3. HTML
        html_path = f"../data/tables/html/{img_name}.html"
        html = extract_and_save_html(llm_response, html_path)

if __name__ == "__main__":
    DATA_DIR = "../data/images/"
    run(DATA_DIR)