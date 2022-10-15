from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", "group")

    def check_text(self):
        data = self.cleaned_data["text"]

        if data == '':
            raise forms.ValidationError(
                "Вы обязательно должны что-то написать!")

        return data
