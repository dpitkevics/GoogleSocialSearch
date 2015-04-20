from django import template

from Jooglin.settings import SITE_NAME, STATIC_URL

register = template.Library()


@register.simple_tag
def title(title_text):
    if len(title_text) > 0:
        return "%s - %s" % (title_text, SITE_NAME)

    return SITE_NAME


class StaticFile(template.Node):
    css_files = []
    js_files = []

    def __init__(self, render_type):
        self.render_type = render_type

    @staticmethod
    def make_css_tag(css_file):
        return '<link rel="stylesheet" type="text/css" href="%scss/%s" />' % (STATIC_URL, css_file)

    @staticmethod
    def make_js_tag(js_file):
        return '<script src="%sjs/%s"></script>' % (STATIC_URL, js_file)

    def render(self, context):
        static_file_string = ''

        if self.render_type == 'css':
            for css_file in self.css_files:
                static_file_string += self.make_css_tag(css_file)
        elif self.render_type == 'js':
            for js_file in self.js_files:
                static_file_string += self.make_js_tag(js_file)

        return static_file_string


@register.tag(name='render_css_files')
def render_css_files(parser, value):
    return StaticFile('css')


@register.tag(name='render_js_files')
def render_css_files(parser, value):
    return StaticFile('js')


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context.dicts[0][self.var_name] = value
        # context[self.var_name] = value
        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])