import csv
import json

def load_elements_from_csv(filepath):
    """Načte data o prvcích z CSV souboru a vrátí seznam slovníků."""
    elements = [] # Inicializuje prázdný seznam pro uložení prvků
    with open(filepath, 'r', encoding='utf-8') as csvfile: # Otevře CSV soubor pro čtení
        reader = csv.DictReader(csvfile) # Vytvoří čtečku pro čtení CSV souboru jako slovníky
        for row in reader: # Projde všechny řádky v CSV souboru
            elements.append(row) # Přidá řádek (slovník) do seznamu prvků
    return elements # Vrátí seznam prvků

def load_groups_from_json(filepath):
    """Načte data o skupinách z JSON souboru a vrátí slovník."""
    with open(filepath, 'r', encoding='utf-8') as jsonfile: # Otevře JSON soubor pro čtení
        groups = json.load(jsonfile) # Načte data z JSON souboru jako slovník
    return groups # Vrátí slovník skupin

if __name__ == '__main__':
    # test load_elements_from_csv
    elements_data = load_elements_from_csv('elements.csv') # Načte data o prvcích z CSV souboru
    print(f"Načteno {len(elements_data)} prvků.") # Vypíše počet načtených prvků
    print(elements_data[0]) # Vypíše první prvek

    # test load_groups_from_json
    groups_data = load_groups_from_json('groups.json') # Načte data o skupinách z JSON souboru
    print(f"Načteno {len(groups_data)} skupin.") # Vypíše počet načtených skupin
    print(groups_data[0]) # Vypíše první skupinu