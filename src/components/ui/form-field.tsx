import type { InputHTMLAttributes, ReactNode, SelectHTMLAttributes, TextareaHTMLAttributes } from "react";

const fieldClasses =
  "w-full rounded-2xl border border-border bg-surface px-4 py-3.5 text-sm text-text placeholder:text-text-muted/60 outline-none transition focus:border-brand-blue dark:focus:border-brand-gold";

function FieldWrapper({
  label,
  htmlFor,
  error,
  children,
}: {
  label: string;
  htmlFor: string;
  error?: string;
  children: ReactNode;
}) {
  return (
    <div className="space-y-1.5">
      <label htmlFor={htmlFor} className="text-sm font-semibold">
        {label}
      </label>
      {children}
      {error && <p className="text-xs font-medium text-red-500">{error}</p>}
    </div>
  );
}

export function TextField({
  label,
  name,
  error,
  ...props
}: { label: string; name: string; error?: string } & InputHTMLAttributes<HTMLInputElement>) {
  return (
    <FieldWrapper label={label} htmlFor={name} error={error}>
      <input id={name} name={name} className={fieldClasses} {...props} />
    </FieldWrapper>
  );
}

export function TextAreaField({
  label,
  name,
  error,
  ...props
}: { label: string; name: string; error?: string } & TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <FieldWrapper label={label} htmlFor={name} error={error}>
      <textarea id={name} name={name} className={`${fieldClasses} resize-none`} {...props} />
    </FieldWrapper>
  );
}

export function SelectField({
  label,
  name,
  error,
  children,
  ...props
}: {
  label: string;
  name: string;
  error?: string;
  children: ReactNode;
} & SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <FieldWrapper label={label} htmlFor={name} error={error}>
      <select id={name} name={name} className={fieldClasses} {...props}>
        {children}
      </select>
    </FieldWrapper>
  );
}
