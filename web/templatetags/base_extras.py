from django import template


register = template.Library()


@register.simple_tag
def active_page(request, view_name):

    from django.core.urlresolvers import resolve, Resolver404
    path = resolve(request.path_info)
    if not request:
        return ""
    try:
        return "active" if "{0}:{1}".format(path.namespace, path.url_name) == view_name else "f"
    except Resolver404:
        return ""