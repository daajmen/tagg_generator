import xml.etree.ElementTree as ET
import pandas as pd
import re 

# returnera dataframe från pd
def import_filter(path_to_import):
    try:
        df = pd.read_csv(path_to_import, on_bad_lines='skip', sep=";")
    except FileNotFoundError:
        print("Inget importfilter hittat. Stoppar skriptet")
    return df                  


# Skicka in element från iterparse, sträng på block i symbol. 
def find_symbol(element, dataframe):
    tagg_lista = []

    if element.text:
         # Gå igenom varje rad i 'endswitch'-kolumnen
        for sufix in dataframe['endswith']:
            if isinstance(sufix, str):
                sufix = sufix.split('.')
                sufix = sufix[0]
                
                # Kontrollera om värdet finns i element.tex
                if isinstance(sufix, str) and element.text.endswith(sufix): # lösa taggar. 
                    #print(f'Matchning: {element.text}, sufixet var: {sufix}') # Det som finns inne i taggen. 
                    formated_tagg = re.split(r'[.]', element.text)  # Dela på både _ och .
                    print(formated_tagg)
                    #tagg_lista.append()


    return tagg_lista


def extract_symbols(path_to_file, dataframe):
    try:
        context = ET.iterparse(path_to_file, events=("start", "end"))
        for event, elem in context: 
            #print(f'Tag: {elem.text}')
            find_symbol(elem, dataframe)

    except FileNotFoundError:
        print("Hittade ingen fil, försök igen.")
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")


# Använd funktionen för att bearbeta filen och hämta symbolerna
file_path = input('Enter file path to TMC file: \n')
df = import_filter('assets/ImportFilter.csv')

symbols_list = extract_symbols(file_path,df)
