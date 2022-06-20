import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from board.models import (CategorySportModel,
                          ExperienceModel,
                          EquipmentModel,
                          ExperiencePriceModel,
                          ExperienceCommentModel,
                          ExperiencePhotoGalleryModel,
                          ExperienceMeetPointModel,)
from board.forms import (CategorySportForm,
                         ExperienceUpdateForm,
                         ExperienceForm1,
                         ExperienceForm2,
                         ExperienceForm3,
                         ExperienceForm4,
                         EquipmentForm1,
                         EquipmentForm2,
                         ExperiencePriceForm,
                         ExperienceCommentForm,
                         ExperiencePhotoGalleryForm,
                         ExperienceMeetPointForm)
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from accounts.forms import Profile
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.


def my_view(request):
    profiles = Profile.objects.all()
    experiences = ExperienceModel.objects.all()

    return render(request, 'home.html', {'profiles': profiles, 'experiences': experiences,})


@method_decorator(login_required, name='dispatch')
class ExperienceWizardCreateView(SuccessMessageMixin, SessionWizardView):
    form_list = [ExperienceForm1, ExperienceForm2, ExperienceForm3, ExperienceForm4]
    template_name = 'board/experience_wizard_create.html'
    success_message = "Experiencia criada com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def done(self, form_list, **kwargs):
        # get merged dictionary from all fields
        form_dict = self.get_all_cleaned_data()
        experience = ExperienceModel()
        experience.author_experience = self.request.user
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(experience, k, v)
        experience.save()
        
        return HttpResponseRedirect(reverse("board:experience_detail", kwargs={'pk': experience.pk}))


class ExperienceDetailView(DetailView):
    model = ExperienceModel
    template_name = 'board/experience_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'experience'


@method_decorator(login_required, name='dispatch')
class ExperienceUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'board/experience_update.html'
    model = ExperienceModel
    form_class = ExperienceUpdateForm
    success_message = "Alterações feitas com sucesso!"

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperiencePhotoGalleryCreateView(SuccessMessageMixin, CreateView):

    def get(self, request, *args, **kwargs):
        experience = get_object_or_404(ExperienceModel, pk=self.kwargs.get('pk'))
        e_photos = ExperiencePhotoGalleryModel.objects.filter(experience_id=experience.pk)

        return render(self.request, 'board/experience_photo_gallery_create.html', {'experience': experience, 'e_photos': e_photos})

    def post(self, request, *args, **kwargs):
        experience = get_object_or_404(ExperienceModel, pk=self.kwargs.get('pk'))
        if request.method == 'POST':
            form = ExperiencePhotoGalleryForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                e_photo = form.save(commit=False)
                e_photo.author_photo = self.request.user
                e_photo.experience = experience
                e_photo.save()
                data = {'is_valid': True, 'name': e_photo.experience_photo.name, 'url': e_photo.experience_photo.url}

            else:
                data = {'is_valid': False}
            return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class ExperiencePhotoDeleteView(DeleteView):
    template_name = 'board/experience_photo_delete.html'
    model = ExperiencePhotoGalleryModel
    success_message = "Imagem deletada com sucesso!"

    def get_object(self, queryset=None, *args, **kwargs):
        e_photo_pk = self.kwargs.get("e_photo_pk")
        experience_pk = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return get_object_or_404(ExperiencePhotoGalleryModel, experience=experience_pk, id=e_photo_pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        experience_pk = self.kwargs['pk']
        e_photo_pk = self.kwargs['e_photo_pk']
        e_photo_pk = ExperiencePhotoGalleryModel.objects.get(experience=experience_pk, id=e_photo_pk)
        e_photo_pk.delete()

        return HttpResponseRedirect(reverse("board:experience_photo_gallery_create", kwargs={'pk': experience_pk}))


@method_decorator(login_required, name='dispatch')
class CategorySportCreateView(SuccessMessageMixin, CreateView):
    model = CategorySportModel
    template_name = 'board/category_sport_create.html'
    form_class = CategorySportForm
    success_message = "Categoria criada com sucesso!"

    def form_valid(self, model):
        model.instance.author_category = self.request.user
        return super().form_valid(model)

    def get_success_url(self):
        return '/'
        #return render(ExperienceWizardCreateView,)


@method_decorator(login_required, name='dispatch')
class EquipmentWizardCreateView(SuccessMessageMixin, SessionWizardView):
    form_list = [EquipmentForm1, EquipmentForm2, ]
    template_name = 'board/equipment_wizard_create.html'
    success_message = "Equipamento adicionado com sucesso!"
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def done(self, form_list, **kwargs):
        form_dict = self.get_all_cleaned_data()
        equipment = EquipmentModel()
        equipment.author_experience = self.request.user
        for k, v in form_dict.items():
            if k != 'tags':
                setattr(equipment, k, v)
        equipment.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        equipment.save()

        return HttpResponseRedirect(reverse("board:experience_detail", kwargs={'pk': equipment.experience.pk}))


@method_decorator(login_required, name='dispatch')
class ExperienceEquipmentUpdateView(SuccessMessageMixin, UpdateView):
    model = EquipmentModel
    fields = ['equipment_title', 'equipment_availability', 'equipment_picture', 'equipment_description']
    pk_url_kwarg = 'equipment_pk'
    context_object_name = 'equipment'
    template_name = 'board/experience_equipment_update.html'
    success_message = "Alterações no comentario feitas com sucesso!"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(experience__author_experience=self.request.user)

    def form_valid(self, form):
        equipment = self.get_form()
        equipment.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        equipment.save()
        form_list = [EquipmentForm1(data=self.request.POST, instance=self.object), EquipmentForm2(data=self.request.POST, instance=self.object), ]
        for form in form_list:
            if form.is_valid():
                return super().form_valid(form)
            else:
                return self.form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperienceEquipmentDeleteView(DeleteView):
    template_name = 'board/experience_equipment_delete.html'
    model = EquipmentModel
    success_message = "Equipamento deletado com sucesso!"

    def get_object(self, queryset=None, *args, **kwargs):
        equipment_pk = self.kwargs.get("equipment_pk")
        experience_pk = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return get_object_or_404(EquipmentModel, experience=experience_pk, id=equipment_pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        experience_pk = self.kwargs['pk']
        equipment_pk = self.kwargs['equipment_pk']
        e_equipment = EquipmentModel.objects.get(experience=experience_pk, id=equipment_pk)
        e_equipment.delete()

        return HttpResponseRedirect(reverse("board:experience_detail", kwargs={'pk': experience_pk}))


@method_decorator(login_required, name='dispatch')
class ExperiencePriceCreateView(SuccessMessageMixin, CreateView):
    model = ExperiencePriceModel
    template_name = 'board/experience_price_create.html'
    form_class = ExperiencePriceForm
    context_object_name = 'e_price'
    success_message = "Valor adicionado com sucesso!"

    def form_valid(self, model):
        model.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(model)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperiencePriceUpdateView(SuccessMessageMixin, UpdateView):
    model = ExperiencePriceModel
    form_class = ExperiencePriceForm
    pk_url_kwarg = 'e_price_pk'
    context_object_name = 'e_price'
    template_name = 'board/experience_price_update.html'
    success_message = "Alterações no valor feitas com sucesso!"

    def form_valid(self, form):
        e_price = self.get_form()
        e_price.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        e_price.save()
        form = ExperiencePriceForm(data=self.request.POST, instance=self.object)
        if form.is_valid():
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperienceMeetPointCreateView(SuccessMessageMixin, CreateView):
    model = ExperienceMeetPointModel
    template_name = 'board/experience_location_create.html'
    form_class = ExperienceMeetPointForm
    context_object_name = 'e_location'
    success_message = "Local adicionado com sucesso!"

    def form_valid(self, model):
        model.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(model)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperienceMeetPointUpdateView(SuccessMessageMixin, UpdateView):
    model = ExperienceMeetPointModel
    form_class = ExperienceMeetPointForm
    pk_url_kwarg = 'e_location_pk'
    context_object_name = 'e_location'
    template_name = 'board/experience_location_update.html'
    success_message = "Alterações na localização feitas com sucesso!"

    def form_valid(self, form):
        e_location = self.get_form()
        e_location.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        e_location.save()
        form = ExperienceMeetPointForm(data=self.request.POST, instance=self.object)
        if form.is_valid():
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperienceCommentCreateView(SuccessMessageMixin, CreateView):
    model = ExperienceCommentModel
    template_name = 'board/experience_comment_create.html'
    form_class = ExperienceCommentForm
    context_object_name = 'e_comment'
    success_message = "Comentario criado com sucesso!"

    def form_valid(self, model):
        model.instance.comment_author = self.request.user
        model.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(model)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperienceCommentUpdateView(SuccessMessageMixin, UpdateView):
    model = ExperienceCommentModel
    form_class = ExperienceCommentForm
    pk_url_kwarg = 'e_comment_pk'
    context_object_name = 'e_comment'
    template_name = 'board/experience_comment_update.html'
    success_message = "Alterações no comentario feitas com sucesso!"

    def form_valid(self, form):
        e_comment = self.get_form()
        e_comment.instance.experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        e_comment.save()
        form = ExperienceCommentForm(data=self.request.POST, instance=self.object)
        if form.is_valid():
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        experience = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return reverse("board:experience_detail", kwargs={'pk': experience.pk})


@method_decorator(login_required, name='dispatch')
class ExperienceCommentDeleteView(DeleteView):
    template_name = 'board/experience_comment_delete.html'
    model = ExperienceCommentModel
    success_message = "Comentario deletado com sucesso!"

    def get_object(self, queryset=None, *args, **kwargs):
        e_comment_pk = self.kwargs.get("e_comment_pk")
        experience_pk = ExperienceModel.objects.get(id=self.kwargs.get('pk'))
        return get_object_or_404(ExperienceCommentModel, experience=experience_pk, id=e_comment_pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        experience_pk = self.kwargs['pk']
        e_comment_pk = self.kwargs['e_comment_pk']
        e_comment_pk = ExperienceCommentModel.objects.get(experience=experience_pk, id=e_comment_pk)
        e_comment_pk.delete()

        return HttpResponseRedirect(reverse("board:experience_detail", kwargs={'pk': experience_pk}))
