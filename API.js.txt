// Thin wrapper around fetch for the owner and client API endpoints.
// Owner calls require a session token (from /api/owner-login), stored
// in memory only — NOT localStorage, so the owner needs to log in again
// after closing the tab. That's an intentional tradeoff for now; see notes.

const OWNER_BASE = "/api/owner";
const CLIENT_BASE = "/api/client";

export async function ownerLogin(email, password) {
  const res = await fetch("/api/owner-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || "Login failed");
  }
  return res.json(); // { token }
}

export async function ownerSetup(email, password) {
  const res = await fetch("/api/owner-setup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || "Setup failed");
  }
  return res.json();
}

function authHeaders(token) {
  return { "Content-Type": "application/json", Authorization: `Bearer ${token}` };
}

export async function ownerFetchAll(token) {
  const res = await fetch(OWNER_BASE, { headers: authHeaders(token) });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to load business data");
  return res.json(); // { clients, jobs, invoices }
}

export async function ownerCreateClient(token, client) {
  const res = await fetch(`${OWNER_BASE}?resource=clients`, {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(client),
  });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to create client");
  return res.json();
}

export async function ownerDeleteClient(token, id) {
  const res = await fetch(`${OWNER_BASE}?resource=clients&id=${id}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to delete client");
  return res.json();
}

export async function ownerCreateJob(token, job) {
  const res = await fetch(`${OWNER_BASE}?resource=jobs`, {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(job),
  });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to create job");
  return res.json();
}

export async function ownerUpdateJob(token, id, patch) {
  const res = await fetch(`${OWNER_BASE}?resource=jobs&id=${id}`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify(patch),
  });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to update job");
  return res.json();
}

export async function ownerDeleteJob(token, id) {
  const res = await fetch(`${OWNER_BASE}?resource=jobs&id=${id}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to delete job");
  return res.json();
}

export async function ownerUpdateInvoice(token, id, patch) {
  const res = await fetch(`${OWNER_BASE}?resource=invoices&id=${id}`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify(patch),
  });
  if (res.status === 401) throw new AuthError();
  if (!res.ok) throw new Error("Failed to update invoice");
  return res.json();
}

export async function ownerUpdateAccount(token, { currentPassword, newEmail, newPassword }) {
  const res = await fetch("/api/owner-account", {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify({ currentPassword, newEmail, newPassword }),
  });
  if (res.status === 401) throw new AuthError(); // session expired — different from wrong password (403)
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || "Failed to update account");
  }
  return res.json();
}

export async function clientFetchAll(code) {
  const res = await fetch(`${CLIENT_BASE}?code=${encodeURIComponent(code)}`);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || "Failed to load your data");
  }
  return res.json(); // { client, jobs, invoices }
}

export async function clientRequestJob(code, { date, time, type }) {
  const res = await fetch(`${CLIENT_BASE}?code=${encodeURIComponent(code)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ date, time, type }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || "Failed to submit request");
  }
  return res.json();
}

export class AuthError extends Error {
  constructor() {
    super("Not authenticated");
    this.name = "AuthError";
  }
}
