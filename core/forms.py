FIELD_CLASSES = (
    "w-full rounded-2xl border border-border bg-surface px-4 py-3.5 text-sm text-text "
    "placeholder:text-text-muted/60 outline-none transition focus:border-brand-blue"
)


class StyledFormMixin:
    """Applies the site's shared input styling to every field's widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{FIELD_CLASSES} {existing}".strip()
            if field.widget.__class__.__name__ == "Textarea":
                field.widget.attrs["class"] += " resize-none"
                field.widget.attrs.setdefault("rows", 5)
