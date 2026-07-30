"use client";

import { useActionState } from "react";
import { CheckCircle2 } from "lucide-react";
import { sendContactMessageAction } from "@/lib/actions/contact-actions";
import { TextField, TextAreaField } from "@/components/ui/form-field";
import { SubmitButton } from "@/components/ui/submit-button";

export function ContactForm() {
  const [state, formAction] = useActionState(sendContactMessageAction, null);

  if (state?.success) {
    return (
      <div className="flex flex-col items-center gap-3 rounded-2xl border border-border bg-surface p-10 text-center">
        <CheckCircle2 className="text-brand-gold" size={40} />
        <h3 className="text-lg font-bold">Message envoyé</h3>
        <p className="text-sm text-text-muted">
          Merci de nous avoir contactés. Notre équipe vous répondra très
          prochainement.
        </p>
      </div>
    );
  }

  return (
    <form action={formAction} className="space-y-5 rounded-2xl border border-border bg-surface p-8">
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
      <TextField
        label="Adresse e-mail"
        name="email"
        type="email"
        required
        error={state?.fieldErrors?.email}
      />
      <TextField label="Pays" name="country" placeholder="Ex : RDC, Zambie…" />
      <TextAreaField
        label="Votre message"
        name="message"
        rows={5}
        required
        error={state?.fieldErrors?.message}
      />
      <SubmitButton>Envoyer le message</SubmitButton>
    </form>
  );
}
