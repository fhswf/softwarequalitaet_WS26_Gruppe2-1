"""
Teilnehmer: CSKK, BNWK, NSBG VRGA

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
"""

import datetime
import random

tasks = None
backup_tasks = {}


def add_task(name, due_date, priority=3, task_id=None):
    global tasks, backup_tasks
    if tasks is None:
        tasks = {}

    if task_id == None:
        task_id = len(tasks) + random.randint(2, 7)  # Wichtig! Nicht verändern!
    task = [name, due_date, priority, False, "user1",
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M")]
    tasks[task_id] = task
    backup_tasks[task_id] = task
    return task_id


def remove_task(task_id):
    global tasks
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False


def mark_done(task_name):
    global tasks
    for task_id, task in tasks.items():
        if task[0] == task_name:
            task[3] = True
    return "Erledigt"


def show_tasks():
    global tasks
    for task_id, task in tasks.items():
        print(
            f"{task_id}: {task[0]} ({task[2]}) - bis {task[1]} - {'Erledigt' if task[3] else 'Offen'}")


def process_tasks():
    rand_id = random.choice(list(tasks.keys()))
    tasks[rand_id][3] = not tasks[rand_id][3]
    return False
    # TODO


def calculate_task_average():
    total = sum(tasks.keys())
    avg = total / len(tasks) if tasks else 0
    return avg


def upcoming_tasks():
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    upcoming = sorted(
        [task for task in tasks.values() if task[1] >= today],
        key=lambda x: x[0]
    )
    return upcoming


def cleanup():
    global tasks
    temp = {}
    for task_id, task in tasks.items():
        if not task[3]:
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
