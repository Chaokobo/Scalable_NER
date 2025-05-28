import json
from pathlib import Path

def extract_named_entities_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    named_entities = {}

    for entity, label in data:
        if label not in named_entities:
            named_entities[label] = []
        named_entities[label].append(entity)

    return named_entities

def merge_named_entities(all_entities, new_entities):
    for label, entities in new_entities.items():
        if label not in all_entities:
            all_entities[label] = []
        all_entities[label].extend(entities)

def extract_from_all_files(root_folder):
    all_named_entities = {}
    for file_path in Path(root_folder).rglob("*list_kg.json"):
        print(f"Processing {file_path}")
        try:
            entities = extract_named_entities_from_file(file_path)
            merge_named_entities(all_named_entities, entities)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    for label in all_named_entities:
        all_named_entities[label] = list(set(all_named_entities[label]))

    return all_named_entities

if __name__ == "__main__":
    root_directory = "NER_sample"
    result = extract_from_all_files(root_directory)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    with open("all_named_entities.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
