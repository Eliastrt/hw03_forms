from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        # На основе какой модели создаётся класс формы
        model = Post
        fields = ('text', 'group')

    def check_text(self):
        data = self.cleaned_data['text']

        if data == '':
            raise forms.ValidationError(
                'Вы обязательно должны что-то написать!')

        # Метод-валидатор обязательно должен вернуть очищенные данные,
        # даже если не изменил их
        return data
