from django.shortcuts import render, redirect, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = None

        if 'tag_slug' in self.kwargs:
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            context['posts'] = self.queryset.filter(tags__in=[tag])

        context['tag'] = tag
        return context


class PostDetailView(DetailView):
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'
    model = None

    def dispatch(self, request, *args, **kwargs):
        self.model = get_object_or_404(Post, slug=self.kwargs['post'], status='published',
                                       publish__year=self.kwargs['year'],
                                       publish__month=self.kwargs['month'],
                                       publish__day=self.kwargs['day'])
        comments = self.model.comments.filter(active=True)
        post_tags_ids = self.model.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(pk=self.model.pk)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

        if request.method == 'POST':
            new_comment = True
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = self.model
                new_comment.save()
        else:
            new_comment = None
            comment_form = CommentForm()
        return self.render_to_response({'post': self.model, 'comments': comments, 'comment_form': comment_form,
                                        'similar_posts': similar_posts, 'new_comment': new_comment})


class PostShareView(DetailView):
    template_name = 'blog/post/share.html'
    model = Post
    context_object_name = 'post'
    sent = False
    cd = {}

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status='published')

    def post(self, request, *args, **kwargs):
        form = EmailPostForm(request.POST)
        post = self.get_object()
        if form.is_valid():
            self.cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{self.cd["name"]} ({self.cd["email"]}) recommends you reading "{post.title}"'
            message = f'Read "{post.title}" at {post_url}\n\n{self.cd["name"]}\'s comments: {self.cd["comments"]}'
            send_mail(subject, message, 'admin@myblog.com', [self.cd['to']])
            self.sent = True
        return self.render_to_response({'post': self.get_object(), 'form': form, 'sent': self.sent, 'cd': self.cd})

    def get(self, request, *args, **kwargs):
        form = EmailPostForm()
        return self.render_to_response({'post': self.get_object(), 'form': form, 'sent': self.sent, 'cd': self.cd})


class PostSearchView(TemplateView):
    template_name = 'blog/post/search.html'

    def post(self, request, *args, **kwargs):
        if request.POST['phrase']:
            phrase = request.POST['phrase']
            searched_posts = [post for post in Post.published.all() if
                              phrase in post.body.lower() or phrase in post.title]
            total_results = len(searched_posts)
        else:
            return redirect('blog:post_list')
        return self.render_to_response(
            {'phrase': phrase, 'searched_posts': searched_posts, 'total_results': total_results})
