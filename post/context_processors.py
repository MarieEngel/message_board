from .models import Category
from .forms import SearchForm

def all_categories(request):
    categories = Category.objects.all()
    return {'all_categories': categories}

def forms_processor(request):
    search_form = SearchForm()
    context = {'name_form': name_form}
    return context