import folium

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.db.models import Q

from .forms import AddPostForm, CommentForm, SearchForm
from .models import Post, Comment


# Create your views here.
@login_required
def home(request):
    post_list = Post.objects.all().order_by("-id")
    context = {"post_list": post_list}
    return render(request, "post/home.html", context)


@login_required
def post(request, id):
    post = Post.objects.get(id=id)
    m = None
    if post.latitude:
        lat = post.latitude
        lon = post.longitude
        if post.postcode:
            popup = f"{post.city}, {post.postcode}"
        else:
            popup = f"{post.city}"
        m = folium.Map(location=[lat, lon], zoom_start=16)
        folium.Marker(
            location=[lat, lon],
            tooltip="Click for more",
            popup=popup,
        ).add_to(m)
        m = m._repr_html_()
    context = {"post": post, "map": m}
    return render(request, "post/post.html", context)


@login_required
def add_post(request):
    success_message = ""
    form = None
    if request.method == "POST":
        post = Post(user=request.user)
        form = AddPostForm(request.POST, request.FILES, instance=post)
        is_valid = form.is_valid()
        if is_valid:
            form.save()
            success_message = "Your post has been saved."
            return redirect("/")
        else:
            success_message = "The form needs fixes."

    else:
        form = AddPostForm()
    context = {"form": form, "success_message": success_message}
    return render(request, "post/add_post.html", context)


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if not request.user == post.user:
        raise PermissionDenied
    else:
        if request.method == "POST":
            post.delete()
            return redirect("/")
    return render(request, "post/delete_post.html", {"post": post})


@login_required
def update_post(request, id):
    success_message = ""
    form = None
    post = get_object_or_404(Post, id=id)
    form = AddPostForm(request.POST or None, request.FILES or None, instance=post)
    if not request.user == post.user:
        raise PermissionDenied
    else:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                success_message = "You have successfully updated your post."
                return redirect("/")
    context = {"form": form, "post": post, "success_message": success_message}
    return render(request, "post/update_post.html", context)


@login_required
def search(request):
    success_message = ""
    search_results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        is_valid = form.is_valid()
        if is_valid:
            search_term = request.GET["query"]
            vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            query = SearchQuery(search_term)
            results = (
                Post.objects.annotate(rank=SearchRank(vector, query))
                .filter(rank__gte=0.2)
                .order_by("-rank")
            )
            category = form.cleaned_data.get("categories")
            if category == "All":
                search_results = results
            else:
                search_results = results.filter(category__name=category)
            if search_results:
                success_message = f'Posts matching "{search_term}":'
            else:
                success_message = f"No results for {search_term}."
        else:
            success_message = "Form needs fixes!"
    else:
        form = SearchForm()
    context = {
        "form": form,
        "success_message": success_message,
        "search_results": search_results,
    }
    return render(request, "post/search.html", context)


class BelongsToTheUserMixin(PermissionRequiredMixin):
    """Mixin for views to only allow the owners of the object to access them"""

    def has_permission(self):
        return self.request.user == self.get_object().user


class RedirectToPostMixin:
    def get_success_url(self):
        url = reverse_lazy("post:post", kwargs={"id": self.object.post_id})
        if not isinstance(self, DeleteView):
            url += f"#comment-{self.object.id}"
        return url


class AddCommentView(RedirectToPostMixin, LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "post/add_comment.html"

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.filter(pk=self.kwargs["pk"]).first()
        return context


class DeleteCommentView(
    RedirectToPostMixin, LoginRequiredMixin, BelongsToTheUserMixin, DeleteView
):
    model = Comment
    template_name = "post/delete_comment.html"


class UpdateCommentView(
    RedirectToPostMixin, LoginRequiredMixin, BelongsToTheUserMixin, UpdateView
):
    model = Comment
    template_name = "post/update_comment.html"
    fields = ["body"]


def entry_not_found(request, exception, template_name="post/404.html"):
    return render(request, template_name, status=404)


def permission_denied(request, exception, template_name="post/403.html"):
    return render(request, template_name, status=403)


def server_error(request, template_name="post/500.html"):
    return render(request, template_name, status=500)
