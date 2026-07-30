"use client";

import { useFormStatus } from "react-dom";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export function SubmitButton({
  children,
  className,
  variant,
}: {
  children: React.ReactNode;
  className?: string;
  variant?: "primary" | "secondary" | "outline-light" | "ghost";
}) {
  const { pending } = useFormStatus();

  return (
    <Button type="submit" disabled={pending} className={`w-full ${className ?? ""}`} variant={variant}>
      {pending && <Loader2 size={16} className="animate-spin" />}
      {children}
    </Button>
  );
}
