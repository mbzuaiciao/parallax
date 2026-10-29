// @vitest-environment jsdom
import React from 'react';
import { afterEach, expect, test, vi } from 'vitest';
import { cleanup, render, screen, within, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App, { CaseView } from '../src/App';
import type { Case } from '../src/types';
import { execFileSync } from 'node:child_process';

// Real adapter output rather than a second invented financial fixture.
const cases: Case[] = JSON.parse(execFileSync('./.venv/bin/python', ['-c',
  'import json; from parallax.workstation import TICKERS, load_workstation_case; print(json.dumps([load_workstation_case(key) for key in TICKERS]))'],
  { cwd: '..', encoding: 'utf8' }));

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

function mockAPI() {
  vi.stubGlobal('fetch', vi.fn(async (path: string) => ({ ok: true, json: async () => path === '/api/cases'
    ? { cases } : cases.find(item => path.endsWith(item.key)) })));
}

test('all five cases load through selection with actual amounts and original SEC links', async () => {
  mockAPI();
  const user = userEvent.setup();
  render(<App />);
  for (const item of cases) {
    const nav = await screen.findByRole('navigation', { name: 'Disclosure cases' });
    await user.click(within(nav).getByRole('button', { name: new RegExp(item.company) }));
    await screen.findByRole('heading', { name: item.company, level: 1 });
    const table = screen.getByRole('table');
    for (const amount of item.amounts) {
      expect(within(table).getByText(amount.value!)).toBeTruthy();
      const row = within(table).getByText(amount.label).closest('tr')!;
      const doc = item.documents.find(doc => doc.id === amount.document_id)!;
      expect(within(row).getByRole('link').getAttribute('href')).toBe(doc.url);
    }
    expect(screen.getByText(/Existing AI-assisted research reference/).textContent).toContain('independent human approval pending');
    for (const doc of item.documents) expect(screen.getByRole('heading', { name: doc.title! })).toBeTruthy();
  }
});

test('perspective switches reproduce existing conditional reference text', async () => {
  const user = userEvent.setup();
  render(<CaseView data={cases[0]} />);
  expect(screen.getByText(cases[0].interpretations.equity!)).toBeTruthy();
  await user.click(screen.getByRole('button', { name: 'Senior unsecured creditor' }));
  expect(screen.getByText(cases[0].interpretations.senior_unsecured_creditor!)).toBeTruthy();
  expect(screen.getByRole('button', { name: 'Senior unsecured creditor' }).getAttribute('aria-pressed')).toBe('true');
});

test('unknown amounts and missing fields stay explicitly unavailable', () => {
  const missing: Case = { ...cases[1], documents: [{ id: 'MISSING' }],
    amounts: [{ label: 'Missing amount', value: null, document_id: null, context: '', status: 'unavailable' }],
    accounting: { status: 'unavailable' }, interpretations: {}, limitations: [] };
  const { container } = render(<CaseView data={missing} />);
  expect(screen.getByRole('table').textContent).toContain('Unavailable in supplied evidence');
  expect(container.textContent).not.toContain('$0');
  expect(screen.queryByRole('link')).toBeNull();
  expect(screen.getByText('Interpretation unavailable in the existing reference.')).toBeTruthy();
  expect(screen.getByText('Accounting information unavailable')).toBeTruthy();
});

test('unknown accounting is distinct from disclosed contractual amounts', () => {
  render(<CaseView data={cases[1]} />);
  expect(screen.getByText('Carrying amount unknown')).toBeTruthy();
  expect(screen.getByRole('table').textContent).toContain('$14.72 billion');
  expect(screen.getByText(/Missing evidence is never represented as zero/)).toBeTruthy();
});

test('search supports ticker, empty state and clearing', async () => {
  mockAPI();
  const user = userEvent.setup();
  render(<App />);
  await screen.findByRole('heading', { name: 'NVIDIA', level: 1 });
  const search = screen.getByRole('searchbox');
  await user.type(search, 'AAPL');
  const nav = screen.getByRole('navigation', { name: 'Disclosure cases' });
  expect(within(nav).getAllByRole('button')).toHaveLength(1);
  await user.clear(search); await user.type(search, 'uncovered');
  expect(screen.getByRole('status').textContent).toContain('No matching cases');
  await user.clear(search);
  expect(within(nav).getAllByRole('button')).toHaveLength(5);
});

test('service failure offers a working retry', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false })));
  const user = userEvent.setup();
  render(<App />);
  await screen.findByRole('alert');
  mockAPI();
  await user.click(screen.getByRole('button', { name: 'Retry loading' }));
  await screen.findByRole('heading', { name: 'NVIDIA', level: 1 });
});

test('late case responses cannot overwrite the newly selected case', async () => {
  let finishOld: (value: unknown) => void = () => {};
  vi.stubGlobal('fetch', vi.fn((path: string) => {
    if (path === '/api/cases') return Promise.resolve({ ok: true, json: async () => ({ cases }) });
    if (path.endsWith('nvidia-ports')) return new Promise(resolve => { finishOld = resolve; });
    return Promise.resolve({ ok: true, json: async () => cases[3] });
  }));
  const user = userEvent.setup();
  render(<App />);
  await user.click(await screen.findByRole('button', { name: /Apple/ }));
  await screen.findByRole('heading', { name: 'Apple', level: 1 });
  finishOld({ ok: true, json: async () => cases[0] });
  await waitFor(() => expect(screen.queryByRole('heading', { name: 'NVIDIA', level: 1 })).toBeNull());
});
