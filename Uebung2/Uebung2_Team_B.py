"""
Teilnehmer: CSKK, BNWK, NSBG, VRGA

Aufgabe 1 – Funktionen des Codes:
Einfache Aufgabenverwaltung (To-do-Liste) im Speicher:
- add_task:               legt eine Aufgabe an (Name, Fälligkeit, Priorität,
                          erledigt-Flag, Benutzer, Erstellzeitpunkt) und gibt die ID zurück
- remove_task:            löscht eine Aufgabe per ID (True/False)
- mark_done:              markiert Aufgaben anhand ihres Namens als erledigt
- show_tasks:             gibt alle Aufgaben auf der Konsole aus
- process_tasks:          schaltet bei einer ZUFÄLLIGEN Aufgabe den Status um
- calculate_task_average: berechnet den Durchschnitt der Aufgaben-IDs
- upcoming_tasks:         soll anstehende Aufgaben liefern (sortiert)
- cleanup:                entfernt alle erledigten Aufgaben
- get_task_count:         liefert die Anzahl der Aufgaben

Was das Verständnis erschwert
- Aufgabe als Liste gespeichert, Zugriff nur über Positionen (task[0],
  task[3] ...): ohne Blick in add_task ist unklar, dass z. B. task[3]
  der Erledigt-Status ist
- Benutzer ist fest "user1" (hart codiert): kann nicht übergeben werden,
  das Feld ist damit für alle Aufgaben identisch und ohne Aussagekraft
- ID-Vergabe len(tasks) + random.randint(2, 7): nicht nachvollziehbar,
  nicht reproduzierbar; da len(tasks) nur um 1 wächst, überschneidet sich
  der Bereich mit bereits vergebenen IDs -> hohe Gefahr, dass eine neue
  Aufgabe still eine bestehende überschreibt
- task_id kann zusätzlich von außen übergeben werden: ID-Vergabe ist damit
  nicht an einer Stelle zentralisiert, eine vorhandene ID überschreibt still
  eine bestehende Aufgabe, gemischte ID-Typen möglich ("hello" neben int)
- tasks wird nicht direkt bei der Deklaration (tasks = None) als leeres
  Dict angelegt, sondern erst "lazy" in add_task -> remove_task, show_tasks,
  calculate_task_average usw. stürzen ab, wenn vorher kein add_task lief
- global-Anweisungen inkonsistent und großteils unnötig: nur in add_task
  (tasks = {}) wirklich nötig, in remove_task/mark_done/show_tasks/cleanup
  wirkungslos -> täuscht eine Neuzuweisung vor
- backup_tasks: Zweck unklar, kein echtes Backup (gleiche Listen-Referenz,
  wird bei remove_task nicht angepasst), wird nirgends gelesen
- process_tasks: Zweck unklar, zufälliges Umschalten, gibt immer False zurück,
  Absturz bei leerer Liste; "# TODO" steht ohne Beschreibung da (unklar,
  was noch zu tun ist) und steht zudem erst hinter dem return
- calculate_task_average: Durchschnitt von IDs ist fachlich sinnlos und
  stürzt bei String-IDs ab (TypeError)
- upcoming_tasks: vergleicht Datum als String "TT-MM-JJJJ" (falsch!),
  sortiert nach Name statt Datum, enthält auch erledigte Aufgaben, obwohl
  die Ausgabe "Offene Aufgaben nach Datum sortiert" behauptet
- mark_done: arbeitet über den Namen (markiert alle Duplikate) und gibt
  immer "Erledigt" zurück, auch wenn keine Aufgabe gefunden wurde
- cleanup: Name verrät nicht, was gelöscht wird; Sonderfall-return unnötig
- get_task_count: umständlich (sum(1 for _ in tasks) statt len(tasks))
- Keine Docstrings, Kommentare oder Type Hints; Testaufrufe ohne
  if __name__ == "__main__" direkt im Modul
- Der Docstring Kommentar '# Wichtig! Nicht verändern!' ohne Beschreibung/
  Begründung ist irreführend und unübersichtlich
"""

"""
Aufgabe 2 – Bewertung aus Sicht der Softwarequalität
Positiv:
- Kleine, überschaubare Funktionen mit je einer Aufgabe
- Funktionsnamen größtenteils sprechend (add_task, remove_task, show_tasks)
- Default-Parameter für priority vorhanden (Aufruf ohne Priorität möglich)
- add_task gibt die vergebene ID zurück, remove_task meldet Erfolg als bool
- Lesbare Ausgabe per f-String in show_tasks
- Nur Standardbibliothek, keine externen Abhängigkeiten

Negativ:
- Struktur:      globaler Zustand, Datenmodell als Liste, Testcode im Modul
- Lesbarkeit:    Magic-Indizes und Magic Values ("user1", Datumsformat);
                 Prioritäts-Skala undokumentiert, Default 3 als Magic Number
- Dokumentation: keine Docstrings, keine Type Hints, TODO ohne Inhalt
- Robustheit:    Absturz bei leerer/uninitialisierter Liste, keine
                 Eingabeprüfung, ID-Kollisionen, String-Datumsvergleich
- Fehlervermeidung: Rückgabewerte ohne Aussage (mark_done, process_tasks)
- Wartbarkeit:   Änderung der Listenreihenfolge zerstört alle Funktionen,
                 backup_tasks und process_tasks ohne erkennbaren Zweck

Mögliche Verbesserungen:
1.  tasks direkt als {} initialisieren, überflüssige global entfernen
2.  Aufgabe als dict/dataclass mit benannten Feldern statt Liste
3.  Konstanten statt Magic Values (DATE_FORMAT, DEFAULT_USER,
    DEFAULT_PRIORITY), Prioritäts-Skala dokumentieren, Benutzer
    als Parameter übergeben
4.  ID-Vergabe zentral in add_task, Kollisionen verhindern (die Zeile mit
    random.randint bleibt laut Vorgabe unverändert)
5.  Fälligkeitsdatum als datetime.date speichern und vergleichen
6.  Eingaben validieren (Priorität 1-3, Datumsformat) mit klaren Fehlern
7.  mark_done über ID statt Name, Rückgabe True/False
8.  upcoming_tasks: nur offene Aufgaben ab heute, nach Datum sortiert
9.  calculate_task_average fachlich sinnvoll machen (z. B. die Durchschnittliche-Priorität)
10. process_tasks entfernen oder Zweck klar definieren (TODO auflösen)
11. backup_tasks entfernen oder als echte Kopie (copy.deepcopy) pflegen
12. cleanup umbenennen (remove_done_tasks) und vereinfachen
13. get_task_count mit len(tasks) umsetzen
14. Docstrings und Type Hints für alle Funktionen
15. Testaufrufe in main() mit if __name__ == "__main__" kapseln
"""

import datetime
import random

# A3: Konstanten statt Magic Values - Formate und Defaults an einer Stelle
DATE_FORMAT = "%d-%m-%Y"                 # Fälligkeitsdatum, z. B. "25-05-2025"
DATETIME_FORMAT = "%d-%m-%Y %H:%M"       # Erstellzeitpunkt einer Aufgabe
DEFAULT_USER = "user1"                   # Benutzer, falls keiner übergeben wird
# Prioritäts-Skala: 1 = hoch, 2 = mittel, 3 = niedrig
DEFAULT_PRIORITY = 3

# A3: tasks direkt als leeres Dict initialisiert (statt None + Lazy-Init in
# add_task) -> alle Funktionen funktionieren auch ohne vorheriges add_task
tasks = {}
backup_tasks = {}


# A3: Default-Priorität als Konstante, Benutzer als Parameter "user" statt
# fest "user1" (neuer Parameter am Ende -> bestehende Aufrufe bleiben gültig)
def add_task(name, due_date, priority=DEFAULT_PRIORITY, task_id=None,
             user=DEFAULT_USER):
    # A3: "global" entfernt - tasks/backup_tasks werden nur verändert,
    # nicht neu zugewiesen; Lazy-Init entfällt (siehe oben)
    if task_id is None:  # A3: "is None" statt "== None" (PEP 8)
        task_id = len(tasks) + random.randint(2, 7)  # Wichtig! Nicht verändern!
    # A3: Aufgabe als dict mit benannten Feldern statt Liste -> Zugriff über
    # task["done"] statt task[3], Reihenfolge der Felder spielt keine Rolle mehr
    task = {
        "name": name,
        "due_date": due_date,
        "priority": priority,
        "done": False,
        "user": user,
        "created_at": datetime.datetime.now().strftime(DATETIME_FORMAT),  # A3: Konstante
    }
    tasks[task_id] = task
    backup_tasks[task_id] = task
    return task_id


def remove_task(task_id):
    # A3: überflüssiges "global tasks" entfernt
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False


def mark_done(task_name):
    # A3: überflüssiges "global tasks" entfernt
    for task_id, task in tasks.items():
        if task["name"] == task_name:  # A3: benannte Felder statt Indizes
            task["done"] = True
    return "Erledigt"


def show_tasks():
    # A3: überflüssiges "global tasks" entfernt
    for task_id, task in tasks.items():
        # A3: benannte Felder statt Indizes, Status vorab berechnet (lesbarer)
        status = "Erledigt" if task["done"] else "Offen"
        print(f"{task_id}: {task['name']} ({task['priority']}) - "
              f"bis {task['due_date']} - {status}")


def process_tasks():
    rand_id = random.choice(list(tasks.keys()))
    tasks[rand_id]["done"] = not tasks[rand_id]["done"]  # A3: benanntes Feld
    return False
    # TODO


def calculate_task_average():
    total = sum(tasks.keys())
    avg = total / len(tasks) if tasks else 0
    return avg


def upcoming_tasks():
    today = datetime.datetime.now().strftime(DATE_FORMAT)  # A3: Konstante
    # A3: benannte Felder statt Indizes (Logik selbst wird in 3.8 korrigiert)
    upcoming = sorted(
        [task for task in tasks.values() if task["due_date"] >= today],
        key=lambda task: task["name"]
    )
    return upcoming


def cleanup():
    # A3: überflüssiges "global tasks" entfernt (clear/update ändern das
    # bestehende Dict, keine Neuzuweisung)
    temp = {}
    for task_id, task in tasks.items():
        if not task["done"]:  # A3: benanntes Feld statt task[3]
            temp[task_id] = task
    if len(temp) == len(tasks):
        return
    tasks.clear()
    tasks.update(temp)


def get_task_count():
    return sum(1 for _ in tasks) if tasks else 0


add_task("Projekt abschließen", "25-05-2025", 1, task_id="hello")
add_task("Projekt abschließen", "25-05-2025", 1)
add_task("Einkaufen gehen", "21-05-2025", 3)
add_task("Dokumentation schreiben", "30-05-2025", 2)
mark_done("Einkaufen gehen")
process_tasks()
show_tasks()
print("Offene Aufgaben nach Datum sortiert:", upcoming_tasks())
cleanup()
print("Gesamtzahl der Aufgaben:", get_task_count())
