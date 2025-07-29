from groq import Groq
import base64
import io

from LLM_key import groq_key, llm_model
from prompt import tsr_html_prompt

image_path = "example/stamboeken/NL-HaNA_2.10.50_45_0355.jpg"
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def call_LLM(image_path, prompt=tsr_html_prompt, model_name=llm_model, temperature=0):
    client = Groq(api_key=groq_key)
    base64_image = encode_image(image_path)
    content = [{"type": "text", "text": prompt}]

    content.append({
       "type": "image_url",
       "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}",
        }
    })

    response = client.chat.completions.create(
       model=model_name,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        temperature=temperature,
    )

    result = response.choices[0].message.content
    print(result)
    return result


if __name__ == "__main__":
   call_LLM(image_path)