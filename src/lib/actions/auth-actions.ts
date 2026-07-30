"use server";

import bcrypt from "bcryptjs";
import { redirect } from "next/navigation";
import { db } from "@/lib/db";
import { createSession, destroySession } from "@/lib/session";
import { loginSchema, signupSchema } from "@/lib/validation";

export type FormState = {
  error?: string;
  success?: boolean;
  fieldErrors?: Record<string, string>;
} | null;

export async function signupAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const raw = {
    fullName: formData.get("fullName"),
    email: formData.get("email"),
    phone: formData.get("phone"),
    country: formData.get("country"),
    password: formData.get("password"),
  };

  const parsed = signupSchema.safeParse(raw);
  if (!parsed.success) {
    const fieldErrors: Record<string, string> = {};
    for (const issue of parsed.error.issues) {
      const key = issue.path[0];
      if (typeof key === "string" && !fieldErrors[key]) {
        fieldErrors[key] = issue.message;
      }
    }
    return { error: "Merci de corriger les champs indiqués.", fieldErrors };
  }

  const { fullName, email, phone, country, password } = parsed.data;

  const existing = await db.user.findUnique({ where: { email } });
  if (existing) {
    return {
      error: "Un compte existe déjà avec cette adresse e-mail.",
      fieldErrors: { email: "Adresse e-mail déjà utilisée" },
    };
  }

  const passwordHash = await bcrypt.hash(password, 12);

  const user = await db.user.create({
    data: { fullName, email, phone, country, passwordHash },
  });

  await createSession({ userId: user.id });
  redirect("/tableau-de-bord");
}

export async function loginAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const raw = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const parsed = loginSchema.safeParse(raw);
  if (!parsed.success) {
    return { error: "Adresse e-mail ou mot de passe invalide." };
  }

  const { email, password } = parsed.data;

  const user = await db.user.findUnique({ where: { email } });
  if (!user) {
    return { error: "Adresse e-mail ou mot de passe incorrect." };
  }

  const passwordMatches = await bcrypt.compare(password, user.passwordHash);
  if (!passwordMatches) {
    return { error: "Adresse e-mail ou mot de passe incorrect." };
  }

  await createSession({ userId: user.id });

  const next = formData.get("next");
  const safeNext = typeof next === "string" && next.startsWith("/") ? next : "/tableau-de-bord";
  redirect(safeNext);
}

export async function logoutAction() {
  await destroySession();
  redirect("/connexion");
}
