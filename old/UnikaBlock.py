import tkinter as tk
from tkinter import filedialog
import csv

def välj_csv_fil():
    root = tk.Tk()
    root.withdraw()  # Gömmer huvudfönstret för Tkinter
    filväg = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return filväg

def extrahera_unika_block(filväg):
    unika_block = set()
    with open(filväg, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            for cell in rad:
                block = '_' + cell.split('_')[-1]  # Tar alltid det sista elementet efter split
                unika_block.add(block)

    return unika_block

def spara_unika_block(unika_block, filväg):
    ny_filväg = 'unika_block.csv'  # Anger en ny filnamn för de unika blocken
    with open(ny_filväg, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for block in sorted(unika_block):
            writer.writerow([block])

    print(f"Unika block har sparats i: {ny_filväg}")

def main():
    filväg = välj_csv_fil()
    if not filväg:
        print("Ingen fil valdes.")
        return
    unika_block = extrahera_unika_block(filväg)
    spara_unika_block(unika_block, filväg)

main()
