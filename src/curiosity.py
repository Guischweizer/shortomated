import google.generativeai as genai

def generate_curiosity(model_name):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Tell me a short and interesting fun fact that could be used to create a 15-second video in a short sentence that lasts 15 seconds.")
    return response.text.strip()

def generate_image_query(model_name):
    def inner(curiosity):
        model = genai.GenerativeModel(model_name)
        prompt = f"Based on this fun fact, give me a one-word image suggestion that could illustrate this fun fact: {curiosity}"
        response = model.generate_content(prompt)
        print(f"✅ Image suggestion: {response.text.strip()}")
        return response.text.strip()
    return inner
