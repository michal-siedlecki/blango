import logging

from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from blog.models import Post

user_model = get_user_model()
register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def author_details(author, current_user):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ''

    if author == current_user:
        return format_html('<strong>me</strong>')

    if author.first_name and author.last_name:
        name = f'{author.first_name} {author.last_name}'
    else:
        name = f'{author.username}'

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html('</a>')
    else:
        prefix = ''
        suffix = ''

    return format_html('{}{}{}', prefix, name, suffix)


"""

from django import template

register = template.Library()


# Question 4: Register the tag

@register.simple_tag()
def comments_for_thing(thing):
    # Question 4: Implement code to render the comments for the Thing object below.
    # Sort the comments alphabetically by their content when fetching.

    comments = thing.comments.all()
    s = ''.join(["<li>" + x.content + "</li>" for x in comments])

    return f"<ul>{s}</ul>"


An optional approach for providing data based on current user's context
it's combined with
<small>By {% author_details_tag %} on {{ post.published_at|date:"M, d Y" }}</small>
in post-byline.html template
"""


@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context['request']
    current_user = request.user
    post = context['post']
    author = post.author

    if author == current_user:
        return format_html('<strong>me</strong>')

    if author.first_name and author.last_name:
        name = f'{author.first_name} {author.last_name}'
    else:
        name = f'{author.username}'

    if author.email:
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html('</a>')
    else:
        prefix = ''
        suffix = ''

    return format_html('{}{}{}', prefix, name, suffix)


@register.simple_tag
def row(extra_classes=''):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html('</div>')


@register.simple_tag
def col(extra_classes=''):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html('</div>')


@register.inclusion_tag('blog/post-list.html')
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)
    logger.debug('Loaded %d recent posts for post %d', len(posts), post.pk)
    return {'title': 'Recent Posts', 'posts': posts}
