from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

register = template.Library()


def get_admin_url(self):
    content_type = ContentType.objects.get_for_model(self.__class__)
    return reverse(
        "admin:%s_%s_change" % (content_type.app_label, content_type.model),
        args=(self.id,)
        )


@register.tag(name="edit_link")
def do_edit_link(parser, token):
    try:
        tag_name, element = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
            )
    return LinkNode(element)


class LinkNode(template.Node):
    def __init__(self, element):
        self.element = template.Variable(element)

    def render(self, context):
        try:
            actual_element = self.element.resolve(context)
            return mark_safe(
                u'''<a href="%s">Edit (admin)</a>''' % get_admin_url(
                    actual_element
                    )
            )
        except template.VariableDoesNotExist:
            return ''
