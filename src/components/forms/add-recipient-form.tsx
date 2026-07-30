"use client";

import { useActionState, useRef, useEffect } from "react";
import { createRecipientAction } from "@/lib/actions/recipient-actions";
import { TextField, SelectField } from "@/components/ui/form-field";
import { SubmitButton } from "@/components/ui/submit-button";
import { COUNTRIES } from "@/lib/data/countries";

export function AddRecipientForm() {
  const [state, formAction] = useActionState(createRecipientAction, null);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (state === null) formRef.current?.reset();
  }, [state]);

  return (
    <form ref={formRef} action={formAction} className="space-y-5 rounded-2xl border border-border bg-surface p-6">
      <h2 className="text-lg font-bold">Ajouter un bénéficiaire</h2>
      {state?.error && (
        <p className="rounded-lg bg-red-500/10 px-4 py-3 text-sm font-medium text-red-500">
          {state.error}
        </p>
      )}
      <TextField
        label="Nom complet"
        name="fullName"
        required
        error={state?.fieldErrors?.fullName}
      />
      <SelectField label="Pays" name="country" required defaultValue="" error={state?.fieldErrors?.country}>
        <option value="" disabled>
          Sélectionnez un pays
        </option>
        {COUNTRIES.map((c) => (
          <option key={c.code} value={c.name}>
            {c.flag} {c.name}
          </option>
        ))}
      </SelectField>
      <TextField label="Téléphone (optionnel)" name="phone" type="tel" />
      <TextField label="Relation (optionnel)" name="relationship" placeholder="Ex : Sœur, ami…" />
      <SubmitButton>Ajouter le bénéficiaire</SubmitButton>
    </form>
  );
}
