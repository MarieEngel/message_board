from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddPostForm, CommentForm, SearchForm

from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Comment
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
@login_required
def home(request):
    post_list = Post.objects.all().order_by("-id")
    context = {"post_list": post_list}
    return render(request, "post/home.html", context)

@login_required
def post(request, id):
    post = Post.objects.get(id=id)
    context = {"post": post}
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
    if request.method == "POST":
        post.delete()
        return redirect("/")

    return render(request, "post/delete_post.html", {'post': post})


@login_required
def update_post(request, id):
    success_message = ""
    form = None
    post = get_object_or_404(Post, id=id)
    form = AddPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            success_message = "You have successfully updated your post."
            return redirect("/")
    context = {"form": form, "post": post, "success_message": success_message}
    return render(request, "post/update_post.html", context)


class BelongsToTheUserMixin(PermissionRequiredMixin):
    """Mixin for views to only allow the owners of the object to access them"""
    def has_permission(self):
        return self.request.user == self.get_object().user


class RedirectToPostMixin:
    def get_success_url(self):
        url = reverse_lazy('post:post', kwargs={'id': self.object.post_id})
        if not isinstance(self, DeleteView):
            url += f"#comment-{self.object.id}"
        return url


class AddCommentView(RedirectToPostMixin, LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.filter(pk=self.kwargs['pk']).first()
        return context


def search(request):
    success_message = ""
    search_results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        is_valid = form.is_valid()
        if is_valid:
            search_term = request.GET["query"]
            search_results = Post.objects.filter(
                Q(title__icontains=search_term)
                | Q(body__icontains=search_term)
            )
            category = form.cleaned_data.get("categories")
            print(category)
            if category == 'All':
                search_results = Post.objects.filter(
                Q(title__icontains=search_term)
                | Q(body__icontains=search_term)
            )
            else:
                search_results = Post.objects.filter(
                Q(title__icontains=search_term, category__name=category)
                | Q(body__icontains=search_term, category__name=category)
            )
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

class DeleteCommentView(RedirectToPostMixin, LoginRequiredMixin, BelongsToTheUserMixin, DeleteView):
    model = Comment
    template_name = 'post/delete_comment.html'


class UpdateCommentView(RedirectToPostMixin, LoginRequiredMixin, BelongsToTheUserMixin, UpdateView):
    model = Comment
    template_name = 'post/update_comment.html'
    fields = ['body']
