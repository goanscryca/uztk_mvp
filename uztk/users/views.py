from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from uztk.app.models import CameraToTourniquetLock, TourniquetLock
from django.http import HttpResponseRedirect

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def get_context_data(self, **kwargs):
        """Получение данных для отображения"""
        user = self.request.user
        cameras = user.cameras.all()
        
        context = super(UserDetailView, self).get_context_data(**kwargs)
        camera_context = []
        locks = []
        for camera in cameras:
            
            tourniquets = CameraToTourniquetLock.objects.filter(cameras__in=[camera.id]).all()
            for lock in tourniquets:
                locks.append({
                    "id": lock.tourniquet.id,
                    "uuid": lock.tourniquet.uuid,
                    "lock_type": lock.tourniquet.get_lock_type_display(),
                    "state": lock.tourniquet.get_state_display(),
                    "ip_address": lock.tourniquet.ip_address,
                    "location": lock.tourniquet.location
                    })
            
            camera_context.append(
                {
                    "id": camera.id,
                    "uuid": camera.uuid,
                    "type": camera.camtype,
                    "location": camera.location,
                    "ip_address": camera.ip_address,
                    "camtype": camera.get_camtype_display()
                }
            )
        context['cameras'] = camera_context
        context['locks'] = locks
        return context

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def lock_control(request, lock_id):
    """Управление турникетами/замками"""
    lock = TourniquetLock.objects.get(id__exact=lock_id)
    lock.state = TourniquetLock.OPENED if lock.state == TourniquetLock.CLOSED else TourniquetLock.CLOSED
    lock.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])