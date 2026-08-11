import { getDatabase } from "@netlify/database";
import crypto from "node:crypto";

const db = getDatabase();

function hashPassword(password, salt) {
  return crypto.scryptSync(password, salt, 64).toString("hex");
}

// One-time setup: only works if no owner account exists yet.
// After first use, this route always returns 409 — the account is locked in.
export default async (req) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });

  const [existing] = await db.sql`SELECT id FROM owner_account WHERE id = 1`;
  if (existing) {
    return new Response(JSON.stringify({ error: "Owner account already set up" }), { status: 409 });
  }

  const { email, password } = await req.json();
  if (!email || !password || password.length < 8) {
    return new Response(JSON.stringify({ error: "Email and an 8+ character password are required" }), { status: 400 });
  }

  const salt = crypto.randomBytes(16).toString("hex");
  const hash = hashPassword(password, salt);
  await db.sql`INSERT INTO owner_account (id, email, password_hash) VALUES (1, ${email}, ${hash + ":" + salt})`;

  return Response.json({ ok: true });
};

export const config = { path: "/api/owner-setup" };
