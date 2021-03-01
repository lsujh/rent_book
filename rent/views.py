from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import BookRent
from .forms import BookRentForm


class RentListView(ListView):
    models = BookRent
    template_name = "rent/rent_list_view.html"
    queryset = BookRent.objects.all()[:20]


class NewRent(CreateView):
    model = BookRent
    form_class = BookRentForm
    template_name = "rent/new_rent.html"
    success_url = reverse_lazy("rent:rent_list")
