import type { TransferStatus } from "@/generated/prisma/enums";

const STYLES: Record<TransferStatus, string> = {
  PENDING: "bg-amber-500/10 text-amber-600 dark:text-amber-400",
  PROCESSING: "bg-blue-500/10 text-blue-600 dark:text-blue-400",
  COMPLETED: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
  CANCELLED: "bg-red-500/10 text-red-600 dark:text-red-400",
};

const LABELS: Record<TransferStatus, string> = {
  PENDING: "En attente",
  PROCESSING: "En cours",
  COMPLETED: "Terminé",
  CANCELLED: "Annulé",
};

export function StatusBadge({ status }: { status: TransferStatus }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold ${STYLES[status]}`}
    >
      {LABELS[status]}
    </span>
  );
}
