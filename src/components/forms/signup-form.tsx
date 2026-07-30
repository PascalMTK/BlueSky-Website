"use client";

import { useActionState } from "react";
import { signupAction } from "@/lib/actions/auth-actions";
import { TextField, SelectField } from "@/components/ui/form-field";
import { SubmitButton } from "@/components/ui/submit-button";
import { COUNTRIES } from "@/lib/data/countries";

export function SignupForm() {
  const [state, formAction] = useActionState(signupAction, null);

  return (
    <form action={formAction} className="space-y-5">
      {state?.error && (
        <p className="rounded-lg bg-red-500/10 px-4 py-3 text-sm font-medium text-red-500">
          {state.error}
        </p>
      )}
      <TextField
        label="Nom complet"
        name="fullName"
        required
        autoComplete="name"
        error={state?.fieldErrors?.fullName}
      />
      <TextField
        label="Adresse e-mail"
        name="email"
        type="email"
        required
        autoComplete="email"
        error={state?.fieldErrors?.email}
      />
      <TextField
        label="Téléphone"
        name="phone"
        type="tel"
        required
        placeholder="+243 ..."
        autoComplete="tel"
        error={state?.fieldErrors?.phone}
      />
      <SelectField label="Pays" name="country" required defaultValue="" error={state?.fieldErrors?.country}>
        <option value="" disabled>
          Sélectionnez votre pays
        </option>
        {COUNTRIES.map((c) => (
          <option key={c.code} value={c.name}>
            {c.flag} {c.name}
          </option>
        ))}
      </SelectField>
      <TextField
        label="Mot de passe"
        name="password"
        type="password"
        required
        autoComplete="new-password"
        error={state?.fieldErrors?.password}
      />
      <p className="text-xs text-text-muted">
        En créant un compte, vous acceptez d&apos;être contacté par Blue Sky
        au sujet de vos transferts.
      </p>
      <SubmitButton>Créer mon compte</SubmitButton>
    </form>
  );
}
