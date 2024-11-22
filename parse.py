import json
import cv2
import numpy as np
from PIL import Image, ImageEnhance

from bs4 import BeautifulSoup


def extract_HTML(text):
    # ```html
    # ```
    start_index = text.find('```html')
    end_index = text.rfind('</table>')
    if start_index != -1 and end_index != -1:
        s = text[start_index + 7:end_index + 8]
        s = s.strip()
        soup = BeautifulSoup(s, 'html.parser')
        cleaned_html = str(soup.table)
        cleaned_html = cleaned_html.replace("\n", "")
        return cleaned_html
    else:
        start_index = text.find('<table>')
        if start_index != -1 and end_index != -1:
            s = text[start_index:end_index + 8]
            s = s.strip()
            soup = BeautifulSoup(s, 'html.parser')
            cleaned_html = str(soup.table)
            cleaned_html = cleaned_html.replace("\n", "")
            return cleaned_html
        raise Exception("Parse error! Not find HTML in LLM response!")


def extract_json(text):
    s = ""
    start_index = text.find('{')
    end_index = text.rfind('}')
    if start_index != -1 and end_index != -1:
        s = text[start_index:end_index + 1]
        s = s.strip()
        res = json.loads(s)
        return res
    else:
        raise Exception("Parse error! Not find json in LLM response!")


def extract_list(text):
    s = ""
    start_index = text.find('[')
    end_index = text.rfind(']')
    if start_index != -1 and end_index != -1:
        s = text[start_index:end_index + 1]
        s = s.strip()
        res = json.loads(s)
        return res
    else:
        raise Exception("Parse error! Not find json in LLM response!")


def format_td(html):
    html = html.replace("\n", "")
    html = html.replace("<thead>", "").replace("</thead>", "")
    html = html.replace("<tbody>", "").replace("</tbody>", "")
    return html


def move_ae_to_front(s):
    if 'a' in s:
        s = 'a' + s.replace('a', '', 1)
    if 'e' in s:
        s = 'e' + s.replace('e', '', 1)

    return s
