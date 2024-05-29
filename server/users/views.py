from django.views import generic
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .forms import EditProfileForm


class ProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()

        request.user.changePhoto(request.FILES.get('photo'))
        request.user.save()
        return super().get(request, *args, **kwargs)
