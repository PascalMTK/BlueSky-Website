import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { Trash2, Phone } from "lucide-react";
import { db } from "@/lib/db";
import { getCurrentUser } from "@/lib/current-user";
import { AddRecipientForm } from "@/components/forms/add-recipient-form";
import { deleteRecipientAction } from "@/lib/actions/recipient-actions";
import { COUNTRIES } from "@/lib/data/countries";

export const metadata: Metadata = { title: "Bénéficiaires" };

export default async function RecipientsPage() {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion");

  const recipients = await db.recipient.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold sm:text-3xl">Bénéficiaires</h1>
        <p className="mt-1 text-sm text-text-muted">
          Gérez les personnes qui reçoivent vos transferts.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_1.3fr]">
        <AddRecipientForm />

        <div className="space-y-4">
          {recipients.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-border p-10 text-center text-sm text-text-muted">
              Aucun bénéficiaire enregistré pour le moment.
            </div>
          ) : (
            recipients.map((recipient) => {
              const flag = COUNTRIES.find((c) => c.name === recipient.country)?.flag;
              return (
                <div
                  key={recipient.id}
                  className="flex items-start justify-between gap-4 rounded-2xl border border-border bg-surface p-6"
                >
                  <div>
                    <p className="font-bold">
                      {flag} {recipient.fullName}
                    </p>
                    <p className="text-sm text-text-muted">{recipient.country}</p>
                    {recipient.phone && (
                      <p className="mt-1 flex items-center gap-1.5 text-sm text-text-muted">
                        <Phone size={13} /> {recipient.phone}
                      </p>
                    )}
                    {recipient.relationship && (
                      <p className="mt-1 text-xs text-text-muted">{recipient.relationship}</p>
                    )}
                  </div>
                  <form action={deleteRecipientAction.bind(null, recipient.id)}>
                    <button
                      type="submit"
                      aria-label="Supprimer"
                      className="rounded-lg p-2 text-text-muted transition hover:bg-red-500/10 hover:text-red-500"
                    >
                      <Trash2 size={16} />
                    </button>
                  </form>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
