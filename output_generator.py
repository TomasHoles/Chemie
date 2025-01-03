import csv
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import xml.sax.saxutils
from lxml import etree


def generate_html_table(elements, output_filepath):
    """Vygeneruje HTML tabulku s informacemi o prvcích, která vypadá jako periodická tabulka."""

    # Find max period and group to create the table dimensions
    max_period = max(int(element['Period']) for element in elements) # Najde maximální periodu
    max_group = 18 # Maximální počet skupin

    # Create a dictionary of elements indexed by their period and group
    element_grid = {} # Vytvoří prázdný slovník pro uložení prvků podle periody a skupiny
    for element in elements: # Projde všechny prvky
        period = int(element['Period']) # Získá periodu prvku
        group = element['Group'] # Získá skupinu prvku
        if group == '': # Pokud je skupina prázdná
            group = 0 # Nastaví skupinu na 0
        else: # Pokud skupina není prázdná
             group = int(group) # Převede skupinu na celé číslo

        if period not in element_grid: # Pokud perioda není v slovníku
            element_grid[period] = {} # Vytvoří nový slovník pro danou periodu
        element_grid[period][group] = element # Uloží prvek do slovníku podle periody a skupiny

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Periodická tabulka prvků</title>
        <style>
            table {
                border-collapse: collapse;
                width: 90%; /* Adjust table width as needed */
                margin: auto; /* Center the table */
                table-layout: fixed; /* Ensure cell sizes are respected */
            }
             th, td {
                border: 1px solid black;
                 padding: 5px;
                text-align: center;
                width: 30px;  /* Adjust cell width */
                height: 30px; /* Adjust cell height */
                 font-size: 10px; /*Adjust cell font size*/

            }
            th {
                background-color: #f2f2f2;
                 font-size: 12px; /*Adjust th font size*/
            }
           .empty-cell {
                border: none;
             }
           .lanthanide {
             background-color: #e0e0f0;
           }

           .actinide {
                background-color: #f0e0e0;
            }
           .alkali-metal {
              background-color: #ffcccc; /* Light Red for Alkali Metals*/
           }
           .alkaline-earth-metal {
               background-color: #ffd8b1; /* Light Orange for Alkaline Earth Metals*/
           }
           .transition-metal {
               background-color: #ffffcc;/* Light Yellow for Transition Metals*/
           }
           .post-transition-metal {
               background-color: #c6ffb3;/* Light Green for Post-Transition Metals*/
           }
           .metalloid {
              background-color: #c6e2ff;/* Light Blue for Metalloids*/
           }
           .nonmetal {
              background-color: #d9e9ff;/* Light Indigo for Nonmetals*/
           }
           .halogen {
               background-color: #c0b2ff; /* Light Violet for Halogens*/
           }
           .noble-gas {
               background-color: #f5b1f0;/* Light Pink for Noble Gases*/
            }
        </style>
    </head>
    <body>
        <h2>Periodická tabulka prvků</h2>
        <table>
            <thead>
                <tr>
    """

    # Create group headers
    for i in range(1,max_group+1): # Projde všechny skupiny
        html_content += f"<th>{i}</th>" # Přidá hlavičku pro skupinu
    html_content += "</tr></thead><tbody>" # Ukončí hlavičku tabulky a zahájí tělo tabulky

    # Create table rows with elements
    for period in range(1, max_period + 1): # Projde všechny periody
        html_content += "<tr>" # Zahájí řádek tabulky
        for group in range(1, max_group + 1): # Projde všechny skupiny
            if period in element_grid and group in element_grid[period]: # Pokud prvek existuje pro danou periodu a skupinu
                 element = element_grid[period][group] # Získá prvek
                 element_type_class = "" # Inicializuje prázdnou třídu pro typ prvku
                 if element['Type'] == 'Alkali Metal': # Pokud je prvek alkalický kov
                       element_type_class = "alkali-metal" # Nastaví třídu pro alkalický kov
                 elif element['Type'] == 'Alkaline Earth Metal': # Pokud je prvek kov alkalických zemin
                        element_type_class = "alkaline-earth-metal" # Nastaví třídu pro kov alkalických zemin
                 elif element['Type'] == 'Transition Metal': # Pokud je prvek přechodný kov
                       element_type_class = "transition-metal" # Nastaví třídu pro přechodný kov
                 elif element['Type'] == 'Post-Transition Metal': # Pokud je prvek post-přechodný kov
                     element_type_class = "post-transition-metal" # Nastaví třídu pro post-přechodný kov
                 elif element['Type'] == 'Metalloid': # Pokud je prvek metaloid
                       element_type_class = "metalloid" # Nastaví třídu pro metaloid
                 elif element['Type'] == 'Nonmetal': # Pokud je prvek nekov
                        element_type_class = "nonmetal" # Nastaví třídu pro nekov
                 elif element['Type'] == 'Halogen': # Pokud je prvek halogen
                        element_type_class = "halogen" # Nastaví třídu pro halogen
                 elif element['Type'] == 'Noble Gas': # Pokud je prvek vzácný plyn
                        element_type_class = "noble-gas" # Nastaví třídu pro vzácný plyn
                 elif element['Type'] == 'Lanthanide': # Pokud je prvek lanthanoid
                        element_type_class = "lanthanide" # Nastaví třídu pro lanthanoid
                 elif element['Type'] == 'Actinide': # Pokud je prvek aktinoid
                       element_type_class = "actinide" # Nastaví třídu pro aktinoid

                 html_content += f"<td class='{element_type_class}'>{element['Symbol']}<br>{element['AtomicNumber']}</td>" # Přidá buňku s prvkem a jeho atomovým číslem
            else: # Pokud prvek pro danou periodu a skupinu neexistuje
                 html_content += "<td class='empty-cell'></td>" # Přidá prázdnou buňku

        html_content += "</tr>" # Ukončí řádek tabulky


    # add the lanthanides and actinides to the bottom
    html_content += "<tr><td colspan='18'><hr style='border-top: 1px solid black;'/></td></tr>" # Přidá oddělovač
    html_content += "<tr>" # Zahájí řádek tabulky pro lanthanoidy
    for element in elements: # Projde všechny prvky
      if element['Type'] == 'Lanthanide': # Pokud je prvek lanthanoid
          html_content += f"<td class='lanthanide'>{element['Symbol']}<br>{element['AtomicNumber']}</td>" # Přidá buňku s prvkem a jeho atomovým číslem
    html_content += "</tr><tr>" # Ukončí řádek tabulky pro lanthanoidy a zahájí řádek pro aktinoidy
    for element in elements: # Projde všechny prvky
      if element['Type'] == 'Actinide': # Pokud je prvek aktinoid
          html_content += f"<td class='actinide'>{element['Symbol']}<br>{element['AtomicNumber']}</td>" # Přidá buňku s prvkem a jeho atomovým číslem
    html_content += "</tr>" # Ukončí řádek tabulky pro aktinoidy

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(output_filepath, 'w', encoding='utf-8') as html_file: # Otevře soubor pro zápis HTML
        html_file.write(html_content) # Zapíše HTML obsah do souboru



def export_to_xml(element, output_filepath):
    """Exportuje informace o prvku do XML souboru pomocí lxml."""
    root = etree.Element("element") # Vytvoří kořenový element XML
    for key, value in element.items(): # Projde všechny položky ve slovníku prvku
        if key == "Symbol": # Pokud je klíč "Symbol"
            elem = etree.SubElement(root, "Symbol") # Vytvoří subelement "Symbol"
            elem.text = str(value) # Nastaví text elementu
        else: # Pro ostatní klíče
           elem = etree.SubElement(root, key) # Vytvoří subelement s klíčem
           elem.text = str(value) # Nastaví text elementu
    
    tree = etree.ElementTree(root) # Vytvoří strom XML z kořenového elementu
    tree.write(output_filepath, pretty_print=True, encoding='utf-8', xml_declaration=True) # Zapíše XML do souboru s formátováním


def generate_markdown(elements, group_or_period, value, output_filepath, groups = None):
    """Vygeneruje Markdown soubor s informacemi o prvcích."""
    markdown_content = f"# Přehled prvků v {group_or_period}: {value}\n\n" # Vytvoří hlavičku Markdown souboru
    if group_or_period == 'Group': # Pokud se jedná o generování pro skupinu
      found_group = None # Inicializuje proměnnou pro nalezenou skupinu
      for group in groups: # Projde všechny skupiny
        if group['cs'].lower() == value.lower() or group['en'].lower() == value.lower(): # Pokud se název skupiny shoduje
             found_group = group # Nastaví nalezenou skupinu
             break
      if found_group: # Pokud je skupina nalezena
        filtered_elements = [element for element in elements if element['Symbol'] in found_group['elements']] # Filtruje prvky podle nalezené skupiny

        markdown_content += "| Chemická Značka | Název | Protonové číslo | Relativní atomová hmotnost |\n" # Vytvoří hlavičku tabulky v Markdown
        markdown_content += "|---|---|---|---|\n" # Vytvoří oddělovač v tabulce Markdown
        for element in filtered_elements: # Projde všechny filtrované prvky
            markdown_content += f"| {element['Symbol']} | {element['Element']} | {element['AtomicNumber']} | {element['AtomicMass']} |\n" # Přidá řádek s daty prvku do tabulky Markdown
      else: # Pokud není skupina nalezena
          markdown_content += "Žádné prvky nenalezeny s tímto kritériem." # Vypíše zprávu o nenalezení prvků
    elif group_or_period == 'Period': # Pokud se jedná o generování pro periodu
        try: # Pokusí se o následující operace
           filtered_elements = [element for element in elements if int(element['Period']) == value] # Filtruje prvky podle periody
           markdown_content += "| Chemická Značka | Název | Protonové číslo | Relativní atomová hmotnost |\n" # Vytvoří hlavičku tabulky v Markdown
           markdown_content += "|---|---|---|---|\n" # Vytvoří oddělovač v tabulce Markdown
           for element in filtered_elements: # Projde všechny filtrované prvky
                markdown_content += f"| {element['Symbol']} | {element['Element']} | {element['AtomicNumber']} | {element['AtomicMass']} |\n" # Přidá řádek s daty prvku do tabulky Markdown
        except ValueError: # Pokud se vyskytne chyba ValueError
           markdown_content += "Žádné prvky nenalezeny s tímto kritériem." # Vypíše zprávu o nenalezení prvků



    with open(output_filepath, 'w', encoding='utf-8') as md_file: # Otevře soubor pro zápis Markdown
        md_file.write(markdown_content) # Zapíše Markdown obsah do souboru