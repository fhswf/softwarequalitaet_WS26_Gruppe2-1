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
from typing import Any

# A3: Typ-Aliase für Type Hints - eine Aufgabe ist ein dict mit benannten
# Feldern, IDs sind int (automatisch vergeben) oder str (von außen übergeben)
TaskId = int | str
Task = dict[str, Any]

# A3: Konstanten statt Magic Values - Formate und Defaults an einer Stelle
DATE_FORMAT = "%d-%m-%Y"                 # Fälligkeitsdatum, z. B. "25-05-2025"
DATETIME_FORMAT = "%d-%m-%Y %H:%M"       # Erstellzeitpunkt einer Aufgabe
DEFAULT_USER = "user1"                   # Benutzer, falls keiner übergeben wird
# Prioritäts-Skala: 1 = hoch, 2 = mittel, 3 = niedrig
MIN_PRIORITY = 1                         # A3: Grenzen für die Eingabeprüfung
MAX_PRIORITY = 3
# A3: Default von 3 (niedrig) auf 2 (mittel) geändert - eine Aufgabe ohne
# Angabe soll nicht automatisch die niedrigste Priorität bekommen
DEFAULT_PRIORITY = 2

# A3: tasks direkt als leeres Dict initialisiert (statt None + Lazy-Init in
# add_task) -> alle Funktionen funktionieren auch ohne vorheriges add_task
tasks: dict[TaskId, Task] = {}
# A3: backup_tasks entfernt - wurde nirgends gelesen, war kein echtes Backup
# (gleiche Objekt-Referenzen, Änderungen schlugen durch) und wurde bei
# remove_task nicht gepflegt -> nur toter, irreführender Code


# A3: Default-Priorität als Konstante, Benutzer als Parameter "user" statt
# fest "user1" (neuer Parameter am Ende -> bestehende Aufrufe bleiben gültig)
# A3: Docstrings und Type Hints für alle Funktionen ergänzt
def add_task(name: str, due_date: str, priority: int = DEFAULT_PRIORITY,
             task_id: TaskId | None = None, user: str = DEFAULT_USER) -> TaskId:
    """Legt eine neue, offene Aufgabe an.

    Args:
        name: Bezeichnung der Aufgabe.
        due_date: Fälligkeitsdatum im Format TT-MM-JJJJ.
        priority: 1 = hoch, 2 = mittel, 3 = niedrig.
        task_id: Optionale eigene ID; ohne Angabe wird eine freie ID vergeben.
        user: Benutzer, dem die Aufgabe gehört.

    Returns:
        Die ID der angelegten Aufgabe.

    Raises:
        ValueError: Bei ungültigem Datum, ungültiger Priorität oder
            bereits vergebener task_id.
    """
    # A3: "global" entfernt - tasks wird nur verändert,
    # nicht neu zugewiesen; Lazy-Init entfällt (siehe oben)

    # A3: Eingabevalidierung vor allen anderen Schritten, damit bei
    # ungültigen Werten nichts angelegt wird
    try:
        # A3: Fälligkeitsdatum als datetime.date speichern statt als String
        # -> korrekte Datumsvergleiche und Sortierung möglich
        due_date = datetime.datetime.strptime(due_date, DATE_FORMAT).date()
    except ValueError:
        raise ValueError(f"Ungültiges Datum {due_date!r}, "
                         f"erwartet TT-MM-JJJJ") from None
    if not isinstance(priority, int) or not MIN_PRIORITY <= priority <= MAX_PRIORITY:
        raise ValueError(f"Ungültige Priorität {priority!r}, "
                         f"erlaubt {MIN_PRIORITY}-{MAX_PRIORITY}")

    if task_id is None:  # A3: "is None" statt "== None" (PEP 8)
        task_id = len(tasks) + random.randint(2, 7)  # Wichtig! Nicht verändern!
        # A3: ID-Kollision verhindern - die Zufalls-ID kann bereits vergeben
        # sein und hätte die bestehende Aufgabe still überschrieben; daher
        # bis zur nächsten freien ID hochzählen (Zeile oben bleibt unverändert)
        while task_id in tasks:
            task_id += 1
    elif task_id in tasks:
        # A3: von außen übergebene, bereits vergebene ID führt zu einem klaren
        # Fehler statt eine bestehende Aufgabe still zu überschreiben
        raise ValueError(f"Aufgaben-ID {task_id!r} ist bereits vergeben")
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
    tasks[task_id] = task  # A3: backup_tasks entfällt (siehe oben)
    return task_id


def remove_task(task_id: TaskId) -> bool:
    """Löscht die Aufgabe mit der ID; False, wenn die ID unbekannt ist."""
    # A3: überflüssiges "global tasks" entfernt
    if task_id in tasks:
        del tasks[task_id]
        return True
    return False


# A3: mark_done arbeitet über die eindeutige ID statt über den Namen
# (Namen können doppelt vorkommen -> es wurden alle Duplikate markiert);
# Rückgabe True/False statt immer "Erledigt", auch wenn nichts gefunden wurde
def mark_done(task_id: TaskId) -> bool:
    """Markiert die Aufgabe als erledigt; False, wenn die ID unbekannt ist."""
    if task_id not in tasks:
        return False
    tasks[task_id]["done"] = True
    return True


def show_tasks() -> None:
    """Gibt alle Aufgaben mit Priorität, Fälligkeit und Status aus."""
    # A3: überflüssiges "global tasks" entfernt
    for task_id, task in tasks.items():
        # A3: benannte Felder statt Indizes, Status vorab berechnet (lesbarer)
        status = "Erledigt" if task["done"] else "Offen"
        # A3: due_date ist jetzt ein date -> für die Ausgabe formatieren
        due = task["due_date"].strftime(DATE_FORMAT)
        print(f"{task_id}: {task['name']} ({task['priority']}) - "
              f"bis {due} - {status}")


# A3: process_tasks durch toggle_task ersetzt - statt eine ZUFÄLLIGE Aufgabe
# umzuschalten (nicht nachvollziehbar, Absturz bei leerer Liste, immer
# False, leeres TODO) wird gezielt die Aufgabe mit der übergebenen ID
# umgeschaltet; Rückgabe zeigt, ob die Aufgabe gefunden wurde
def toggle_task(task_id: TaskId) -> bool:
    """Schaltet offen/erledigt um; False, wenn die ID unbekannt ist."""
    if task_id not in tasks:
        return False
    tasks[task_id]["done"] = not tasks[task_id]["done"]
    return True


# A3: calculate_task_average -> calculate_average_priority - der
# Durchschnitt der IDs war fachlich sinnlos (und stürzte bei String-IDs ab),
# die durchschnittliche Priorität ist eine aussagekräftige Kennzahl
def calculate_average_priority() -> float:
    """Liefert die durchschnittliche Priorität aller Aufgaben (0.0 wenn leer)."""
    if not tasks:
        return 0.0
    total = sum(task["priority"] for task in tasks.values())
    return total / len(tasks)


def upcoming_tasks() -> list[Task]:
    """Liefert offene Aufgaben ab heute, sortiert nach Fälligkeit und Priorität."""
    # A3: due_date ist jetzt ein date -> mit date.today() statt mit einem
    # String vergleichen ("TT-MM-JJJJ" als String sortiert falsch)
    today = datetime.date.today()
    # A3: nur OFFENE Aufgaben (vorher auch erledigte), sortiert nach
    # Fälligkeit statt nach Name; bei gleichem Datum höhere Priorität zuerst
    upcoming = sorted(
        [task for task in tasks.values()
         if not task["done"] and task["due_date"] >= today],
        key=lambda task: (task["due_date"], task["priority"])
    )
    return upcoming


# A3: cleanup -> remove_done_tasks - Name sagt jetzt, was gelöscht wird;
# Hilfs-Dict, clear/update und Sonderfall-return durch eine Liste der zu
# löschenden IDs ersetzt; Rückgabe = Anzahl gelöschter Aufgaben
def remove_done_tasks() -> int:
    """Löscht alle erledigten Aufgaben und liefert deren Anzahl."""
    done_ids = [task_id for task_id, task in tasks.items() if task["done"]]
    for task_id in done_ids:
        del tasks[task_id]
    return len(done_ids)


def get_task_count() -> int:
    """Liefert die Anzahl aller Aufgaben."""
    return len(tasks)  # A3: len() statt sum(1 for _ in tasks) + Sonderfall


def days_from_today(days: int) -> str:
    """Liefert das Datum in `days` Tagen im Format TT-MM-JJJJ."""
    # A3: Hilfsfunktion für die Demo - relative Daten, damit upcoming_tasks
    # unabhängig vom Ausführungstag immer etwas anzeigt
    return (datetime.date.today() + datetime.timedelta(days=days)).strftime(DATE_FORMAT)


def main() -> None:
    """Demonstriert die Aufgabenverwaltung mit Beispieldaten."""
    # A3: Demo-Aufrufe in main() gekapselt und per Main-Guard (unten) nur
    # beim direkten Ausführen gestartet - beim Import passiert nichts
    add_task("Projekt abschließen", "25-05-2025", 1, task_id="hello")
    add_task("Projekt abschließen", "25-05-2025", 1)
    # A3: IDs merken, damit mark_done/toggle_task gezielt aufgerufen werden können
    shopping_id = add_task("Einkaufen gehen", "21-05-2025", 3)
    doc_id = add_task("Dokumentation schreiben", "30-05-2025", 2)
    # A3: Aufgaben in der Zukunft ergänzt, damit upcoming_tasks etwas liefert
    add_task("Präsentation vorbereiten", days_from_today(14), 1)
    add_task("Code-Review Team A", days_from_today(3), 2, user="BNWK")
    pylint_id = add_task("Pylint ausführen", days_from_today(3))
    add_task("Abgabe per Mail", days_from_today(3), 1)

    mark_done(shopping_id)  # A3: über ID statt Name
    mark_done(pylint_id)
    toggle_task(doc_id)  # A3: ersetzt process_tasks()
    show_tasks()
    print("Durchschnittliche Priorität:", calculate_average_priority())  # A3

    # A3: lesbare Ausgabe statt roher dicts
    print("Offene Aufgaben nach Datum sortiert:")
    for task in upcoming_tasks():
        print(f"  {task['due_date'].strftime(DATE_FORMAT)} "
              f"(Prio {task['priority']}): {task['name']}")

    print("Gelöschte erledigte Aufgaben:", remove_done_tasks())  # A3: umbenannt
    print("Gesamtzahl der Aufgaben:", get_task_count())


if __name__ == "__main__":
    main()
