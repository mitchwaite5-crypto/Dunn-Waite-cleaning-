import { getDatabase } from "@netlify/database";
import crypto from "node:crypto";

const db = getDatabase();

export async function verifyOwnerToken(req) {
  const authHeader = req.headers.get("authorization") || "";
  const token = authHeader.replace(/^Bearer\s+/i, "");
  if (!token) return false;

  let decoded;
  try {
    decoded = Buffer.from(token, "base64").toString("utf8");
  } catch {
    return false;
  }
  const [expiryStr, hmac] = decoded.split(".");
  const expiry = Number(expiryStr);
  if (!expiry || !hmac || Date.now() > expiry) return false;

  const [account] = await db.sql`SELECT password_hash FROM owner_account WHERE id = 1`;
  if (!account) return false;

  const expectedHmac = crypto.createHmac("sha256", account.password_hash).update(String(expiry)).digest("hex");
  return hmac === expectedHmac;
}
