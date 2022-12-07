from audioop import reverse
from django.shortcuts import render, get_object_or_404, reverse
from posting.models import Posting
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.views import View
# Create your views here.


def index(request):
    postings = Posting.objects.all().order_by('-id')
    context = {
        'postings': postings
    }

    return render(request, 'posting/index.html', context)


class SearchPosting(View):
    def get(self, request):
        query = self.request.GET.get('q')

        query_list = Posting.objects.filter(
            Q(judul__icontains=query) |
            Q(konten__icontains=query)
        )

        context = {
            'query_list': query_list,
        }

        return render(request, 'posting/search.html', context )

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class DetailPosting(generic.DetailView):
    model = Posting
    template_name = 'posting/detail.html'


class AddPost(LoginRequiredMixin,generic.CreateView):
    model = Posting
    fields = ['judul', 'date', 'image', 'konten']
    template_name = 'posting/addpost.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk})


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Posting
    fields = ['judul', 'image', 'konten']
    template_name = 'posting/addpost.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk': self.object.pk})


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = Posting
    template_name = 'posting/deletepost.html'
    success_url = reverse_lazy('index')