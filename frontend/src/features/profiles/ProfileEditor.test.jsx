import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, afterEach, test, expect, vi } from 'vitest';
import ProfileEditor from './ProfileEditor';
import { setSession, clearSession } from '../auth/session';

const records = {
  employees: { id: 'employee-id', employee_number: 'E-1', name: 'Alex', current_title: 'Technician', status: 'ACTIVE', total_years_experience: 5, version: 4, skills: [{skill_id: 'electrical', proficiency: 3, years_experience: 2, last_used_on: null}], certifications: [] },
  jobs: { id: 'job-id', job_code: 'J-1', title: 'Technician', description: 'Maintain equipment', status: 'OPEN', minimum_years_experience: 3, version: 7, skill_requirements: [{skill_id: 'electrical', level: 'REQUIRED', minimum_proficiency: 3, importance: 2}], certification_requirements: [] },
};
const reply = (body, status = 200) => new Response(JSON.stringify(body), { status });
beforeEach(() => { setSession({ access_token: 'test-token', token_type: 'bearer', expires_in: 900 }); vi.stubGlobal('fetch', vi.fn()); });
afterEach(() => { clearSession(); vi.unstubAllGlobals(); });

for (const kind of ['employees', 'jobs']) {
  test(`${kind}: PUT sends the server version and complete editable profile`, async () => {
    const record = records[kind];
    fetch.mockResolvedValueOnce(reply(record)).mockResolvedValueOnce(reply({...record, version: record.version + 1}));
    render(<ProfileEditor kind={kind} recordId={record.id} onSaved={vi.fn()} onCancel={vi.fn()} />);
    await screen.findByDisplayValue(kind === 'employees' ? 'Alex' : 'Technician');
    await userEvent.click(screen.getByRole('button', { name: 'Save changes' }));
    await screen.findByRole('status');
    const request = fetch.mock.calls.find(([, options]) => options.method === 'PUT');
    const {id, ...expected} = record;
    expect(request[0]).toBe(`/api/v1/${kind}/${record.id}`);
    expect(JSON.parse(request[1].body)).toEqual(expected);
    expect(request[1].headers.get('Authorization')).toBe('Bearer test-token');
  });

  test(`${kind}: stale conflicts retain drafts and require explicit reload`, async () => {
    const record = records[kind];
    fetch.mockResolvedValueOnce(reply(record)).mockResolvedValueOnce(reply({code: 'STALE_VERSION', detail: 'private detail', request_id: 'trace-1'}, 409))
      .mockResolvedValueOnce(reply({...record, version: record.version + 2}));
    render(<ProfileEditor kind={kind} recordId={record.id} onSaved={vi.fn()} onCancel={vi.fn()} />);
    const name = await screen.findByLabelText(kind === 'employees' ? 'Name' : 'Title');
    await userEvent.clear(name); await userEvent.type(name, 'My draft');
    await userEvent.click(screen.getByRole('button', { name: 'Save changes' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Someone else updated this profile');
    expect(name).toHaveValue('My draft');
    expect(screen.queryByText('private detail')).not.toBeInTheDocument();
    expect(screen.getByRole('button', {name: 'Save changes'})).toBeDisabled();
    expect(fetch.mock.calls.filter(([, options]) => options.method === 'PUT')).toHaveLength(1);
    await userEvent.click(screen.getByRole('button', {name: 'Reload latest version'}));
    await screen.findByText('Reloading will replace your unsaved changes.');
    await userEvent.click(screen.getByRole('button', {name: 'Keep my changes'}));
    expect(name).toHaveValue('My draft');
    await userEvent.click(screen.getByRole('button', {name: 'Reload latest version'}));
    await userEvent.click(screen.getByRole('button', {name: 'Discard changes and reload'}));
    await waitFor(() => expect(screen.getByRole('button', {name: 'Save changes'})).toBeEnabled());
    expect(screen.getByLabelText(kind === 'employees' ? 'Name' : 'Title')).toHaveValue(kind === 'employees' ? 'Alex' : 'Technician');
    fetch.mockResolvedValueOnce(reply({...record, version: record.version + 3}));
    await userEvent.click(screen.getByRole('button', {name: 'Save changes'}));
    const requests = fetch.mock.calls.filter(([, options]) => options.method === 'PUT');
    expect(JSON.parse(requests[1][1].body).version).toBe(record.version + 2);
  });
}

test('create submits editable fields without a version or ID', async () => {
  fetch.mockResolvedValue(reply({...records.employees, version: 1}, 201));
  render(<ProfileEditor kind="employees" onSaved={vi.fn()} onCancel={vi.fn()} />);
  await userEvent.type(screen.getByLabelText('Employee number'), 'E-2');
  await userEvent.type(screen.getByLabelText('Name'), 'New employee');
  await userEvent.type(screen.getByLabelText('Current title'), 'Technician');
  await userEvent.type(screen.getByLabelText('Status'), 'ACTIVE');
  await userEvent.type(screen.getByLabelText('Total years of experience'), '3');
  await userEvent.click(screen.getByRole('button', {name: 'Create profile'}));
  const body = JSON.parse(fetch.mock.calls[0][1].body);
  expect(body).not.toHaveProperty('version'); expect(body).not.toHaveProperty('id');
  expect(fetch.mock.calls[0][1].method).toBe('POST');
});

test('missing version disables editing without guessing one', async () => {
  const {version, ...legacy} = records.employees;
  fetch.mockResolvedValue(reply(legacy));
  render(<ProfileEditor kind="employees" recordId={legacy.id} onSaved={vi.fn()} onCancel={vi.fn()} />);
  expect(await screen.findByRole('alert')).toHaveTextContent('This profile does not include a valid version');
  expect(screen.getByRole('button', {name: 'Save changes'})).toBeDisabled();
  expect(fetch).toHaveBeenCalledTimes(1);
});

test('pending submissions are not duplicated', async () => {
  let complete;
  fetch.mockResolvedValueOnce(reply(records.jobs)).mockImplementationOnce(() => new Promise(resolve => {complete = resolve;}));
  render(<ProfileEditor kind="jobs" recordId="job-id" onSaved={vi.fn()} onCancel={vi.fn()} />);
  await screen.findByDisplayValue('Technician');
  await userEvent.click(screen.getByRole('button', {name: 'Save changes'}));
  expect(screen.getByRole('button', {name: 'Saving…'})).toBeDisabled();
  await userEvent.click(screen.getByRole('button', {name: 'Saving…'}));
  expect(fetch.mock.calls.filter(([, options]) => options.method === 'PUT')).toHaveLength(1);
  complete(reply({...records.jobs, version: 8}));
  await screen.findByText('Profile saved.');
});

for (const kind of ['employees', 'jobs']) {
  test(`${kind}: deletion requires confirmation and sends last-read version`, async () => {
    const record = records[kind]; const deleted = vi.fn();
    fetch.mockResolvedValueOnce(reply(record)).mockResolvedValueOnce(new Response(null, {status: 204}));
    render(<ProfileEditor kind={kind} recordId={record.id} onDeleted={deleted} />);
    await screen.findByDisplayValue(kind === 'employees' ? 'Alex' : 'Technician');
    await userEvent.click(screen.getByRole('button', {name: 'Delete permanently'}));
    expect(fetch).toHaveBeenCalledTimes(1);
    await userEvent.click(screen.getByRole('button', {name: 'Cancel deletion'}));
    expect(fetch).toHaveBeenCalledTimes(1);
    await userEvent.click(screen.getByRole('button', {name: 'Delete permanently'}));
    await userEvent.click(screen.getByRole('button', {name: 'Confirm permanent deletion'}));
    await waitFor(() => expect(deleted).toHaveBeenCalledTimes(1));
    expect(fetch.mock.calls[1][1].method).toBe('DELETE');
    expect(JSON.parse(fetch.mock.calls[1][1].body)).toEqual({version: record.version});
  });
}
test('stale deletion preserves draft and blocks repeated deletion', async () => {
  fetch.mockResolvedValueOnce(reply(records.employees)).mockResolvedValueOnce(reply({code: 'STALE_VERSION'}, 409));
  render(<ProfileEditor kind="employees" recordId="employee-id" />);
  const name = await screen.findByLabelText('Name');
  await userEvent.clear(name); await userEvent.type(name, 'Keep this draft');
  await userEvent.click(screen.getByRole('button', {name: 'Delete permanently'}));
  await userEvent.click(screen.getByRole('button', {name: 'Confirm permanent deletion'}));
  await screen.findByRole('alert');
  expect(name).toHaveValue('Keep this draft');
  expect(screen.getByRole('button', {name: 'Delete permanently'})).toBeDisabled();
  expect(fetch).toHaveBeenCalledTimes(2);
});
