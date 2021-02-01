from django import http
from django.urls import reverse
from django.views.generic import DeleteView

from pages.models import Page


class PageDeleteView(DeleteView):
    template_name = 'utils/delete_view.html'
    model = Page

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return http.HttpResponseRedirect(success_url)
        else:
            return http.HttpResponseForbidden("Cannot delete other's pages")

    def get_success_url(self):
        return reverse("pages:page_list")
