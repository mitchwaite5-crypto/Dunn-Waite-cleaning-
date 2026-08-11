import { getDatabase } from "@netlify/database";
import crypto from "node:crypto";

const db = getDatabase();

function hashPassword(password, salt) {
  return crypto.scryptSync(password, salt, 64).toString("hex");
}

export default async (req) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });

  const { email, password } = await req.json();
  const [account] = await db.sql`SELECT * FROM owner_account WHERE id = 1`;

  if (!account) {
    return new Response(JSON.stringify({ error: "No owner account set up yet" }), { status: 404 });
  }

  const [storedHash, salt] = account.password_hash.split(":");
  const attemptHash = hashPassword(password, salt);

  if (account.email !== email || attemptHash !== storedHash) {
    return new Response(JSON.stringify({ error: "Invalid email or password" }), { status: 401 });
  }

  // Simple signed session token: base64(expiry) + hmac signature.
  // Good enough for a single-owner app; not a full auth system.
  const expiry = Date.now() + 1000 * 60 * 60 * 24 * 7; // 7 days
  const hmac = crypto.createHmac("sha256", account.password_hash).update(String(expiry)).digest("hex");
  const token = Buffer.from(`${expiry}.${hmac}`).toString("base64");

  return Response.json({ token });
};

export const config = { path: "/api/owner-login" };
