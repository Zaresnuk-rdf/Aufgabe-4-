import tkinter as tk
import mariadb
from tkinter import messagebox

# Verbindung zur Datenbank herstellen
try:
    conn = mariadb.connect(
        user="WIV_Denis",
        password="denisHDD1996",
        host="localhost",
        port=3306,
        database="schlumpfshop3"
    )
    cur = conn.cursor()
except mariadb.Error as e:
    messagebox.showerror("Fehler", f"Verbindung zur Datenbank konnte nicht hergestellt werden: {e}")
    raise  # Beende das Programm, wenn keine Verbindung zur DB hergestellt werden kann

# Klasse für Kundenobjekte
class Kunde:
    def __init__(self, anrede, vorname, nachname, strasse, hausnummer, ortid):
        self.anrede = anrede
        self.vorname = vorname
        self.nachname = nachname
        self.strasse = strasse
        self.hausnummer = hausnummer
        self.ortid = ortid

# Funktion zur Kundenabfrage
def kunden_abfragen():
    plz = plz_entry.get()

    if not plz.isdigit() or len(plz) != 5:  # Überprüfung auf gültige Postleitzahl (5 Ziffern)
        messagebox.showerror("Fehler", "Bitte eine gültige 5-stellige Postleitzahl eingeben!")
        return

    try:
        # SQL-Abfrage: Alle Kunden mit der angegebenen Postleitzahl (OrtID)
        cur.execute(
            """
            SELECT Anrede, Vorname, Name, Strasse, Husnummer, OrtID
            FROM kunden
            WHERE OrtID = ?
            """, 
            (plz,)  # Die Postleitzahl wird als Abfrageparameter verwendet
        )
        kunden = cur.fetchall()

        kunden_liste = []
        for anrede, vorname, nachname, strasse, hausnummer, ortid in kunden:
            kunde = Kunde(anrede, vorname, nachname, strasse, hausnummer, ortid)
            kunden_liste.append(kunde)

        ausgabe_text.delete("1.0", tk.END)  # Textfeld löschen, um neue Ausgabe zu zeigen

        if not kunden_liste:
            ausgabe_text.insert(tk.END, f"Keine Kunden mit der Postleitzahl {plz} gefunden.")
        else:
            for kunde in kunden_liste:
                ausgabe_text.insert(tk.END, f"{kunde.anrede} {kunde.vorname} {kunde.nachname} - {kunde.strasse} {kunde.hausnummer}, PLZ: {kunde.ortid}\n")

    except mariadb.Error as e:
        messagebox.showerror("Datenbankfehler", f"Fehler bei der Datenbankabfrage: {e}")

# GUI erstellen
fenster = tk.Tk()
fenster.title("Kundenabfrage nach Postleitzahl")

tk.Label(fenster, text="Postleitzahl eingeben:").pack(pady=5)
plz_entry = tk.Entry(fenster)
plz_entry.pack(pady=5)

# Button zum Starten der Abfrage
tk.Button(fenster, text="Kunden suchen", command=kunden_abfragen).pack(pady=5)

# Textfeld zur Ausgabe der Kunden
ausgabe_text = tk.Text(fenster, height=15, width=50)
ausgabe_text.pack(pady=5)

fenster.mainloop()

# Am Ende: Verbindung schließen
cur.close()
conn.close()
