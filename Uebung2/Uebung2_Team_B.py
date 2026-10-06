# VRGA, NSBG

'''
Aufgabe 1 (Stellen, die das  Verständnis des Codes erschweren)

    Die vielen globalen Variablen machen den Code etwas unübersichtlich.

    Die Aufgaben werden als Listen gespeichert, dadurch ist nicht sofort klar was task[0], task[1] bedeutet.

    process_tasks() verändert zufällig eine Aufgabe, gibt aber immer False zurück.

    Die Funktion calculate_task_average() berechnet den Durchschnitt der Aufgaben-IDs und nicht wirklich einen Aufgabendurchschnitt.

    backup_tasks wird erstellt, aber später nicht verwendet.

    Die Datumswerte werden als Strings gespeichert und verglichen.


Aufgabe 2  
    Verbesserungen

        Die Aufgaben könnten statt als Listen besser als Dictionary oder eigene Klasse gespeichert werden.

        Weniger globale Variablen verwenden damit der Code übersichtlicher und leichter zu testen ist.

        Die Funktionen könnten besser dokumentiert werden.

        Die zufällige Vergabe der Aufgaben-ID kann zu Problemen führen da IDs doppelt vorkommen können.

        Bei leeren tasks kann process_tasks() einen Fehler verursachen.

        Die Datumswerte besser als echte Datumsobjekte speichern und nicht als Strings.

        Unbenutzte bzw. unnötige Sachen wie backup_tasks oder TODO entfernen.

        Bessere Namen für manche Variablen verwenden damit der Code verständlicher wird.

        Mehr Fehlerbehandlung einbauen z.B. wenn eine Aufgabe nicht existiert.


    Positiv:

        Der Code ist in mehrere Funktionen aufgeteilt und dadurch grundsätzlich übersichtlich.

        Die Funktionen haben meistens verständliche Namen.

        Die Aufgabenverwaltung ist grundsätzlich einfach aufgebaut und leicht nachzuvollziehen.


    Negativ:

        Viele globale Variablen machen den Code schwerer wartbar.

        Die Aufgaben als Listen zu speichern macht den Code weniger verständlich.

        Es gibt wenig Dokumentation und keine Kommentare bei den meisten Funktionen.

        Teilweise können Fehler auftreten z.B. bei leeren Aufgaben.
'''



import datetime
import random

# Änderung: tasks direkt als Dictionary initialisieren.
# Dadurch ist kein globales None und keine zusätzliche Prüfung nötig.
tasks = {}


def add_task(name, due_date, priority=3, task_id=None):
    global tasks

    # Änderung: "is None" ist die passendere Prüfung für None.
    if task_id is None:
        # Änderung: ID wird weiterhin zufällig erstellt, aber es wird
        # geprüft, ob die ID schon vorhanden ist.
        task_id = len(tasks) + random.randint(2, 7)
        while task_id in tasks:
            task_id += 1

    task = [name, due_date, priority, False, "user1",
            datetime.datetime.now().strftime("%d-%m-%Y %H:%M")]
    tasks[task_id] = task
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
            f"{task_id}: {task[0]} ({task[2]}) - bis {task[1]} - "
            f"{'Erledigt' if task[3] else 'Offen'}"
        )


def process_tasks():
    # Änderung: Prüfen, ob überhaupt Aufgaben vorhanden sind.
    # Sonst kann random.choice bei einer leeren Liste einen Fehler auslösen.
    if not tasks:
        return False

    rand_id = random.choice(list(tasks.keys()))
    tasks[rand_id][3] = not tasks[rand_id][3]
    return True  # Änderung: Die Funktion gibt jetzt zurück, ob etwas geändert wurde.


def calculate_task_average():
    if not tasks:
        return 0

    total = sum(tasks.keys())
    return total / len(tasks)


def upcoming_tasks():
    # Änderung: Datum als echtes Datum vergleichen statt als String.
    today = datetime.datetime.now().date()

    upcoming = sorted(
        [
            task for task in tasks.values()
            if datetime.datetime.strptime(task[1], "%d-%m-%Y").date() >= today
        ],
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
    return len(tasks)  # Änderung: einfacher und verständlicher als sum(1 for _ in tasks)


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
