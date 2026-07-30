import "server-only";

import { cache } from "react";
import { db } from "@/lib/db";
import { getSession } from "@/lib/session";

export const getCurrentUser = cache(async () => {
  const session = await getSession();
  if (!session) return null;

  const user = await db.user.findUnique({
    where: { id: session.userId },
    select: {
      id: true,
      fullName: true,
      email: true,
      phone: true,
      country: true,
      createdAt: true,
    },
  });

  return user;
});
