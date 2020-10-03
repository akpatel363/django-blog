from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, FormView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .forms import CommentForm, SearchForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 12
    template_name = 'blog/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if (self.kwargs.get('tag_slug') != None):
            qs = qs.filter(tags__slug__in=[self.kwargs['tag_slug']])
        return qs.select_related('author').prefetch_related('tags')


class PostDetail(View):
    def get(self, request, *args, **kwargs):
        return PostDetailView.as_view()(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return PostCommentView.as_view()(request, *args, **kwargs)


class PostCommentView(SingleObjectMixin, FormView):
    template_name = "blog/post_detail.html"
    model = Post
    queryset = Post.published.all().select_related(
        'author').prefetch_related('tags', 'comments')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if(form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self, *args):
        date = self.object.created
        return reverse('blog:post_detail', kwargs={'year': date.year, 'month': date.month, 'date': date.day, 'slug': self.object.slug})


class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    queryset = Post.published.all().select_related(
        'author').prefetch_related('comments', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_posts"] = Post.published.filter(tags__in=self.object.tags.values_list(
            'id', flat=True)).exclude(id=self.object.id).annotate(similar_tags=Count('tags')).order_by('-similar_tags', '-created')
        context["form"] = CommentForm()
        return context


class SearchView(ListView):
    context_object_name = 'results'
    paginate_by = 12
    template_name = 'blog/search.html'

    def get_queryset(self):
        results = []
        if ('query' in self.request.GET):
            results = Post.published.annotate(
                search=SearchVector('title', 'body')).filter(search=self.request.GET['query'])
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'query' in self.request.GET:
            context["form"] = SearchForm(self.request.GET)
            context['query'] = self.request.GET['query']
        else:
            context["form"] = SearchForm()
        return context
