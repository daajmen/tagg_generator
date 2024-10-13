import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import csv

def läs_config():
    exclude_set = set()
    try:
        with open('config.csv', 'r', newline='', encoding='utf-8') as csvfile:
            innehåll = csvfile.read()
            exclude_set.update([item.strip().lower() for item in innehåll.split(';') if item.strip()])
    except FileNotFoundError:
        print("Ingen config.csv hittad. Fortsätter utan exkluderingar.")
    return exclude_set

def innehåller_någon_term(namn, exclude_terms):
    return any(term in namn for term in exclude_terms)

def välj_fil_och_processa(exclude_terms):
    root = tk.Tk()
    root.withdraw()  # Gömmer huvudfönstret för Tkinter
    filväg = filedialog.askopenfilename(filetypes=[("TMC files", "*.tmc")])
    if not filväg:
        return

    namn_set = set()

    träd = ET.parse(filväg)
    rot = träd.getroot()

    for symbol in rot.findall('.//Symbol'):
        namn = symbol.find('Name')
        if namn is not None:
            clean_name = namn.text.strip()
            if not innehåller_någon_term(clean_name.lower(), exclude_terms):
                namn_set.add(clean_name)
                
    # Skapa en CSV-fil och skriv de unika namnen
    with open('unika_namn.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Unika Namn'])
        for namn in sorted(namn_set):
            writer.writerow([namn])

    print(f"Klar! Hittade {len(namn_set)} unika namn som har sparats i unika_namn.csv")

exclude_terms = läs_config()
välj_fil_och_processa(exclude_terms)
