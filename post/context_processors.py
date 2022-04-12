from .models import Category
from .forms import SearchForm


def forms_processor(request):
    search_form = SearchForm()
    return {"search_form": search_form}


def all_categories(request):
    categories = Category.objects.all()
    return {"all_categories": categories}
