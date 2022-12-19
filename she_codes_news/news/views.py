from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import NewsStory
from .forms import StoryForm, FilterForm

class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'all_stories'

    def get_queryset(self):
        '''Return all news stories.'''
        qs = NewsStory.objects.all()
        form = FilterForm(self.request.GET)
        order_by = "-pub_date"
        if form.is_valid():
            order = form.cleaned_data.get('order')
            if order == "oldfirst":
                order_by = "pub_date"

            if author := form.cleaned_data.get('author'):
                qs = qs.filter(author=author)

            if search := form.cleaned_data.get('search'):
                qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search))

        return qs.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_stories'] = NewsStory.objects.all().order_by('-pub_date')[:4]
        context['form'] = FilterForm(self.request.GET)
        return context


class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = 'story'


class AddStoryView(generic.CreateView):
    form_class = StoryForm
    context_object_name = 'storyForm'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StoryEditView(generic.UpdateView):
    model = NewsStory
    fields = ['title', 'pub_date', 'content']

    def get_success_url(self) -> str:
        return reverse_lazy('news:story', kwargs={"pk":self.kwargs['pk']})

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            raise qs.model.DoesNotExist
        qs = qs.filter(author=self.request.user)
        return qs

class StoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = NewsStory
    success_url = reverse_lazy('news:index')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)

def like(request, pk):
    news_story = get_object_or_404(NewsStory, pk=pk)
    if news_story.favorited_by.filter(username=request.user.username).exists():
        news_story.favorited_by.remove(request.user)
    else:
        news_story.favorited_by.add(request.user)
    return redirect(reverse_lazy('news:story', kwargs={'pk':pk}))