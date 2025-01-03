import data_handler
import element_operations
import output_generator

def display_menu():
    """Zobrazí hlavní menu aplikace."""
    print("\n=== Hlavní menu ===")
    print("1. Vyhledávání prvku")
    print("2. Zobrazení vlastností prvku")
    print("3. Výpočet průměrné atomové hmotnosti")
    print("4. Generování HTML tabulky")
    print("5. Export dat do XML")
    print("6. Generování Markdown souboru")
    print("0. Ukončit aplikaci")
    print("=====================")

def get_user_choice():
    """Získá uživatelský vstup pro výběr z menu."""
    while True:
        try:
            choice = int(input("Vyberte možnost: ")) # Získá vstup od uživatele a pokusí se ho převést na celé číslo
            if 0 <= choice <= 6: # Zkontroluje, zda je vstup v platném rozsahu menu
                return choice # Vrátí vybranou možnost, pokud je platná
            else:
                print("Neplatná volba. Zkuste znovu.") # Upozorní uživatele na neplatnou volbu
        except ValueError:
            print("Neplatná volba. Zkuste zadat číslo.") # Upozorní uživatele na neplatnou volbu (nečíselný vstup)

def handle_search_element(elements, groups):
    """Zpracuje vyhledávání prvku."""
    while True:
      print("\n=== Vyhledávání prvku ===")
      print("1. Vyhledat podle chemické značky")
      print("2. Vyhledat podle názvu")
      print("3. Vyhledat podle protonového čísla")
      print("4. Vyhledat podle skupiny")
      print("5. Vyhledat podle periody")
      print("0. Zpět do hlavního menu")
    
      search_choice = get_user_choice() # Získá volbu z menu vyhledávání
      if search_choice == 0: # Pokud uživatel zvolí návrat do hlavního menu
          return # Vrátí se do hlavního menu
      
      search_value = input("Zadejte hledanou hodnotu: ") # Získá hodnotu pro vyhledávání
      
      if search_choice == 1: # Vyhledávání podle chemické značky
            found_element = element_operations.find_element(elements, 'Symbol', search_value.capitalize()) # Volání funkce pro vyhledání prvku
      elif search_choice == 2: # Vyhledávání podle názvu
          found_element = element_operations.find_element(elements, 'Element', search_value.capitalize()) # Volání funkce pro vyhledání prvku
      elif search_choice == 3: # Vyhledávání podle protonového čísla
          try:
              found_element = element_operations.find_element(elements, 'AtomicNumber', int(search_value)) # Volání funkce pro vyhledání prvku, vstup musí být celé číslo
          except ValueError:
              print("Neplatná hodnota protonového čísla. Zkuste to znovu.") # Upozorní uživatele na neplatnou hodnotu protonového čísla
              continue
      elif search_choice == 4: # Vyhledávání podle skupiny
          found_elements = element_operations.find_elements_by_group_name(elements, groups, search_value.capitalize()) # Volání funkce pro vyhledání prvků ve skupině
          if found_elements: # Pokud jsou prvky nalezeny
              for element in found_elements:
                element_operations.display_element_details(element) # Zobrazí detaily všech nalezených prvků
          else:
             print("Prvek nebyl nalezen.") # Pokud nejsou prvky nalezeny
          continue
      elif search_choice == 5: # Vyhledávání podle periody
        try:
              found_element = element_operations.find_element(elements, 'Period', int(search_value)) # Volání funkce pro vyhledání prvku podle periody
        except ValueError:
              print("Neplatná hodnota periody. Zkuste to znovu.") # Upozorní uživatele na neplatnou hodnotu periody
              continue
      
      if found_element: # Pokud je prvek nalezen
         if isinstance(found_element, list): # Pokud je nalezena skupina prvku
           for element in found_element:
             element_operations.display_element_details(element) # Zobrazí detaily všech nalezených prvků
         else: # Pokud je nalezen jeden prvek
            element_operations.display_element_details(found_element) # Zobrazí detaily nalezeného prvku
      else:
           print("Prvek nebyl nalezen.") # Pokud prvek nebyl nalezen

def handle_display_element_details(elements):
    """Zpracuje zobrazení detailů prvku."""
    while True:
        print("\n=== Zobrazení vlastností prvku ===")
        element_symbol = input("Zadejte chemickou značku prvku: ") # Získá chemickou značku od uživatele
        found_elements = element_operations.find_element(elements, 'Symbol', element_symbol) # Volání funkce pro nalezení prvku podle chemické značky

        if found_elements: # Pokud jsou prvky nalezeny
          if len(found_elements) > 0: # Pokud je nalezena skupina prvku
            element_operations.display_element_details(found_elements[0]) # Zobrazí detaily prvního nalezeného prvku
            return # Vrátí se
          else:
            print("Prvek s tímto symbolem nebyl nalezen.") # Upozorní uživatele, že prvek s tímto symbolem nebyl nalezen
        else:
            print("Prvek s tímto symbolem nebyl nalezen.") # Upozorní uživatele, že prvek s tímto symbolem nebyl nalezen


def handle_calculate_average_mass(elements, groups):
    """Zpracuje výpočet průměrné atomové hmotnosti."""
    while True:
        print("\n=== Výpočet průměrné atomové hmotnosti ===")
        print("1. Výpočet pro skupinu")
        print("2. Výpočet pro periodu")
        print("0. Zpět do hlavního menu")
        
        calc_choice = get_user_choice() # Získá volbu z menu pro výpočet průměrné atomové hmotnosti
        if calc_choice == 0: # Pokud se uživatel chce vrátit do hlavního menu
            return # Vrátí se do hlavního menu
        if calc_choice == 1: # Výpočet průměrné atomové hmotnosti pro skupinu
            group_name = input("Zadejte název skupiny: ").capitalize() # Získá název skupiny od uživatele
            average_mass = element_operations.calculate_average_mass(elements, 'Group', group_name, groups) # Volá funkci pro výpočet průměrné atomové hmotnosti
            if average_mass is not None: # Pokud je průměrná atomová hmotnost vypočítána
              print(f"Průměrná atomová hmotnost prvků ve skupině {group_name}: {average_mass:.3f}") # Vypíše průměrnou atomovou hmotnost
              return # Vrátí se
            else:
              print("Skupina nenalezena nebo neobsahuje platné prvky.") # Upozorní uživatele, že skupina nebyla nalezena nebo neobsahuje platné prvky
        elif calc_choice == 2: # Výpočet průměrné atomové hmotnosti pro periodu
            try:
              period_number = int(input("Zadejte číslo periody: ")) # Získá číslo periody od uživatele
              average_mass = element_operations.calculate_average_mass(elements, 'Period', period_number) # Volá funkci pro výpočet průměrné atomové hmotnosti
              if average_mass is not None: # Pokud je průměrná atomová hmotnost vypočítána
                 print(f"Průměrná atomová hmotnost prvků v periodě {period_number}: {average_mass:.3f}") # Vypíše průměrnou atomovou hmotnost
                 return # Vrátí se
              else:
                 print("Perioda nenalezena nebo neobsahuje platné prvky.") # Upozorní uživatele, že perioda nebyla nalezena nebo neobsahuje platné prvky
            except ValueError:
                print("Neplatná hodnota periody. Zkuste to znovu.") # Upozorní uživatele na neplatnou hodnotu periody

def handle_generate_html(elements):
     """Zpracuje generování HTML tabulky."""
     print("\n=== Generování HTML tabulky ===")
     filepath = input("Zadejte název výstupnímu HTML souboru např. (tabulka.html): ") # Získá název souboru pro uložení HTML tabulky
     output_generator.generate_html_table(elements,filepath) # Volá funkci pro vygenerování HTML tabulky
     print(f"HTML tabulka byla vygenerována do {filepath}") # Potvrdí vygenerování HTML tabulky


def handle_export_xml(elements):
    """Zpracuje export dat do XML souboru."""
    while True:
        print("\n=== Export dat do XML souboru ===")
        element_symbol = input("Zadejte chemickou značku prvku: ").capitalize() # Získá chemickou značku od uživatele
        found_elements = element_operations.find_element(elements, 'Symbol', element_symbol) # Volá funkci pro nalezení prvku podle chemické značky
        if found_elements: # Pokud jsou prvky nalezeny
          if len(found_elements) > 1: # Pokud je nalezena skupina prvků
            print("Muzete exportovat jenom jeden prvek, zadali jste skupinu, opakujte zadani") # Upozorní uživatele, že může exportovat pouze jeden prvek
            continue
          else: # Pokud je nalezen pouze jeden prvek
            filepath = input("Zadejte název výstupnímu XML souboru např. (prvek.xml): ") # Získá název souboru pro uložení XML dat
            output_generator.export_to_xml(found_elements[0],filepath) # Volá funkci pro export do XML
            print(f"Data prvku {element_symbol} byla exportována do {filepath}") # Potvrdí export dat do XML
            return # Vrátí se
        else:
            print("Prvek s tímto symbolem nebyl nalezen.") # Upozorní uživatele, že prvek s tímto symbolem nebyl nalezen
       

def handle_generate_markdown(elements, groups):
    """Zpracuje generování Markdown souboru."""
    while True:
      print("\n=== Generování Markdown souboru ===")
      print("1. Generovat přehled pro skupinu")
      print("2. Generovat přehled pro periodu")
      print("0. Zpět do hlavního menu")
      
      md_choice = get_user_choice() # Získá volbu z menu pro generování Markdown souboru
      if md_choice == 0: # Pokud uživatel chce zpět do hlavního menu
           return # Vrátí se do hlavního menu
      if md_choice == 1: # Generování přehledu pro skupinu
        group_name = input("Zadejte název skupiny: ").capitalize() # Získá název skupiny od uživatele
        filepath = input("Zadejte název výstupnímu Markdown souboru např. (skupina.md): ") # Získá název souboru pro uložení Markdown dat
        output_generator.generate_markdown(elements, 'Group', group_name, filepath, groups) # Volá funkci pro generování Markdown souboru
        print(f"Markdown soubor s přehledem pro skupinu {group_name} byl vygenerován do {filepath}") # Potvrdí vygenerování Markdown souboru
        return # Vrátí se

      elif md_choice == 2: # Generování přehledu pro periodu
         try:
           period_number = int(input("Zadejte číslo periody: ")) # Získá číslo periody od uživatele
           filepath = input("Zadejte název výstupnímu Markdown souboru např. (perioda.md): ") # Získá název souboru pro uložení Markdown dat
           output_generator.generate_markdown(elements, 'Period', period_number, filepath) # Volá funkci pro generování Markdown souboru
           print(f"Markdown soubor s přehledem pro periodu {period_number} byl vygenerován do {filepath}") # Potvrdí vygenerování Markdown souboru
           return # Vrátí se
         except ValueError:
            print("Neplatná hodnota periody. Zkuste to znovu.") # Upozorní uživatele na neplatnou hodnotu periody

def main():
    """Hlavní funkce aplikace."""
    elements = data_handler.load_elements_from_csv("elements.csv") # Načte data o prvcích z CSV souboru
    groups = data_handler.load_groups_from_json("groups.json") # Načte data o skupinách z JSON souboru

    while True:
        display_menu() # Zobrazí hlavní menu
        choice = get_user_choice() # Získá volbu z hlavního menu

        if choice == 1: # Volba pro vyhledávání prvku
             handle_search_element(elements,groups) # Volá funkci pro zpracování vyhledávání prvku
        elif choice == 2: # Volba pro zobrazení vlastností prvku
             handle_display_element_details(elements) # Volá funkci pro zobrazení detailů prvku
        elif choice == 3: # Volba pro výpočet průměrné atomové hmotnosti
             handle_calculate_average_mass(elements, groups) # Volá funkci pro výpočet průměrné atomové hmotnosti
        elif choice == 4: # Volba pro generování HTML tabulky
            handle_generate_html(elements) # Volá funkci pro generování HTML tabulky
        elif choice == 5: # Volba pro export do XML
            handle_export_xml(elements) # Volá funkci pro export do XML
        elif choice == 6: # Volba pro generování Markdown souboru
           handle_generate_markdown(elements,groups) # Volá funkci pro generování Markdown souboru
        elif choice == 0: # Volba pro ukončení aplikace
            print("Ukončuji aplikaci.") # Potvrdí ukončení aplikace
            break

if __name__ == "__main__":
    main() # Spustí hlavní funkci aplikace, pokud je skript spuštěn přímo