import os
import requests
from .curiosity import generate_image_query

def download_image(model_name, curiosity):
    unsplash_access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not unsplash_access_key:
        raise Exception("UNSPLASH_ACCESS_KEY not set in environment variables.")
    
    query = generate_image_query(model_name)(curiosity)
    
    search_url = "https://api.unsplash.com/search/photos"
    num_images = 3
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": num_images
    }
    headers = {
        "Authorization": f"Client-ID {unsplash_access_key}"
    }

    response = requests.get(search_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            image_paths = []
            for idx, result in enumerate(data["results"][:num_images]):
                image_url = result["urls"]["regular"]
                img_path = f"content/image_{idx+1}.jpg"
                img_response = requests.get(image_url)
                if img_response.status_code == 200 and img_response.headers.get('Content-Type', '').startswith('image/'):
                    with open(img_path, "wb") as f:
                        f.write(img_response.content)
                    image_paths.append(img_path)
                else:
                    raise Exception(f"Failed to download image from Unsplash. Status: {img_response.status_code}, Content-Type: {img_response.headers.get('Content-Type')}")
            return image_paths
        else:
            raise Exception("No images found for the given query on Unsplash.")
    else:
        raise Exception(f"Failed to search Unsplash API. Status: {response.status_code}, Response: {response.text}")
