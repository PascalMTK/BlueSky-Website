from django import forms

from blog.models import Post
from core.forms import StyledFormMixin


class PostForm(StyledFormMixin, forms.ModelForm):
    title = forms.CharField(
        label="Titre",
        min_length=3,
        error_messages={"required": "Entrez un titre", "min_length": "Entrez un titre"},
    )
    excerpt = forms.CharField(label="Résumé (optionnel)", required=False)
    body = forms.CharField(
        label="Contenu",
        min_length=10,
        widget=forms.Textarea,
        error_messages={
            "required": "Le contenu est trop court",
            "min_length": "Le contenu est trop court",
        },
    )
    cover_image = forms.ImageField(label="Image de couverture (optionnel)", required=False)
    is_published = forms.BooleanField(label="Publier immédiatement", required=False)

    class Meta:
        model = Post
        fields = ["title", "excerpt", "body", "cover_image", "is_published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # StyledFormMixin applies the text-input styling to every field; a
        # checkbox needs its own, much smaller, treatment instead.
        self.fields["is_published"].widget.attrs["class"] = (
            "h-5 w-5 rounded border-border text-brand-blue focus:ring-brand-blue"
        )
