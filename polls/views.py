"""Views for the polls application."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question


class IndexView(generic.ListView):
    """Poll index page that show the latest question list."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


def show_detail(request, pk):
    """Question detail page show the question text and choice to vote."""
    question = get_object_or_404(Question, pk=pk)
    if not question.can_vote():
        messages.error(
            request,
            f'Error: poll "{question.question_text}" is no longer publish.'
        )
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    """Result page that show the results for each question."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Increase the result of vote and save it if the question can vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )
