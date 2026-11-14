// VRGA, NSBG

import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc/#/');
});

test('Filter-Logik: All, Active und Completed', async ({ page }) => {
    const newTodo = page.getByRole('textbox', { name: 'What needs to be done?' });
    const todos = page.locator('.todo-list li');

    // Drei Todos anlegen
    await newTodo.fill('Einkaufen');
    await newTodo.press('Enter');

    await newTodo.fill('Lernen');
    await newTodo.press('Enter');

    await newTodo.fill('Sport');
    await newTodo.press('Enter');

    // Ein Todo als erledigt markieren
    await todos.filter({ hasText: 'Lernen' }).locator('.toggle').check();

    // Nur die zwei offenen Todos
    await page.getByRole('link', { name: 'Active' }).click();
    await expect(todos).toHaveCount(2);
    await expect(todos.filter({ hasText: 'Lernen' })).toHaveCount(0);

    // Nur das erledigte Todo
    await page.getByRole('link', { name: 'Completed' }).click();
    await expect(todos).toHaveCount(1);
    await expect(todos.filter({ hasText: 'Lernen' })).toHaveCount(1);

    // Wieder alle drei Todos
    await page.getByRole('link', { name: 'All' }).click();
    await expect(todos).toHaveCount(3);
});

test('Todo bearbeiten und Bearbeitung mit Escape abbrechen', async ({ page }) => {
    const newTodo = page.getByRole('textbox', { name: 'What needs to be done?' });

    await newTodo.fill('Alter Text');
    await newTodo.press('Enter');

    const alterTodo = page
        .locator('.todo-list li')
        .filter({ hasText: 'Alter Text' });

    // Bearbeiten und speichern
    await alterTodo.locator('label').dblclick();
    await alterTodo.locator('.edit').fill('Neuer Text');
    await alterTodo.locator('.edit').press('Enter');

    const neuesTodo = page
        .locator('.todo-list li')
        .filter({ hasText: 'Neuer Text' });

    await expect(neuesTodo).toHaveCount(1);

    // Erneut bearbeiten, dann mit Escape abbrechen
    await neuesTodo.locator('label').dblclick();
    await neuesTodo.locator('.edit').fill('Soll nicht gespeichert werden');
    await neuesTodo.locator('.edit').press('Escape');

    await expect(neuesTodo).toHaveCount(1);
    await expect(
        page.locator('.todo-list li').filter({ hasText: 'Soll nicht gespeichert werden' })
    ).toHaveCount(0);
});

test('Erledigtes Todo löschen und nach Reload prüfen', async ({ page }) => {
    const newTodo = page.getByRole('textbox', { name: 'What needs to be done?' });
    const todos = page.locator('.todo-list li');

    await newTodo.fill('Offenes Todo');
    await newTodo.press('Enter');

    await newTodo.fill('Erledigtes Todo');
    await newTodo.press('Enter');

    await todos.filter({ hasText: 'Erledigtes Todo' }).locator('.toggle').check();

    await page.getByRole('button', { name: 'Clear completed' }).click();

    // Nach dem Reload weiterhin gelöscht
    await page.reload();

    await expect(todos).toHaveCount(1);
    await expect(todos.filter({ hasText: 'Offenes Todo' })).toHaveCount(1);
    await expect(todos.filter({ hasText: 'Erledigtes Todo' })).toHaveCount(0);
});