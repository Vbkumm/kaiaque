from django.contrib import admin
from board.models import ExperienceModel, CategorySportModel, EquipmentModel, ExperiencePriceModel, \
    ExperiencePhotoGalleryModel, ExperienceCommentModel, ExperienceMeetPointModel
from django.contrib.gis.db import models as geo_models
from leaflet.forms.widgets import LeafletWidget


LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
    'map_width': '100%',
    'display_raw': 'true',
    'map_srid': 4326,
}

LEAFLET_FIELD_OPTIONS = {'widget': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}

FORMFIELD_OVERRIDES = {
    geo_models.PointField: LEAFLET_FIELD_OPTIONS,
}


class ExperienceMeetPointAdmin(admin.ModelAdmin):

    formfield_overrides = FORMFIELD_OVERRIDES


admin.site.register(ExperienceMeetPointModel)
admin.site.register(ExperienceModel)
admin.site.register(CategorySportModel)
admin.site.register(EquipmentModel)
admin.site.register(ExperiencePriceModel)
admin.site.register(ExperienceCommentModel)
admin.site.register(ExperiencePhotoGalleryModel)

