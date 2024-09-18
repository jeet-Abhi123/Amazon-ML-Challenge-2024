import pandas as pd
from datasets import Dataset, Features, Image, Value
from huggingface_hub import HfApi
import os
import requests
from PIL import Image as PILImage
from io import BytesIO
from tqdm import tqdm
import time
import random

HF_TOKEN = "your_token_here"
username = "Sarvesh2003"
dataset_name = "mlchallenge-data_train_30k"

csv_file_path = "train_30k.csv"
df = pd.read_csv(csv_file_path)
df['entity_name'] = 'what is the value of '+ df['entity_name']+'?'
def download_image(url, filename, max_retries=1000):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                img = PILImage.open(BytesIO(response.content))
                img = img.convert('RGB')  # Convert to RGB to ensure consistency
                img.save(filename, format='JPEG')
                return filename
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 3))  # Random delay between retries
            else:
                print(f"Failed to download {url} after {max_retries} attempts")
    return None

os.makedirs("images", exist_ok=True)

image_paths = []
for index, row in tqdm(df.iterrows(), total=len(df), desc="Downloading images"):
    image_url = row['image_link']
    image_filename = f"images/image_{index}.jpg"
    downloaded_path = download_image(image_url, image_filename)
    image_paths.append(downloaded_path if downloaded_path else None)

df['image_path'] = image_paths

df = df.dropna(subset=['image_path'])

def load_image(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

hf_data = {
    'image': [load_image(path) for path in df['image_path']],
    'group_id': df['group_id'].tolist(),
    'entity_name': df['entity_name'].tolist(),
    'entity_value': df['entity_value'].tolist()
}

features = Features({
    'image': Image(),
    'group_id': Value('int64'),
    'entity_name': Value('string'),
    'entity_value': Value('string')
})

dataset = Dataset.from_dict(hf_data, features=features)

api = HfApi(token=HF_TOKEN)

print("Pushing dataset to Hugging Face...")
dataset.push_to_hub(f"{username}/{dataset_name}", token=HF_TOKEN)

readme_content = ""

api.upload_file(
    path_or_fileobj=readme_content.encode(),
    path_in_repo="README.md",
    repo_id=f"{username}/{dataset_name}",
    repo_type="dataset",
)

print(f"Dataset uploaded successfully to https://huggingface.co/datasets/{username}/{dataset_name}")