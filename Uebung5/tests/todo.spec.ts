import { expect, Page, test } from '@playwright/test';

const TODO_URL = 'https://demo.playwright.dev/todomvc/';

async function addTodo(page: Page, text: string) {
    const newTodoInput = page.getByPlaceholder('What needs to be done?');
    await newTodoInput.fill(text);
    await newTodoInput.press('Enter');
}

test.describe('TodoMVC Tests', () => {
    test.beforeEach(async ({ page }: { page: Page }) => {
        await page.goto(TODO_URL);
    });

    test.describe('1. Grundlegende Funktionen', () => {
        test('Ein neues Todo wird hinzugefügt', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Mein erstes Todo');
            await expect(page.getByText('Mein erstes Todo')).toBeVisible();
        });

        test('Mehrere Todos hinzufügen und Zähler prüfen', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Todo 1');
            await addTodo(page, 'Todo 2');
            await addTodo(page, 'Todo 3');

            await expect(page.getByTestId('todo-item')).toHaveCount(3);
            await expect(page.getByTestId('todo-count')).toContainText('3 items left');
        });

        test('Checkboxen setzen und Zähler aktualisieren', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Aufgabe A');
            await addTodo(page, 'Aufgabe B');

            const firstCheckbox = page.getByTestId('todo-item').nth(0).getByRole('checkbox');
            await firstCheckbox.check();

            await expect(firstCheckbox).toBeChecked();
            await expect(page.getByTestId('todo-count')).toContainText('1 item left');
        });
    });

    test.describe('2. Löschen & Toggle-All', () => {
        test('Todo via X (Hover) löschen', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Zu löschendes Todo');
            await addTodo(page, 'Bleibendes Todo');

            const firstTodo = page.getByTestId('todo-item').nth(0);
            await firstTodo.hover();
            await firstTodo.getByRole('button', { name: 'Delete' }).click();

            await expect(page.getByTestId('todo-item')).toHaveCount(1);
            await expect(page.getByText('Bleibendes Todo')).toBeVisible();
        });

        test('Toggle-All setzt alle Todos auf erledigt/nicht erledigt (inkl. Vorauswahl)', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Todo 1');
            await addTodo(page, 'Todo 2');

            const items = page.getByTestId('todo-item');
            const toggleAll = page.getByLabel('Mark all as complete');

            // Ein Todo vorab auswählen
            await items.nth(0).getByRole('checkbox').check();
            await expect(page.getByTestId('todo-count')).toContainText('1 item left');

            // Toggle-All aktiviert nun alle Todos
            await toggleAll.check();
            await expect(items.nth(0).getByRole('checkbox')).toBeChecked();
            await expect(items.nth(1).getByRole('checkbox')).toBeChecked();
            await expect(page.getByTestId('todo-count')).toContainText('0 items left');

            // Erneutes Toggle-All hebt die Auswahl für alle auf
            await toggleAll.uncheck();
            await expect(items.nth(0).getByRole('checkbox')).not.toBeChecked();
            await expect(items.nth(1).getByRole('checkbox')).not.toBeChecked();
            await expect(page.getByTestId('todo-count')).toContainText('2 items left');
        });

        test('Clear completed entfernt erledigte Todos', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Erledigtes Todo');
            await addTodo(page, 'Offenes Todo');

            await page.getByTestId('todo-item').nth(0).getByRole('checkbox').check();
            await page.getByRole('button', { name: 'Clear completed' }).click();

            await expect(page.getByTestId('todo-item')).toHaveCount(1);
            await expect(page.getByText('Offenes Todo')).toBeVisible();
        });
    });

    test.describe('3. Filter', () => {
        test('Active, Completed und All zeigen jeweils die richtigen Todos und Count', async ({ page }: { page: Page }) => {
            await addTodo(page, 'Todo 1');
            await addTodo(page, 'Todo 2');
            await addTodo(page, 'Todo 3');

            // Todo 1 als erledigt markieren
            await page.getByTestId('todo-item').nth(0).getByRole('checkbox').check();
            await expect(page.getByTestId('todo-count')).toContainText('2 items left');

            // Filter: Active
            await page.getByRole('link', { name: 'Active' }).click();
            await expect(page.getByTestId('todo-item')).toHaveCount(2);
            await expect(page.getByText('Todo 2')).toBeVisible();
            await expect(page.getByText('Todo 3')).toBeVisible();

            // Filter: Completed
            await page.getByRole('link', { name: 'Completed' }).click();
            await expect(page.getByTestId('todo-item')).toHaveCount(1);
            await expect(page.getByText('Todo 1')).toBeVisible();

            // Filter: All
            await page.getByRole('link', { name: 'All' }).click();
            await expect(page.getByTestId('todo-item')).toHaveCount(3);
            await expect(page.getByTestId('todo-count')).toContainText('2 items left');
        });
    });

    test.describe('4. Edge Cases', () => {
        test('Leere Eingabe (Enter ohne Text) fügt kein Todo hinzu', async ({ page }: { page: Page }) => {
            const newTodoInput = page.getByPlaceholder('What needs to be done?');
            await newTodoInput.press('Enter');

            await expect(page.getByTestId('todo-item')).toHaveCount(0);
        });

        test('Sehr langer Text wird korrekt dargestellt', async ({ page }: { page: Page }) => {
            const longText = 'Sehr langes Todo '.repeat(15).trim();
            await addTodo(page, longText);

            await expect(page.getByTestId('todo-item')).toHaveCount(1);
            await expect(page.getByText(longText)).toBeVisible();
        });

        test('Verhalten ohne Todos (Clear completed und Zähler nicht sichtbar)', async ({ page }: { page: Page }) => {
            await expect(page.getByRole('button', { name: 'Clear completed' })).toBeHidden();
            await expect(page.getByTestId('todo-count')).toBeHidden();
        });
    });
});