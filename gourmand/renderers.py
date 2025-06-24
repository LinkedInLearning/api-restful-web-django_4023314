from rest_framework import renderers

class TemplateHTMLFragmentRenderer(renderers.TemplateHTMLRenderer):
    media_type = 'text/html-fragment'
    format = 'html-fragment'
    charset = 'utf-8'
