from django import forms

css_class = {
    'class': 'form-control',
    'style': 'max-width: 350px'
}
class SearchCandidate(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Prénom",
        widget=forms.TextInput(attrs=css_class)
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nom",
        widget=forms.TextInput(attrs=css_class)
    )