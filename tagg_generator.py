import xml.etree.ElementTree as ET
import pandas as pd
import re 
import csv

class Webport:
    def __init__(self, startwith, contains, endswith, find, replace, rawmin, rawmax, engmin, engmax, unit, formats, description, alarmoption, trendoption):
        self.startwith = startwith
        self.contains = contains
        self.endswith = endswith
        self.find = find
        self.replace = replace
        self.rawmin = rawmin
        self.rawmax = rawmax
        self.engmin = engmin
        self.engmax = engmax
        self.unit = unit
        self.formats = formats
        self.description = description
        self.alarmoption = alarmoption
        self.trendoption = trendoption

# returnera dataframe från pd
def import_filter(path_to_import):
    try:
        df = pd.read_csv(path_to_import, on_bad_lines='skip', sep=";")
    except FileNotFoundError:
        print("Inget importfilter hittat. Stoppar skriptet")
    return df                  


# Skicka in element från iterparse, sträng på block i symbol. 
def find_symbol(element, dataframe):
    symbol = []
    found_tag = {'system': '', 'component': ''}

    if element.text:
         # Gå igenom varje rad i 'endswitch'-kolumnen, detta är mot importfiltret...
        for sufix in dataframe['endswith']:
            if isinstance(sufix, str):
                sufix = sufix.split('.')
                sufix = sufix[0]
                
                # Kontrollera om värdet finns i element.tex
                if isinstance(sufix, str) and element.text.endswith(sufix): # lösa taggar. 
                    symbol = re.split(r'[.]', element.text)  # Dela på både _ och .
                    if len(symbol) > 1: 
                        found_tag['system'] = re.split(r'[.]', element.text)[0]  # Dela på både _ och .
                        found_tag['component'] = re.split(r'[.]', element.text)[1]  # Dela på både _ och .
                    else: 
                        found_tag['system'] = re.split(r'[.]', element.text)[0]  # Dela på både _ och .
                    return found_tag

def extract_symbols(path_to_file, dataframe):
    try:
        tagg_lista = []

        context = ET.iterparse(path_to_file, events=("start", "end"))
        for event, elem in context: 
            data = find_symbol(elem, dataframe)
            if data: 
                tagg_lista.append(data)

        return tagg_lista

    except FileNotFoundError:
        print("Hittade ingen fil, försök igen.")
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def make_tagg_list(symbol_dict, import_filter):
    test_frame = pd.DataFrame(columns=['name', 'device', 'address', 'datatype', 'rawmin', 'rawmax', 'engmin', 'engmax', 'unit', 'format', 'description', 'alarmoptions', 'trendoptions'])

    for my_dict in symbol_dict: 
        my_string = (f" {my_dict['system']}_{my_dict['component']} ")

        #for blocks, replace_value in import_filter['endswith']['replace']:
        for index, row in import_filter.iterrows(): 
            try:
                import_row = Webport(
                    startwith = row['startwith'],
                    contains = row['contains'],
                    endswith = row['endswith'].split('.')[0],
                    find = row['find'],
                    replace = row['replace'],
                    rawmin = row['rawmin'],
                    rawmax = row['rawmax'],
                    engmin = row['engmin'],
                    engmax = row['engmax'],
                    unit = row['unit'],
                    formats = row['format'],
                    description = row['description'],
                    alarmoption = row['alarmoption'],
                    trendoption = row['trendoption'])
                


                if isinstance(import_row.endswith, str) and import_row.endswith in my_string: 
                    output = my_string.replace(import_row.endswith,import_row.replace)

                    csv_row = {
                        'name': output,
                        'device': 'AS01',
                        'address': my_string + import_row.replace,  # Lägg till address här                        
                        'datatype': 'BOOL',
                        'rawmin': import_row.rawmin,
                        'rawmax': import_row.rawmin,
                        'engmin': import_row.engmin,
                        'engmax': import_row.engmax,
                        'unit': import_row.unit,
                        'format': import_row.formats,
                        'description': import_row.description,
                        'alarmoption': import_row.alarmoption,
                        'trendoption': import_row.trendoption
                        }    
                    csv_row_df = pd.DataFrame([csv_row])   
                    #print(csv_row)             
                    test_frame = pd.concat([test_frame,csv_row_df], ignore_index=True)
            except Exception as e:
                #print(f"Error processing row {index}: {e}")
                pass
    filename = 'first_try_tagglist.csv'
    test_frame.to_csv(filename, index=False, encoding='utf-8',sep=';' )


# Make csv structure. 
def make_tagglist_header():
    df = pd.DataFrame(columns=['name', 'device', 'address', 'datatype', 'rawmin', 'rawmax', 'engmin', 'engmax', 'unit', 'format', 'description', 'alarmoptions', 'trendoptions'])
    filename = 'generated_list.csv'
    df.to_csv(filename, index=False, encoding='utf-8',sep=';' )
    return df

# Använd funktionen för att bearbeta filen och hämta symbolerna
#file_path = input('Enter file path to TMC file: \n')
file_path = 'assets/AS1.tmc'
df = import_filter('assets/ImportFilter.csv')

# Rådata med alla taggar. 
symbols_list = extract_symbols(file_path,df)

#print(symbols_list)
# Skapa header i csv, retur df som tagglist. 
tagglist = make_tagglist_header()
make_tagg_list(symbols_list,df)



