"use client";

import { useActionState } from "react";
import { loginAction } from "@/lib/actions/auth-actions";
import { TextField } from "@/components/ui/form-field";
import { SubmitButton } from "@/components/ui/submit-button";

export function LoginForm({ next }: { next?: string }) {
  const [state, formAction] = useActionState(loginAction, null);

  return (
    <form action={formAction} className="space-y-5">
      <input type="hidden" name="next" value={next ?? ""} />
      {state?.error && (
        <p className="rounded-lg bg-red-500/10 px-4 py-3 text-sm font-medium text-red-500">
          {state.error}
        </p>
      )}
      <TextField label="Adresse e-mail" name="email" type="email" required autoComplete="email" />
      <TextField
        label="Mot de passe"
        name="password"
        type="password"
        required
        autoComplete="current-password"
      />
      <SubmitButton>Se connecter</SubmitButton>
    </form>
  );
}
