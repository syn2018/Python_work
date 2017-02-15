from django.http import HttpResponseRedirect, HttpResponse, Http404 # normal response, and error response 
from django.template import loader
from django.shortcuts import render, render_to_response, get_list_or_404, get_object_or_404
from django.urls import reverse # I don't know what this library does
# Database input imports
# Testing student 
from django.views import generic 
from .models import Question, Choice, Student

# Each view is responsible for doing one of two things - returning
# a HttpResponse object containing the content for the requested
# page, or raising an exception 

class IndexView(generic.ListView):
    template_name = 'site1/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions """
        return Question.objects.order_by('-pub_date')[:5]

class ScienceView(generic.ListView):
    template_name = 'Science/index.html'

class DetailView(generic.DetailView):
    model = Question
    template_name = 'site1/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'site1/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'site1/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('site1/results', args=(question.id,)))
