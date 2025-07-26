import os

def show_ascii_art():
    art_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'art')
    if os.path.exists(art_path):
        with open(art_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("[ascii art missing]")
