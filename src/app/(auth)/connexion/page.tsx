import type { Metadata } from "next";
import Link from "next/link";
import { LoginForm } from "@/components/forms/login-form";

export const metadata: Metadata = {
  title: "Connexion",
};

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string }>;
}) {
  const { next } = await searchParams;

  return (
    <div>
      <h1 className="text-3xl font-extrabold">Bon retour parmi nous</h1>
      <p className="mt-2 text-sm text-text-muted">
        Connectez-vous pour suivre vos transferts et gérer vos bénéficiaires.
      </p>
      <div className="mt-8">
        <LoginForm next={next} />
      </div>
      <p className="mt-6 text-center text-sm text-text-muted">
        Pas encore de compte ?{" "}
        <Link href="/inscription" className="font-bold text-brand-blue dark:text-brand-gold-light">
          Ouvrir un compte
        </Link>
      </p>
    </div>
  );
}
