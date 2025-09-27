from django import forms


class ArticleForm(forms.Form):
    image_url = forms.URLField(max_length=250)
    title = forms.CharField(max_length=250)
    category = forms.CharField(max_length=250)
    tags = forms.CharField()
    content = forms.CharField()


class FileArticleForm(forms.Form):
    file = forms.FileField()