from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .forms import AddPostForm, CommentForm
from .models import Post, Comment
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/add_comment.html'

    def get_success_url(self):
        '''URL to redirect to when the form is successfully validated'''
        return reverse_lazy('post:post', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.get(pk=self.kwargs['pk'])
        return context


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'post/delete_comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        '''URL to redirect to when the form is successfully validated'''
        return reverse_lazy('post:post', args=[self.kwargs.get('post_id')])

    def get_object(self):
        '''
        Return the object the view is displaying if user is an author of a comment
        else return 403
        '''
        comment = Comment.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        if self.request.user != comment.user:
            raise PermissionDenied("You are not allowed here")
        return comment


class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'post/update_comment.html'
    pk_url_kwarg = 'comment_id'
    fields = ['body']

    def get_success_url(self):
        '''URL to redirect to when the form is successfully validated'''
        return reverse_lazy('post:post', args=[self.kwargs.get('post_id')])

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        comment = Comment.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        return { 'body': comment.body}
 
    def get_object(self):
        '''
        Return the object the view is displaying if user is an author of a comment
        else return 403
        '''
        comment = Comment.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        if self.request.user != comment.user:
            raise PermissionDenied("You are not allowed here")
        return comment
        