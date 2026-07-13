import crypto from "crypto";
import { cookies } from "next/headers";

const SESSION_COOKIE = "admin_session";
const secret = process.env.ADMIN_SESSION_SECRET || "dev-secret-change-me";

function sign(value: string) {
  return crypto.createHmac("sha256", secret).update(value).digest("hex");
}

export function createSessionToken(username: string) {
  const payload = `${username}.${Date.now()}`;
  return `${payload}.${sign(payload)}`;
}

export function verifySessionToken(token: string | undefined): string | null {
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  const [username, ts, sig] = parts;
  const payload = `${username}.${ts}`;
  if (sign(payload) !== sig) return null;
  return username;
}

export async function getAdminUsername(): Promise<string | null> {
  const store = await cookies();
  return verifySessionToken(store.get(SESSION_COOKIE)?.value);
}

export const SESSION_COOKIE_NAME = SESSION_COOKIE;
