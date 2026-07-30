import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { ArrowUpRight, Send, Users, Clock, CheckCircle2 } from "lucide-react";
import { LinkButton } from "@/components/ui/button";
import { StatusBadge } from "@/components/dashboard/status-badge";
import { db } from "@/lib/db";
import { getCurrentUser } from "@/lib/current-user";
import { formatAmount, formatDate } from "@/lib/format";
import { cancelTransferAction } from "@/lib/actions/transfer-actions";

export const metadata: Metadata = { title: "Tableau de bord" };

export default async function DashboardOverviewPage() {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion");

  const [transfers, recipientCount] = await Promise.all([
    db.transfer.findMany({
      where: { userId: user.id },
      include: { recipient: true },
      orderBy: { createdAt: "desc" },
      take: 8,
    }),
    db.recipient.count({ where: { userId: user.id } }),
  ]);

  const pendingCount = transfers.filter((t) => t.status === "PENDING").length;
  const completedCount = transfers.filter((t) => t.status === "COMPLETED").length;

  const stats = [
    { label: "Transferts envoyés", value: transfers.length, icon: Send },
    { label: "En attente", value: pendingCount, icon: Clock },
    { label: "Terminés", value: completedCount, icon: CheckCircle2 },
    { label: "Bénéficiaires", value: recipientCount, icon: Users },
  ];

  return (
    <div className="space-y-8">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-2xl font-extrabold sm:text-3xl">
            Bonjour, {user.fullName.split(" ")[0]} 👋
          </h1>
          <p className="mt-1 text-sm text-text-muted">
            Voici un aperçu de votre activité Blue Sky.
          </p>
        </div>
        <LinkButton href="/tableau-de-bord/nouveau-transfert">
          <Send size={16} /> Nouveau transfert
        </LinkButton>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-2xl border border-border bg-surface p-6">
            <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-brand-blue/10 text-brand-blue dark:bg-white/10 dark:text-brand-gold-light">
              <Icon size={18} />
            </div>
            <p className="text-2xl font-extrabold">{value}</p>
            <p className="text-sm text-text-muted">{label}</p>
          </div>
        ))}
      </div>

      <div className="rounded-2xl border border-border bg-surface">
        <div className="flex items-center justify-between border-b border-border p-6">
          <h2 className="text-lg font-bold">Transferts récents</h2>
          {recipientCount === 0 && (
            <LinkButton href="/tableau-de-bord/beneficiaires" variant="ghost" size="md">
              Ajouter un bénéficiaire
            </LinkButton>
          )}
        </div>

        {transfers.length === 0 ? (
          <div className="p-10 text-center text-sm text-text-muted">
            Vous n&apos;avez encore effectué aucun transfert.
            <div className="mt-4">
              <LinkButton href="/tableau-de-bord/nouveau-transfert">
                Envoyer mon premier transfert <ArrowUpRight size={16} />
              </LinkButton>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="text-xs uppercase tracking-wide text-text-muted">
                  <th className="px-6 py-3">Référence</th>
                  <th className="px-6 py-3">Bénéficiaire</th>
                  <th className="px-6 py-3">Destination</th>
                  <th className="px-6 py-3">Montant</th>
                  <th className="px-6 py-3">Statut</th>
                  <th className="px-6 py-3">Date</th>
                  <th className="px-6 py-3" />
                </tr>
              </thead>
              <tbody>
                {transfers.map((transfer) => (
                  <tr key={transfer.id} className="border-t border-border">
                    <td className="px-6 py-4 font-mono text-xs font-bold">{transfer.reference}</td>
                    <td className="px-6 py-4">{transfer.recipient?.fullName ?? "—"}</td>
                    <td className="px-6 py-4">{transfer.destinationCountry}</td>
                    <td className="px-6 py-4 font-semibold">
                      {formatAmount(transfer.amountSent, transfer.currencySent)}
                    </td>
                    <td className="px-6 py-4">
                      <StatusBadge status={transfer.status} />
                    </td>
                    <td className="px-6 py-4 text-text-muted">{formatDate(transfer.createdAt)}</td>
                    <td className="px-6 py-4 text-right">
                      {transfer.status === "PENDING" && (
                        <form action={cancelTransferAction.bind(null, transfer.id)}>
                          <button className="text-xs font-bold text-red-500 hover:underline">
                            Annuler
                          </button>
                        </form>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
