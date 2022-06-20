
from django import forms
from .models import (ExperienceModel,
                     CategorySportModel,
                     EquipmentModel,
                     ExperiencePriceModel,
                     ExperienceCommentModel,
                     ExperiencePhotoGalleryModel,
                     ExperienceMeetPointModel,
                     )
from django.contrib.gis import forms as geo_forms
from leaflet.forms.widgets import LeafletWidget


class ExperienceUpdateForm(forms.ModelForm):
    experience_title = forms.CharField(label='Um titulo para sua atividade',
                                       widget=forms.TextInput(attrs={'placeholder': 'Ex. Surfar como um local!'})
                                       )
    category_sport = forms.ModelChoiceField(label='Selecione uma catergoria',
                                            queryset=CategorySportModel.objects.all(),
                                            empty_label="(Adicione uma nova caso não encotre-a)",
                                            required=False,
                                            initial=0,
                                            )
    experience_description = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 4, 'placeholder': 'Descreva sua experiência em 800 caracteres.'}
    ),
                                             max_length=800,
                                             help_text='The max length of the text is 800.'
                                             )

    class Meta:
        model = ExperienceModel
        fields = ['category_sport', 'experience_title', 'experience_equipment', 'experience_people',
                  'experience_supervisor', 'experience_difficulty', 'experience_age', 'experience_pet',
                  'experience_duration', 'experience_duration_method', 'experience_value', 'experience_description', ]


class ExperienceForm1(forms.ModelForm):
    experience_title = forms.CharField(label='Um titulo para sua atividade',
                                       widget=forms.TextInput(attrs={'placeholder': 'Ex. Surfar como um local!'})
                                       )
    category_sport = forms.ModelChoiceField(label='Selecione uma catergoria',
                                            queryset=CategorySportModel.objects.all(),
                                            empty_label="(Adicione uma nova caso não encotre-a)",
                                            required=False,
                                            initial=0,
                                            )

    class Meta:
        model = ExperienceModel
        fields = ['category_sport', 'experience_title', 'experience_equipment', ]


class ExperienceForm2(forms.ModelForm):

    class Meta:
        model = ExperienceModel
        fields = ['experience_people', 'experience_supervisor', 'experience_difficulty', 'experience_age', 'experience_pet', ]


class ExperienceForm3(forms.ModelForm):

    class Meta:
        model = ExperienceModel
        fields = ['experience_duration', 'experience_duration_method', 'experience_value', ]


class ExperienceForm4(forms.ModelForm):
    experience_description = forms.CharField(label='', widget=forms.Textarea(
                                  attrs={'rows': 4, 'placeholder': 'Descreva sua experiência em 800 caracteres.'}
                              ),
                              max_length=800,
                              help_text='The max length of the text is 800.'
                              )

    class Meta:
        model = ExperienceModel
        fields = ['experience_description', ]


class CategorySportForm(forms.ModelForm):

    class Meta:
        model = CategorySportModel
        fields = fields = ['category_sport', ]


class ExperiencePhotoGalleryForm(forms.ModelForm):

    class Meta:
        model = ExperiencePhotoGalleryModel
        fields = ['experience_photo']


class EquipmentForm1(forms.ModelForm):

    class Meta:
        model = EquipmentModel
        fields = ['equipment_availability', 'equipment_title', 'equipment_picture' ]


class EquipmentForm2(forms.ModelForm):
    equipment_description = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 4, 'placeholder': 'Descreva o equipamento necessário indicando o que esta incluso. Exemplo tipo de roupa.'}
    ),
                                             max_length=800,
                                             help_text='The max length of the text is 800.'
                                             )

    class Meta:
        model = EquipmentModel
        fields = ['equipment_description', ]


class ExperiencePriceForm(forms.ModelForm):

    class Meta:
        model = ExperiencePriceModel
        fields = ['experience_price', 'experience_price_method',]


class ExperienceCommentForm(forms.ModelForm):
    comment_description = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 4,
               'placeholder': 'Deixe seu comentario'}
    ),
                                            max_length=500,
                                            help_text='O maximo de caracters 500.')

    class Meta:
        model = ExperienceCommentModel
        fields = ['comment_description', 'comment_star']


LEAFLET_WIDGET_ATTRS = {
    'map_srid': 4326,
    'map_width': '100%',
    'default_lat': -0.0,
    'default_lon': -48.02096738,
    'default_zoom': 2,

}


class ExperienceMeetPointForm(geo_forms.ModelForm):

    class Meta:
        model = ExperienceMeetPointModel
        fields = ['e_location', 'e_address', 'e_city']
        widgets = {'e_location': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}
