from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post


# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog/list.html'


def post_list(req, tag_slug=None):
    objs = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        objs = objs.filter(tags__in=[tag])

    paginator = Paginator(objs, 6)
    page = req.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'page': page, 'tag': tag}
    return render(req, 'blog/list.html', context)


def post_detail(req, year, month, date, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=date)
    comments = post.comments.filter(active=True)
    tag_list = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=tag_list).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    new_comment = None
    if req.method == 'POST':
        comment_form = CommentForm(data=req.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(req, 'blog/post_detail.html', context)


def post_share(req, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False
    if req.method == 'POST':
        form = EmailPostForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = req.build_absolute_uri(post.get_absolute_path())
            sub = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comments']}"
            send_mail(sub, message, 'clashofclanssmasher94@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(req, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})


def search_view(req):
    form = SearchForm()
    query = None
    results = []
    if 'query' in req.GET:
        form = SearchForm(req.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body')).filter(search=query)
    return render(req, 'blog/search.html', {'form': form, 'query': query, 'results': results})
