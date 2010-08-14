#from django
from django import forms
from django.utils.translation import ugettext_lazy as _

#from piano
from models import Track


class TrackForm(forms.ModelForm):
    """
    Track Form: form associated to the Track model
    """

    def __init__(self, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)
        self.is_update = False

    def clean(self):
        """ Do validation stuff. """
        # title is mandatory
        if 'title' not in self.cleaned_data:
            return
        # if a track with that title already exists...
        if not self.is_update:
            if Track.objects.filter(title=self.cleaned_data['title']).\
                                                            count() > 0:
                raise forms.ValidationError(_("There is already this track "
                                              "in the library."))
        return self.cleaned_data

    class Meta:
        model = Track
        fields = ('composer', 'publisher', 'author', 'description', 'title')
