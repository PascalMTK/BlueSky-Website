import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { UserPlus } from "lucide-react";
import { db } from "@/lib/db";
import { getCurrentUser } from "@/lib/current-user";
import { NewTransferForm } from "@/components/forms/new-transfer-form";
import { LinkButton } from "@/components/ui/button";

export const metadata: Metadata = { title: "Nouveau transfert" };

export default async function NewTransferPage() {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion");

  const recipients = await db.recipient.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: "desc" },
  });

  return (
    <div className="mx-auto max-w-xl space-y-8">
      <div>
        <h1 className="text-2xl font-extrabold sm:text-3xl">Nouveau transfert</h1>
        <p className="mt-1 text-sm text-text-muted">
          Renseignez les détails de votre envoi. Notre équipe vous contactera pour la confirmation.
        </p>
      </div>

      {recipients.length === 0 ? (
        <div className="flex flex-col items-center gap-4 rounded-2xl border border-dashed border-border p-10 text-center">
          <UserPlus className="text-brand-blue dark:text-brand-gold-light" size={32} />
          <p className="text-sm text-text-muted">
            Ajoutez d&apos;abord un bénéficiaire avant d&apos;envoyer un transfert.
          </p>
          <LinkButton href="/tableau-de-bord/beneficiaires">Ajouter un bénéficiaire</LinkButton>
        </div>
      ) : (
        <NewTransferForm recipients={recipients} />
      )}
    </div>
  );
}
