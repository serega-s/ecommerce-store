from django.views import generic


class FrontPageView(generic.TemplateView):
    template_name = 'core/frontpage.html'
