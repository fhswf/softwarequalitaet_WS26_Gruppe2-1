# Übung 5: End-to-End-Testing mit Playwright

In dieser Übung lernen Sie, wie man moderne Webanwendungen mithilfe von **Playwright** automatisiert testet. Im ersten Teil (Abschnitte 1–4) richten Sie die Testumgebung ein und lernen die Werkzeuge kennen. Im zweiten Teil (Abschnitt 5) bearbeiten Sie drei praktische Testaufgaben.

## Inhaltsverzeichnis

1. [Umgebung starten (Docker / Codespaces & Lokal)](#1-umgebung-starten-docker--codespaces--lokal)
2. [Tests aufzeichnen mit Playwright CodeGen](#2-tests-aufzeichnen-mit-playwright-codegen)
3. [Tests manuell programmieren (Kurzreferenz)](#3-tests-manuell-programmieren-kurzreferenz)
4. [Tests ausführen und auswerten](#4-tests-ausführen-und-auswerten)
5. [Praktische Aufgaben](#5-praktische-aufgaben)

---

## 1. Umgebung starten (Docker / Codespaces & Lokal)

### Option A: Start über den Docker-Container (Empfohlen)

Für diese Übung steht eine fertige Desktop-Umgebung (XFCE + noVNC) mit vorinstalliertem Playwright und allen Browsern bereit.

1. Öffnen Sie ein Terminal und wechseln Sie in das Verzeichnis `Uebung5`:
   ~~~bash
   cd Uebung5
   ~~~

2. Starten Sie den Container mit einem der beiden Skripte:
   * **Schnellstart (lädt das fertige Image direkt aus der GitHub Registry):**
     ~~~bash
     ./run.sh
     ~~~
   * **Lokal bauen und starten (nur nötig bei eigenen Änderungen am `Dockerfile`):**
     ~~~bash
     ./build-run.sh
     ~~~

3. Öffnen Sie die grafische Desktop-Oberfläche im Browser:
   * **In GitHub Codespaces:** Klicken Sie unten im Terminal-Bereich auf den Reiter **Ports**, suchen Sie den Port **6080** und klicken Sie auf das **Weltkugel-Symbol (Open in Browser)**.
   * **Lokal auf dem eigenen PC:** Öffnen Sie `http://localhost:6080` in Ihrem Browser.

4. **Wichtiger Hinweis zu Ihren Dateien:**
   Auf dem Desktop arbeiten Sie im Verzeichnis `/workspace`. Alle Testdateien, die Sie dort im Unterordner `/workspace/tests` anlegen oder bearbeiten, werden automatisch mit Ihrem Ordner `Uebung5/tests` synchronisiert.

5. **Beenden:** Drücken Sie im Terminal von Schritt 2 einmal `Ctrl + C`, um den Container zu stoppen.

### Option B: Lokale Installation ohne Docker (Optional)

Falls Sie Playwright ohne Docker direkt auf Ihrem Rechner nutzen möchten (Node.js erforderlich), folgen Sie der offiziellen Dokumentation unter https://playwright.dev/docs/intro oder führen Sie folgenden Befehl im Ordner `Uebung5` aus:

~~~bash
npm init playwright@latest
~~~

---

## 2. Tests aufzeichnen mit Playwright CodeGen

Mit dem Werkzeug **CodeGen** führen Sie Klicks und Texteingaben direkt im Browser aus, während Playwright im Hintergrund automatisch den passenden TypeScript-Testcode generiert.

### Schritt 1: CodeGen starten

Starten Sie CodeGen innerhalb der Desktop-Umgebung (Port `6080`) über eine der beiden Möglichkeiten:

* **Per Desktop-Verknüpfung:** Doppelklicken Sie auf dem Desktop auf das Symbol **Playwright Codegen**.
* **Per Terminal:** Doppelklicken Sie auf dem Desktop auf **Workspace Terminal** und führen Sie diesen Befehl aus:
  ~~~bash
  npx playwright codegen https://demo.playwright.dev/todomvc/
  ~~~

### Schritt 2: Interaktionen und Überprüfungen (Assertions) aufzeichnen

1. Es öffnen sich zwei Fenster nebeneinander: links der **Chromium-Browser** mit der TodoMVC-Anwendung und rechts der **Playwright Inspector**.
2. Führen Sie im Browser Aktionen aus (z. B. Text eingeben und `Enter` drücken). Jeder Schritt erscheint sofort als Code im Inspector.
3. **Assertions über die Werkzeugleiste hinzufügen:** Nutzen Sie die Symbole oben im Browserfenster (oder im Inspector), um Bedingungen zu prüfen:
   * **Assert visibility (Augen-Symbol):** Prüft, ob ein Element auf der Seite sichtbar ist.
   * **Assert text (`ab`-Symbol):** Prüft, ob ein Element einen bestimmten Text enthält.
   * **Assert value:** Prüft den aktuellen Wert eines Eingabefelds.
4. Klicken Sie oben auf den roten Punkt (**Record**), um die Aufzeichnung zu beenden.
5. Klicken Sie im Inspector auf **Copy** und fügen Sie den Code in eine neue Datei unter `Uebung5/tests/` ein.

---

## 3. Tests manuell programmieren (Kurzreferenz)

Alle Testdateien liegen im Ordner `tests/` und enden auf `.spec.ts` (z. B. `tests/todo.spec.ts`). Sie können diese Dateien bequem direkt in Ihrem VS Code Editor unter `Uebung5/tests/` erstellen und bearbeiten.

### Grundaufbau einer Testdatei

~~~typescript
import { test, expect } from '@playwright/test';

test.describe('TodoMVC Beispieltests', () => {
  // Wird automatisch vor jedem einzelnen Test ausgeführt
  test.beforeEach(async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc/');
  });

  test('Neues Todo anlegen und in der Liste prüfen', async ({ page }) => {
    // 1. Eingabefeld finden (Locator) und Text eingeben (Action)
    const input = page.getByPlaceholder('What needs to be done?');
    await input.fill('Softwarequalität Übung 5 bearbeiten');
    await input.press('Enter');

    // 2. Ergebnis überprüfen (Assertion)
    await expect(page.getByTestId('todo-title')).toHaveText([
      'Softwarequalität Übung 5 bearbeiten'
    ]);
  });
});
~~~

### Wichtige Playwright-Befehle im Überblick

* **Elemente finden (Locators):**
  * `page.getByPlaceholder('What needs to be done?')` – findet Eingabefelder über den Platzhalter.
  * `page.getByTestId('todo-title')` – findet Elemente über das Attribut `data-testid`.
  * `page.getByRole('link', { name: 'Active' })` – findet Links, Buttons oder Checkboxen anhand ihrer Rolle.
  * `page.getByText('1 item left')` – findet Elemente anhand ihres sichtbaren Textes.
* **Aktionen ausführen (Interactions):**
  * `await locator.fill('Text')` – trägt Text in ein Eingabefeld ein.
  * `await locator.press('Enter')` – simuliert einen Tastendruck (z. B. `Enter` oder `Escape`).
  * `await locator.click()` / `await locator.dblclick()` – einfacher Klick / Doppelklick.
  * `await locator.check()` / `await locator.uncheck()` – setzt oder entfernt den Haken einer Checkbox.
  * `await locator.hover()` – bewegt den Mauszeiger über ein Element (wichtig für Hover-Buttons).
* **Ergebnisse prüfen (Assertions):**
  * `await expect(locator).toBeVisible()` / `await expect(locator).toBeHidden()` – prüft Sichtbarkeit.
  * `await expect(locator).toHaveText('...')` – prüft auf exakten Text (oder ein Array von Texten).
  * `await expect(locator).toHaveCount(2)` – prüft die genaue Anzahl gefundener Elemente.
  * `await expect(locator).toHaveClass(/completed/)` – prüft, ob ein Element eine bestimmte CSS-Klasse besitzt.

---

## 4. Tests ausführen und auswerten

### Option A: Interaktiv über die Playwright Test UI (Empfohlen zur Fehlersuche)

1. Doppelklicken Sie auf dem VNC-Desktop auf **Playwright Test UI** (oder starten Sie im Workspace Terminal `npx playwright test --ui`).
2. Klicken Sie in der linken Seitenleiste neben Ihrer Testdatei oder einem einzelnen Test auf das **Play-Symbol (▶)**.
3. Klicken Sie oben auf der Zeitleiste durch die einzelnen Schritte, um den genauen Zustand der Webseite vor und nach jeder Aktion zu inspizieren.

### Option B: Über das Terminal (Kommandozeile)

Öffnen Sie das **Workspace Terminal** auf dem Desktop und nutzen Sie folgende Befehle:

* **Alle Tests ausführen:**
  ~~~bash
  npx playwright test
  ~~~
* **Nur eine bestimmte Testdatei ausführen:**
  ~~~bash
  npx playwright test tests/manual-todo.spec.ts
  ~~~
* **Grafischen HTML-Testbericht öffnen:**
  ~~~bash
  npx playwright show-report
  ~~~

---

## 5. Praktische Aufgaben

Bearbeiten Sie die folgenden drei Aufgaben für die Webanwendung `https://demo.playwright.dev/todomvc/`. Speichern Sie alle Lösungen im Ordner `Uebung5/tests/`.

---

### Aufgabe 1: Einfachen Testablauf mit CodeGen aufzeichnen

Erstellen Sie Ihren ersten automatisierten Test mithilfe des Code-Generators:

1. Starten Sie **Playwright Codegen** für die URL `https://demo.playwright.dev/todomvc/`.
2. Zeichnen Sie genau folgenden Ablauf auf:
   * Fügen Sie **zwei neue Todo-Einträge** hinzu (z. B. `"Einkaufen"` und `"Lernen"`).
   * Haken Sie das erste Todo über die Checkbox als **erledigt** ab.
   * Prüfen Sie über das Werkzeug **Assert text**, dass unten links der Text `1 item left` angezeigt wird.
   * Prüfen Sie über das Werkzeug **Assert visibility**, dass unten rechts der Button `Clear completed` sichtbar ist.
3. Kopieren Sie den generierten Code in eine neue Datei `tests/codegen-todo.spec.ts`.
4. Führen Sie den Test in der **Playwright Test UI** aus und stellen Sie sicher, dass er erfolgreich durchläuft.

---

### Aufgabe 2: Kernfunktionen manuell implementieren

Erstellen Sie eine neue Datei `tests/manual-todo.spec.ts` und programmieren Sie die folgenden drei Testszenarien **manuell** (nutzen Sie `test.beforeEach`, um vor jedem Test die Startseite zu öffnen):

1. **Filter-Logik überprüfen (`All`, `Active`, `Completed`):**
   * Legen Sie drei Todos an und markieren Sie eines davon als erledigt.
   * Klicken Sie unten auf den Filter-Link `Active` und prüfen Sie mit `toHaveCount(2)`, dass nur die zwei offenen Einträge angezeigt werden.
   * Klicken Sie auf `Completed` und prüfen Sie, dass genau ein Eintrag sichtbar ist (`toHaveCount(1)`).
   * Klicken Sie auf `All` und verifizieren Sie, dass wieder alle drei Einträge angezeigt werden (`toHaveCount(3)`).

2. **Todo nachträglich bearbeiten & Bearbeitung mit `Escape` abbrechen:**
   * Legen Sie ein Todo an und führen Sie einen Doppelklick auf den Titel aus (`await locator.dblclick()`).
   * Ändern Sie den Text im Bearbeitungsfeld, bestätigen Sie mit `Enter` und prüfen Sie per Assertion, dass der neue Text übernommen wurde.
   * Doppelklicken Sie erneut auf denselben Eintrag, tippen Sie einen anderen Text ein, aber brechen Sie diesmal mit der Taste `Escape` ab. Prüfen Sie, dass die Änderung verworfen wurde und der vorherige Text erhalten bleibt.

3. **Erledigte Todos löschen (`Clear completed`) & Seiten-Reload testen:**
   * Legen Sie zwei Todos an, markieren Sie eines als erledigt und klicken Sie auf den Button `Clear completed`.
   * Laden Sie die Seite über `await page.reload()` neu.
   * Überprüfen Sie, dass das gelöschte Todo auch nach dem Neuladen verschwunden bleibt und nur noch das offene Todo in der Liste steht.

---

### Aufgabe 3: Fortgeschrittene E2E-Szenarien & Edge-Cases

Erstellen Sie eine weitere Datei `tests/advanced-todo.spec.ts` und implementieren Sie die folgenden vier fortgeschrittenen Testfälle:

1. **Abweisung leerer Eingaben (Edge-Case):**
   * Drücken Sie im leeren Eingabefeld direkt `Enter` und versuchen Sie anschließend, ein Todo bestehend aus reinen Leerzeichen (`"   "`) einzugeben.
   * Prüfen Sie, dass keine Einträge in der Liste erzeugt werden (`toHaveCount(0)`) und die Fußzeile der Liste ausgeblendet bleibt (`toBeHidden()`).

2. **„Alle markieren"-Funktion (`Toggle All`) & Zähler-Synchronisation:**
   * Legen Sie drei Todos an und klicken Sie auf das Pfeil-Symbol links neben dem Eingabefeld (`Mark all as complete`), um alle Einträge gleichzeitig abzuhaken.
   * Prüfen Sie, dass der Zähler `0 items left` anzeigt und alle Listenelemente (`page.getByTestId('todo-item')`) die CSS-Klasse `completed` besitzen (`toHaveClass(/completed/)`).
   * Klicken Sie erneut auf `Mark all as complete` und prüfen Sie, dass wieder `3 items left` angezeigt wird.

3. **Einzelnes Todo über das Hover-Symbol (`×`) löschen:**
   * Das rote Lösch-Kreuz (`×`) rechts neben einem Eintrag erscheint erst, wenn sich der Mauszeiger über dem Todo befindet.
   * Legen Sie ein Todo an, bewegen Sie die Maus mit `await todoItem.hover()` darüber, klicken Sie auf den erscheinenden Button (`getByRole('button', { name: 'Delete' })`) und verifizieren Sie, dass die Liste danach leer ist.

4. **Datenpersistenz im `localStorage` überprüfen:**
   * Fügen Sie zwei Todos hinzu und markieren Sie das erste als erledigt.
   * Lesen Sie den Browser-Speicher im Test aus:
     ~~~typescript
     const storedData = await page.evaluate(() => localStorage.getItem('react-todos'));
     const todos = JSON.parse(storedData ?? '[]');
     ~~~
   * Prüfen Sie mit `expect(todos).toHaveLength(2)` sowie `expect(todos[0].completed).toBe(true)`, dass die Daten korrekt im Browser gespeichert wurden.
