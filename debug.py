from openai import OpenAI
import base64
from mimetypes import guess_type

client = OpenAI(
    api_key='sk-V3CaY1MOnf1MNzumEb9bE5B288114964A94e2e3e7c9780Af',
    base_url="https://yeysai.com/v1/",
)

def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded_data}"

filepath = "D:\ComputerScience\CODES\MatPlotAgent-main\workspace\FRDOuW2XoAAz4ua.jpg"
prompt = "What’s in this image?"

# 本地图片支持
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": local_image_to_data_url(filepath)},
                },
            ],
        }
    ],
    max_tokens = 1000,
    temperature = 0.2
)
print(response.choices[0].message.content)