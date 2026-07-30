"use client";

import { LogOut } from "lucide-react";
import { logoutAction } from "@/lib/actions/auth-actions";

export function LogoutButton({ className = "" }: { className?: string }) {
  return (
    <form action={logoutAction}>
      <button
        type="submit"
        className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold text-text-muted transition hover:bg-surface-muted hover:text-red-500 ${className}`}
      >
        <LogOut size={18} />
        Se déconnecter
      </button>
    </form>
  );
}
