import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { WhatsappFab } from "@/components/whatsapp-fab";
import { getCurrentUser } from "@/lib/current-user";

export default async function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await getCurrentUser();

  return (
    <>
      <SiteHeader userName={user?.fullName ?? null} />
      <main className="flex-1">{children}</main>
      <SiteFooter />
      <WhatsappFab />
    </>
  );
}
