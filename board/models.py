from builtins import super, int
from PIL import Image
from django.db import models
from django.utils.html import mark_safe
from markdown import markdown
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.gis.db import models as geomodels
from .templatetags.validators import validate_file_extension


# Create your models here.


class CategorySportModel(models.Model):
    category_sport = models.CharField('Defina uma categoria de esporte para sua experiência!', max_length=100, unique=True, )
    author_category = models.ForeignKey(User, on_delete=models.CASCADE)
    category_published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_sport


class ExperienceModel(models.Model):
    FACIL = '1'
    MEDIO = '2'
    DIFICIL = '3'
    EXPERT = '4'
    MINUTOS = 'mi'
    HORA = 'ho'
    DIA = 'di'
    SEMANA = 'se'
    LOCATOR_YES_NO_CHOICES = ((None, ''), (True, 'Sim'), (False, 'Não'))
    DIFFICULTY_LEVEL = ((None, ''), (FACIL, 'Facil'), (MEDIO, 'Medio'), (DIFICIL, 'Dificil'), (EXPERT, 'Expert'),)
    DURATION_METHOD = ((MINUTOS, 'Minuto'), (HORA, 'Hora'), (DIA, 'Dia'), (SEMANA, 'Semana'),)
    experience_title = models.CharField(max_length=150, unique=True, )
    category_sport = models.ForeignKey(CategorySportModel, default=1, verbose_name="category", on_delete=models.SET_DEFAULT)
    experience_equipment = models.BooleanField('Precisa de algum equipamento?', choices=LOCATOR_YES_NO_CHOICES, max_length=3, default=None,)
    experience_people = models.PositiveIntegerField('Quantas pessoas podem realizar a atividade?',)
    experience_supervisor = models.BooleanField('O anfitrião precisa acompanhar durante a atividade?', choices=LOCATOR_YES_NO_CHOICES, max_length=3, default=None,)
    experience_difficulty = models.CharField('Qual nivel de dificuldade?', choices=DIFFICULTY_LEVEL, max_length=1, default=None, )
    experience_age = models.PositiveIntegerField('Qual idade minima?',)
    experience_pet = models.BooleanField('Animais de estimação são bem vindos?',choices=LOCATOR_YES_NO_CHOICES, max_length=3, default=None,)
    experience_duration = models.DecimalField('Qual tempo de duração?',null=True, max_digits=8, decimal_places=2,)
    experience_duration_method = models.CharField('', choices=DURATION_METHOD, max_length=2,  default=None, )
    experience_value = models.BooleanField('A experiencia é cobrada?', choices=LOCATOR_YES_NO_CHOICES, max_length=3, default=None,)
    experience_published = models.DateTimeField(auto_now_add=True)
    experience_description = models.CharField('Descreva a experiência!', max_length=800)
    author_experience = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "experiences"
        verbose_name = "experience"

    def __str__(self):
        return self.experience_title

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.experience_description, safe_mode='escape'))

    def get_absolute_url(self):
        return reverse('experience_detail', kwargs={'pk': self.pk})


class ExperiencePhotoGalleryModel(models.Model):
    experience = models.ForeignKey(ExperienceModel, related_name='e_photos', default=1, on_delete=models.SET_DEFAULT)
    experience_photo = models.FileField('Adicione fotos a experiência!', upload_to="img/experience/",
                                        validators=[validate_file_extension],
                                        null=True, blank=True, )
    author_photo = models.ForeignKey(User, on_delete=models.CASCADE)
    photo_published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "e_photos"
        verbose_name = "e_photo"


class EquipmentModel(models.Model):
    LOCATOR_YES_NO_CHOICES = ((None, ''), (True, 'Sim'), (False, 'Não'))
    experience = models.ForeignKey(ExperienceModel, related_name='equipments', default=1, on_delete=models.SET_DEFAULT)
    equipment_title = models.CharField('Nome do equipamento:',max_length=150, )
    equipment_availability = models.BooleanField('Você disponibiliza o equipamento?', choices=LOCATOR_YES_NO_CHOICES, max_length=3, default=None, )
    equipment_picture = models.ImageField('Uma imagem do equipamento!', upload_to="img/equipment/", null=True,
                                          blank=True, )
    equipment_description = models.CharField('Descreva o equipamento!', max_length=800, null=True, blank=True, )

    class Meta:
        verbose_name_plural = "equipments"
        verbose_name = "equipment"

    def __str__(self):
        return self.equipment_title

    def save1(self):

        super(EquipmentModel, self).save()
        if not self.id:
            return
        else:
            if self.equipment_picture:

                im1 = Image.open(self.equipment_picture)
                (width, height) = im1.size
                if width > 1200:
                    if 1000 / width < 1000 / height:
                        factor = 1000 / height
                    else:
                        factor = 1000 / width

                    size = (int(width * factor), int(height * factor))
                    im1 = im1.resize(size, Image.ANTIALIAS)
                    im1.save(self.equipment_picture.path, optimize=True)


class ExperiencePriceModel(models.Model):
    POR_PESSOA = 'pe'
    POR_ATIVIDADE = 'ac'
    POR_HORA_PESSOA = 'hp'
    POR_HORA_ATIVIDADE = 'ha'
    PRICE_METHOD = ((None, ''), (POR_PESSOA, 'Por pessoa'), (POR_ATIVIDADE, 'Por atividade'), (POR_HORA_PESSOA, 'Por hora/pessoa'),
    (POR_HORA_ATIVIDADE, 'Por hora/atividade'),)
    experience = models.ForeignKey(ExperienceModel, related_name='e_prices', default=1, on_delete=models.SET_DEFAULT)
    experience_price = models.DecimalField('Qual valor?', null=True, max_digits=8, decimal_places=2, )
    experience_price_method = models.CharField('Como é cobrado?', choices=PRICE_METHOD, max_length=2, default=None, )

    class Meta:
        verbose_name_plural = "e_prices"
        verbose_name = "e_price"


class ExperienceCommentModel(models.Model):
    PESSIMO = '1'
    RUIM = '2'
    MEDIO = '3'
    BOM = '4'
    MARAVILHA = '5'
    STARS_LEVEL = ((None, ''), (PESSIMO, 'Pessima'), (RUIM, 'Ruim'), (MEDIO, 'Mais ou menos'), (BOM, 'Bom'), (MARAVILHA, 'Maravilha'),)
    experience = models.ForeignKey(ExperienceModel, related_name='e_comments', default=1, on_delete=models.SET_DEFAULT)
    comment_description = models.CharField('Descreva seu comentario!', max_length=500, )
    comment_star = models.CharField('Qual sua avalição?', choices=STARS_LEVEL, max_length=1, default=MARAVILHA, )
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "e_comments"
        verbose_name = "e_comment"


class ExperienceMeetPointModel(models.Model):

    experience = models.ForeignKey(ExperienceModel, related_name='e_locations', default=1, on_delete=models.SET_DEFAULT)
    e_location = geomodels.PointField('Indique a localização geografica no mapa', srid=4326)
    e_address = geomodels.CharField('Qual o endereço do ponto de encontro para inicio da experiência?', max_length=100)
    e_city = geomodels.CharField('Qual a cidade?', max_length=50)

    class Meta:
        verbose_name_plural = "e_locations"
        verbose_name = "e_location"
