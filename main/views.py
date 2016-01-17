from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from watchlog.models import Watchlog
from watchlist.models import Watchlist


class Index(TemplateView):
    """
    Index View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/main.html"

    def get_context_data(self, **kwargs):
        """
        Fill up the context array.

        Args:
            **kwargs: Parameters that where given to the view.

        Returns:
            dict: Context dictionary with all values.
        """
        context = super(Index, self).get_context_data(**kwargs)
        context['wlog_list'] = list(Watchlog.objects.order_by(
            '-episode__series', '-added').distinct('episode__series'))[:12]
        context['wlog_list'].sort(key=lambda x: x.added, reverse=True)
        return context


class About(TemplateView):
    """
    About View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/about.html"


class Dummy(TemplateView):
    """
    Index View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/dummy.html"


class SignIn(TemplateView):
    """
    Index View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/sign-in.html"


class Contact(TemplateView):
    """
    Contact View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/contact.html"


class Help(TemplateView):
    """
    Contact View.
    template_name : takes the given template and rendes it to the view.
    """
    template_name = "main/help.html"


class Overview(LoginRequiredMixin, TemplateView):
    """
    Overview View.
    template_name : takes the given template and rendes it to the view.
    @login_required : this view can only be accessed when the user is
        logged in(signed in).
    login_url : is the url wich is taken when the user is not logged in.
    """
    template_name = "main/overview.html"

    def get_context_data(self, **kwargs):
        """
        Fill up the context array.

        Args:
            **kwargs: Parameters that where given to the view.

        Returns:
            dict: Context dictionary with all values.
        """
        user = self.request.user
        context = super(Overview, self).get_context_data(**kwargs)
        context['wlist_list'] = list(Watchlist.objects.filter(
            user=user).order_by('-added'))[:6]
        context['wlog_list'] = list(Watchlog.objects.filter(
            user=user).order_by(
            'episode__series', '-added').distinct('episode__series'))[:6]
        context['wlog_list'].sort(key=lambda x: x.added, reverse=True)
        return context
