from datetime import datetime
from urllib.parse import quote, urlencode
import re
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from ctfpad.forms import (
    CategoryCreateForm,
    CtfCreateUpdateForm,
)
from ctfpad.models import Ctf
from ctfpad.helpers import (
    ctftime_fetch_running_ctf_data,
    ctftime_fetch_next_ctf_data,
    ctftime_get_ctf_info,
    ctftime_parse_date
)


class CtfListView(LoginRequiredMixin, ListView):
    model = Ctf
    template_name = "ctfpad/ctfs/list.html"
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    paginate_by = 10
    ordering = ["-id"]
    extra_context = {
        "ctftime_ctfs": ctftime_fetch_running_ctf_data() + ctftime_fetch_next_ctf_data(),
    }


class CtfCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ctf
    template_name = "ctfpad/ctfs/create.html"
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    form_class = CtfCreateUpdateForm
    initial = {
        "name": "",
        "url": "",
        "description": "",
        "start_date": "",
        "end_date": "",
        "flag_prefix": "",
        "team_login": "",
        "team_password": "",
    }
    success_message = "CTF '%(name)s' created"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})


    def form_valid(self, form):
        if Ctf.objects.filter(name=form.instance.name).count() > 0:
            form.errors["name"] = "CtfAlreadyExistError"
            return render(self.request, self.template_name, {'form': form})
        return super().form_valid(form)


    def get_success_url(self):
        return reverse("ctfpad:ctfs-detail", kwargs={'pk': self.object.pk})


class CtfImportView(CtfCreateView):
    def get(self, request, *args, **kwargs):
        initial = {}
        initial["name"] = request.GET.get("name") or ""
        initial["url"] = request.GET.get("url") or ""

        rx = re.match('https://ctftime.org/.+/(\d+)', request.GET.get("url"))
        if rx:
            ctf = ctftime_get_ctf_info(rx.group(1))

            initial["ctftime_id"] = ctf["id"]
            initial["name"] = ctf["title"]
            initial["url"] = ctf["url"]
            initial["description"] = ctf["description"]
            initial["start_date"] = ctftime_parse_date(ctf["start"])
            initial["end_date"] = ctftime_parse_date(ctf["finish"])

        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})


class CtfDetailView(LoginRequiredMixin, DetailView):
    model = Ctf
    template_name = "ctfpad/ctfs/detail.html"
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    extra_context = {
        "add_category_form": CategoryCreateForm(),
    }


class CtfUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ctf
    form_class = CtfCreateUpdateForm
    template_name = "ctfpad/ctfs/create.html"
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    success_message = "CTF '%(name)s' updated"

    def get_success_url(self):
        return reverse("ctfpad:ctfs-detail", kwargs={'pk': self.object.pk})


class CtfDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Ctf
    success_url = reverse_lazy('ctfpad:dashboard')
    template_name = "ctfpad/ctfs/confirm_delete.html"
    login_url = "/users/login/"
    redirect_field_name = "redirect_to"
    success_message = "CTF deleted"

