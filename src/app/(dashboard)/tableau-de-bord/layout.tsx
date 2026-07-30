import { redirect } from "next/navigation";
import { Logo } from "@/components/brand/logo";
import { DashboardNav } from "@/components/dashboard/dashboard-nav";
import { LogoutButton } from "@/components/dashboard/logout-button";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { getCurrentUser } from "@/lib/current-user";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await getCurrentUser();
  if (!user) redirect("/connexion");

  return (
    <div className="min-h-screen bg-surface-muted lg:grid lg:grid-cols-[292px_1fr]">
      <aside className="hidden border-r border-border bg-brand-blue-deep text-white lg:flex lg:flex-col lg:justify-between lg:p-6">
        <div>
          <Logo />
          <div className="mt-8">
            <DashboardNav />
          </div>
        </div>
        <div className="space-y-3">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <p className="text-sm font-bold">{user.fullName}</p>
            <p className="truncate text-xs text-white/50">{user.email}</p>
          </div>
          <LogoutButton />
        </div>
      </aside>

      <div className="flex min-h-screen flex-col">
        <header className="flex items-center justify-between border-b border-border bg-surface px-5 py-4 lg:justify-end lg:px-8">
          <div className="lg:hidden">
            <Logo />
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle />
          </div>
        </header>

        <nav className="flex gap-1 overflow-x-auto border-b border-border bg-surface px-4 py-2 lg:hidden">
          <DashboardNav className="flex flex-row gap-1" />
        </nav>

        <main className="flex-1 p-5 sm:p-8">{children}</main>

        <div className="border-t border-border bg-surface p-4 lg:hidden">
          <LogoutButton />
        </div>
      </div>
    </div>
  );
}
