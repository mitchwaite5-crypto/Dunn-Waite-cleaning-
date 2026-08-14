import { getDatabase } from "@netlify/database";
import crypto from "node:crypto";
import { verifyOwnerToken } from "./lib/auth.js";

const db = getDatabase();

function hashPassword(password, salt) {
  return crypto.scryptSync(password, salt, 64).toString("hex");
}

export default async (req) => {
  const authed = await verifyOwnerToken(req);
  if (!authed) {
    return new Response(JSON.stringify({ error: "Not authenticated" }), { status: 401 });
  }
  if (req.method !== "PATCH") return new Response("Method not allowed", { status: 405 });

  const { currentPassword, newEmail, newPassword } = await req.json();
  if (!currentPassword) {
    return new Response(JSON.stringify({ error: "Enter your current password to confirm this change" }), { status: 400 });
  }

  const [account] = await db.sql`SELECT * FROM owner_account WHERE id = 1`;
  if (!account) {
    return new Response(JSON.stringify({ error: "No owner account set up" }), { status: 404 });
  }

  const [storedHash, salt] = account.password_hash.split(":");
  const attemptHash = hashPassword(currentPassword, salt);
  if (attemptHash !== storedHash) {
    // 403, not 401 — this is a wrong password, not an expired/invalid session.
    return new Response(JSON.stringify({ error: "Current password is incorrect" }), { status: 403 });
  }

  let newHashField = null;
  if (newPassword) {
    if (newPassword.length < 8) {
      return new Response(JSON.stringify({ error: "New password must be at least 8 characters" }), { status: 400 });
    }
    const newSalt = crypto.randomBytes(16).toString("hex");
    newHashField = hashPassword(newPassword, newSalt) + ":" + newSalt;
  }

  if (!newEmail && !newHashField) {
    return new Response(JSON.stringify({ error: "Nothing to update" }), { status: 400 });
  }

  await db.sql`
    UPDATE owner_account SET
      email = COALESCE(${newEmail ?? null}, email),
      password_hash = COALESCE(${newHashField}, password_hash)
    WHERE id = 1
  `;

  return Response.json({ ok: true });
};

export const config = { path: "/api/owner-account" };
