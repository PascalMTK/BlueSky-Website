"use server";

import { randomBytes } from "crypto";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { db } from "@/lib/db";
import { getSession } from "@/lib/session";
import { transferSchema } from "@/lib/validation";
import type { FormState } from "@/lib/actions/auth-actions";

function generateReference() {
  return `BS-${randomBytes(4).toString("hex").toUpperCase()}`;
}

export async function createTransferAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const session = await getSession();
  if (!session) return { error: "Vous devez être connecté." };

  const parsed = transferSchema.safeParse({
    recipientId: formData.get("recipientId"),
    amountSent: formData.get("amountSent"),
    currencySent: formData.get("currencySent"),
    paymentMethod: formData.get("paymentMethod"),
    note: formData.get("note") || undefined,
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

  const [recipient, user] = await Promise.all([
    db.recipient.findFirst({
      where: { id: parsed.data.recipientId, userId: session.userId },
    }),
    db.user.findUnique({ where: { id: session.userId } }),
  ]);
  if (!recipient || !user) {
    return { error: "Bénéficiaire introuvable." };
  }

  await db.transfer.create({
    data: {
      ...parsed.data,
      originCountry: user.country ?? "RDC",
      destinationCountry: recipient.country,
      userId: session.userId,
      reference: generateReference(),
    },
  });

  revalidatePath("/tableau-de-bord");
  redirect("/tableau-de-bord");
}

export async function cancelTransferAction(transferId: string) {
  const session = await getSession();
  if (!session) return;

  await db.transfer.updateMany({
    where: { id: transferId, userId: session.userId, status: "PENDING" },
    data: { status: "CANCELLED" },
  });

  revalidatePath("/tableau-de-bord");
}
