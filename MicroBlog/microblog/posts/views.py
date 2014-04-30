# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from posts.models import Post
from posts.forms import PostForm


@login_required
def show_timeline(request):
    context = RequestContext(
        request,
        {'posts': Post.objects.order_by('-date_posted')}
    )
    return render_to_response('posts/timeline.html', context)


@login_required
def write_post(request):
    layout = 'vertical'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return show_timeline(request)
    else:
        form = PostForm()

    context = RequestContext(
        request,
        {'form': form,  # The Django form instance
         'layout': layout,  # For bootstrap toolkit UI rendering
         }
    )
    return render_to_response('posts/form.html', context)
