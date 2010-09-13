#from django
from django import forms
from django.utils.translation import ugettext_lazy as _

#from piano
from models import Track


class TrackForm(forms.ModelForm):
    """ Track Form: form associated to the Track model """

    class Meta:
        model = Track
        #fields = ('coverart', 'composer', 'artist', 'category',
                  #'description', 'title')
        exclude = ('adder', 'track_mp4', 'track_webm', 'track_ogv',
                   'date_added')

    def __init__(self, user=None, *args, **kwargs):
        super(TrackForm, self).__init__(*args, **kwargs)
        self.user = user
        self.is_update = False

    def clean(self):
        """ Do validation stuff. """
        # if a track with that title already exists...
        if not self.is_update:
            if Track.objects.filter(title=self.cleaned_data['title'])\
                    .count() > 0:
                raise forms.ValidationError(_("There is already a track "
                                "with the same title in the pianostore."))
        return self.cleaned_data
