"use server";

import { db } from "@/lib/db";
import { contactSchema } from "@/lib/validation";
import type { FormState } from "@/lib/actions/auth-actions";

export async function sendContactMessageAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const parsed = contactSchema.safeParse({
    fullName: formData.get("fullName"),
    email: formData.get("email"),
    country: formData.get("country") || undefined,
    message: formData.get("message"),
  });

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

  await db.contactMessage.create({ data: parsed.data });

  return { success: true };
}
