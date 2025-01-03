def find_element(elements, search_criteria, search_value):
    """Najde prvek podle zadaných kritérií."""
    found_elements = [] # Inicializuje seznam pro uložení nalezených prvků
    for element in elements: # Projde všechny prvky
        if search_criteria in element: # Pokud kritérium hledání existuje v prvku
           if isinstance(search_value, int): # Pokud je hledaná hodnota celé číslo
               try: # Pokusí se o následující operace
                    if int(element[search_criteria]) == search_value: # Pokud se hodnota v prvku rovná hledané hodnotě
                        found_elements.append(element) # Přidá prvek do seznamu nalezených
               except ValueError: # Pokud se vyskytne chyba ValueError
                 continue # Pokračuje na další prvek
           elif element[search_criteria] == search_value: # Pokud se hodnota v prvku rovná hledané hodnotě jako text
            found_elements.append(element) # Přidá prvek do seznamu nalezených
    
    return found_elements if found_elements else None # Vrátí nalezené prvky nebo None, pokud nejsou žádné nalezeny


def find_elements_by_group_name(elements, groups, group_name):
    """Najde prvky podle názvu skupiny."""
    found_group = None # Inicializuje proměnnou pro nalezenou skupinu
    for group in groups: # Projde všechny skupiny
        if group['cs'].lower() == group_name.lower() or group['en'].lower() == group_name.lower(): # Pokud se název skupiny shoduje
             found_group = group # Nastaví nalezenou skupinu
             break
    if found_group: # Pokud je skupina nalezena
      found_elements = [] # Inicializuje seznam pro uložení nalezených prvků
      for element in elements: # Projde všechny prvky
        if element['Symbol'] in found_group['elements']: # Pokud je symbol prvku v seznamu prvků ve skupině
          found_elements.append(element) # Přidá prvek do seznamu nalezených
      return found_elements # Vrátí seznam nalezených prvků
    return None # Vrátí None, pokud skupina není nalezena

def display_element_details(element):
    """Zobrazí detailní informace o prvku."""
    if element: # Pokud je prvek platný
        print("\n=== Detail prvku ===")
        for key, value in element.items(): # Projde všechny položky ve slovníku prvku
            print(f"{key}: {value}") # Vypíše klíč a hodnotu položky
    else:
        print("Prvek nenalezen") # Vypíše zprávu, že prvek nebyl nalezen

def calculate_average_mass(elements, group_or_period, value, groups=None):
    """Vypočítá průměrnou atomovou hmotnost pro skupinu nebo periodu."""
    total_mass = 0  # Inicializuje celkovou hmotnost na 0
    valid_element_count = 0  # Inicializuje počet platných prvků na 0
    if group_or_period == 'Group':  # Pokud se jedná o výpočet pro skupinu
        found_elements = find_elements_by_group_name(elements, groups, value)  # Najde prvky podle názvu skupiny
        if found_elements:  # Pokud jsou prvky nalezeny
            for element in found_elements:  # Projde všechny nalezené prvky
                try:  # Pokusí se o následující operace
                    total_mass += float(element['AtomicMass'])  # Přičte atomovou hmotnost k celkové hmotnosti
                    valid_element_count += 1  # Zvýší počet platných prvků o 1
                except ValueError:  # Pokud se vyskytne chyba ValueError
                    continue  # Pokračuje na další prvek
        else:  # Pokud nejsou prvky nalezeny
            return None  # Vrátí None
    else:  # Pokud se jedná o výpočet pro periodu
        for element in elements:  # Projde všechny prvky
            if group_or_period in element:  # Pokud kritérium (perioda) existuje v prvku
                if isinstance(value, int):  # Pokud je hodnota periody celé číslo
                    try:  # Pokusí se o následující operace
                        if int(element[group_or_period]) == value:  # Pokud se perioda prvku rovná hledané periodě
                            try:  # Pokusí se o následující operace
                                total_mass += float(element['AtomicMass'])  # Přičte atomovou hmotnost k celkové hmotnosti
                                valid_element_count += 1  # Zvýší počet platných prvků o 1
                            except ValueError:  # Pokud se vyskytne chyba ValueError (např. neplatná atomová hmotnost)
                                continue  # Pokračuje na další prvek
                    except ValueError: # Pokud se vyskytne chyba ValueError (např. neplatná perioda)
                       continue # Pokračuje na další prvek
                elif element[group_or_period] == value:  # Pokud se perioda prvku rovná hledané periodě jako text
                    try:  # Pokusí se o následující operace
                        total_mass += float(element['AtomicMass'])  # Přičte atomovou hmotnost k celkové hmotnosti
                        valid_element_count += 1  # Zvýší počet platných prvků o 1
                    except ValueError:  # Pokud se vyskytne chyba ValueError (např. neplatná atomová hmotnost)
                        continue  # Pokračuje na další prvek

    if valid_element_count > 0:  # Pokud je počet platných prvků větší než 0
        return total_mass / valid_element_count  # Vrátí průměrnou atomovou hmotnost
    return None  # Vrátí None, pokud nebyly nalezeny žádné platné prvky