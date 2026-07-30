import { z } from "zod";

export const signupSchema = z.object({
  fullName: z.string().trim().min(2, "Entrez votre nom complet"),
  email: z.email("Adresse e-mail invalide").trim().toLowerCase(),
  phone: z.string().trim().min(6, "Numéro de téléphone invalide"),
  country: z.string().trim().min(2, "Sélectionnez votre pays"),
  password: z
    .string()
    .min(8, "Le mot de passe doit contenir au moins 8 caractères"),
});

export const loginSchema = z.object({
  email: z.email("Adresse e-mail invalide").trim().toLowerCase(),
  password: z.string().min(1, "Mot de passe requis"),
});

export const recipientSchema = z.object({
  fullName: z.string().trim().min(2, "Nom du bénéficiaire requis"),
  country: z.string().trim().min(2, "Sélectionnez un pays"),
  phone: z.string().trim().optional(),
  relationship: z.string().trim().optional(),
});

export const contactSchema = z.object({
  fullName: z.string().trim().min(2, "Entrez votre nom complet"),
  email: z.email("Adresse e-mail invalide").trim().toLowerCase(),
  country: z.string().trim().optional(),
  message: z.string().trim().min(10, "Votre message est un peu court"),
});

export const transferSchema = z.object({
  recipientId: z.string().trim().min(1, "Sélectionnez un bénéficiaire"),
  amountSent: z.coerce.number().positive("Le montant doit être supérieur à 0"),
  currencySent: z.string().trim().min(2, "Sélectionnez une devise"),
  paymentMethod: z.string().trim().min(2, "Sélectionnez un moyen de paiement"),
  note: z.string().trim().optional(),
});
