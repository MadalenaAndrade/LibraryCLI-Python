import json #to load localization

def load_localization():
    with open(f"MyLibraryCLI_default.json", "r", encoding="utf-8") as default_language: 
            return json.load(default_language)

def set_localization(language):
    try:
        with open(f"MyLibraryCLI_{language}.json", "r", encoding="utf-8") as original_file:
            content = json.load(original_file)
        
        with open(f"MyLibraryCLI_default.json", "w", encoding="utf-8") as new_file:
            json.dump(content, new_file, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        raise ValueError(f"Localization file for language {language} not found.")
    

