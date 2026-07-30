# Blue Sky — Money Transfer Website

Marketing site and customer portal for Blue Sky, a money transfer agency operating across the RDC, Zambia, Namibia, South Africa, Zimbabwe, Kenya, Tanzania, and Malawi.

## Stack

- [Next.js 16](https://nextjs.org) (App Router, TypeScript, Turbopack)
- [Tailwind CSS 4](https://tailwindcss.com)
- [Prisma 7](https://www.prisma.io) + SQLite (swap `DATABASE_URL` for Postgres/MySQL in production)
- Custom auth: bcrypt password hashing + signed JWT session cookies (`jose`), route protection via `proxy.ts`

## Getting started

```bash
npm install
cp .env.example .env   # then fill in SESSION_SECRET
npx prisma migrate dev
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Project structure

- `src/app/(marketing)` — public pages (home, about, team, impact, countries, contact)
- `src/app/(auth)` — sign up / log in
- `src/app/(dashboard)/tableau-de-bord` — authenticated customer dashboard (transfers, recipients)
- `src/lib/actions` — server actions (auth, transfers, recipients, contact form)
- `prisma/schema.prisma` — data model (User, Recipient, Transfer, ContactMessage)

## Deployment

Any Node.js host works (Vercel, Railway, a VPS, etc.). Set `DATABASE_URL` and `SESSION_SECRET` as environment variables, then run `npm run build && npm run start`.
