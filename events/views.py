from django.views.generic import DetailView, ListView

from .models import Event


# Create your views here.
class IndexView(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.all()


class DetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        form = kwargs.pop('form', None)
        if form:
            context['form'] = form
        else:
            context['form'] = self.object.make_registration_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.sign_up:
            form = self.object.make_registration_form().__call__(data=request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        self.get_object().add_event_attendance(user=form.cleaned_data['user'], email=form.cleaned_data['email'],
                                               anonymous=form.cleaned_data['anonymous'], preferences=form.cleaned_data)
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        print(form.data)
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
