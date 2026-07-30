import { MessageCircle } from "lucide-react";
import { SITE } from "@/lib/data/site";

export function WhatsappFab() {
  return (
    <a
      href={`https://wa.me/${SITE.whatsappNumber}`}
      target="_blank"
      rel="noreferrer noopener"
      aria-label="Discuter sur WhatsApp"
      className="fixed bottom-6 right-6 z-40 inline-flex h-14 w-14 items-center justify-center rounded-full border-4 border-white/80 bg-[#25D366] text-white shadow-xl shadow-black/20 transition hover:-translate-y-1 hover:scale-105"
    >
      <MessageCircle size={26} />
    </a>
  );
}
