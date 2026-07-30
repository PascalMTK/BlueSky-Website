"use server";

import { revalidatePath } from "next/cache";
import { db } from "@/lib/db";
import { getSession } from "@/lib/session";
import { recipientSchema } from "@/lib/validation";
import type { FormState } from "@/lib/actions/auth-actions";

export async function createRecipientAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const session = await getSession();
  if (!session) return { error: "Vous devez être connecté." };

  const parsed = recipientSchema.safeParse({
    fullName: formData.get("fullName"),
    country: formData.get("country"),
    phone: formData.get("phone") || undefined,
    relationship: formData.get("relationship") || undefined,
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

  await db.recipient.create({
    data: { ...parsed.data, userId: session.userId },
  });

  revalidatePath("/tableau-de-bord/beneficiaires");
  revalidatePath("/tableau-de-bord/nouveau-transfert");
  return null;
}

export async function deleteRecipientAction(recipientId: string) {
  const session = await getSession();
  if (!session) return;

  await db.recipient.deleteMany({
    where: { id: recipientId, userId: session.userId },
  });

  revalidatePath("/tableau-de-bord/beneficiaires");
  revalidatePath("/tableau-de-bord/nouveau-transfert");
}
