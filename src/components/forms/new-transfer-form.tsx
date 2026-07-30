"use client";

import { useActionState } from "react";
import { createTransferAction } from "@/lib/actions/transfer-actions";
import { TextField, SelectField, TextAreaField } from "@/components/ui/form-field";
import { SubmitButton } from "@/components/ui/submit-button";
import { SITE } from "@/lib/data/site";
import type { Recipient } from "@/generated/prisma/client";

const CURRENCIES = ["USD", "CDF", "ZMW", "NAD", "ZAR", "KES", "TZS", "MWK"];

export function NewTransferForm({ recipients }: { recipients: Recipient[] }) {
  const [state, formAction] = useActionState(createTransferAction, null);

  return (
    <form action={formAction} className="space-y-5 rounded-2xl border border-border bg-surface p-8">
      {state?.error && (
        <p className="rounded-lg bg-red-500/10 px-4 py-3 text-sm font-medium text-red-500">
          {state.error}
        </p>
      )}
      <SelectField
        label="Bénéficiaire"
        name="recipientId"
        required
        defaultValue=""
        error={state?.fieldErrors?.recipientId}
      >
        <option value="" disabled>
          Sélectionnez un bénéficiaire
        </option>
        {recipients.map((r) => (
          <option key={r.id} value={r.id}>
            {r.fullName} — {r.country}
          </option>
        ))}
      </SelectField>

      <div className="grid gap-5 sm:grid-cols-2">
        <TextField
          label="Montant"
          name="amountSent"
          type="number"
          min="1"
          step="0.01"
          required
          error={state?.fieldErrors?.amountSent}
        />
        <SelectField
          label="Devise"
          name="currencySent"
          required
          defaultValue="USD"
          error={state?.fieldErrors?.currencySent}
        >
          {CURRENCIES.map((currency) => (
            <option key={currency} value={currency}>
              {currency}
            </option>
          ))}
        </SelectField>
      </div>

      <SelectField
        label="Moyen de paiement"
        name="paymentMethod"
        required
        defaultValue=""
        error={state?.fieldErrors?.paymentMethod}
      >
        <option value="" disabled>
          Sélectionnez un moyen de paiement
        </option>
        {SITE.paymentPartners.map((partner) => (
          <option key={partner} value={partner}>
            {partner}
          </option>
        ))}
      </SelectField>

      <TextAreaField label="Note (optionnel)" name="note" rows={3} />

      <SubmitButton>Envoyer la demande de transfert</SubmitButton>
      <p className="text-center text-xs text-text-muted">
        Votre demande sera confirmée par notre équipe avant traitement.
      </p>
    </form>
  );
}
