import type { Metadata } from "next";
import Link from "next/link";
import { SignupForm } from "@/components/forms/signup-form";

export const metadata: Metadata = {
  title: "Ouvrir un compte",
};

export default function SignupPage() {
  return (
    <div>
      <h1 className="text-3xl font-extrabold">Ouvrez votre compte Blue Sky</h1>
      <p className="mt-2 text-sm text-text-muted">
        Gratuit et rapide. Suivez vos transferts depuis un seul endroit.
      </p>
      <div className="mt-8">
        <SignupForm />
      </div>
      <p className="mt-6 text-center text-sm text-text-muted">
        Déjà un compte ?{" "}
        <Link href="/connexion" className="font-bold text-brand-blue dark:text-brand-gold-light">
          Se connecter
        </Link>
      </p>
    </div>
  );
}
