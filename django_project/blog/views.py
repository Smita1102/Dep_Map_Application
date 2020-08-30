
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, reverse
from django.views import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random
from django import forms
from .forms import BookFormset
import json
import ast


#EMAIL
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from django.template.loader import render_to_string


from .models import Question, Choice, SetsAttempted,Book

btn_value = str()
set_id = int()
question_id = int()



class QuestionView(View):
    template_name = 'blog/mcq.html'

    def render_invalid_post(self, request, question, error_message):
        return render(request,
                      self.template_name, {
                          'question': question,
                          'error_message': error_message
                      },
                      status=400)

    def get(self, request):
        #session_key = request.session.session_key
        #question_type=request.session.btn_value
        #question = Question.objects.get_random(session_key)
        #question = Question.objects.get(question_type)
        if btn_value != None and btn_value != "":
            l_question_type = btn_value
            global set_id, question_id , question
            if set_id == 0:
                user_completed_sets=SetsAttempted.objects.filter(user_id=request.user, question_type=l_question_type).values("set_id").distinct()
                possible_sets = Question.objects.filter(question_type=l_question_type).exclude(set_id__in=user_completed_sets).values("set_id").distinct()
                if len(possible_sets) == 0:
                    possible_sets = Question.objects.filter(question_type=l_question_type).values("set_id").distinct()
                set_id = int(random.choice(possible_sets)['set_id'])
                print("user_completed_sets Sets-> ", user_completed_sets)
                print("Possible Sets-> ", possible_sets)
            question_id_count =  Question.objects.filter(set_id=set_id, question_type=l_question_type).count()
            print("Set ID-> ", set_id)
            print("Question Count-> ", question_id_count)
            l_set_id = set_id
            l_question_id = question_id
            print("Current Question ID-> ",l_question_id)
            if l_question_id > question_id_count:
                return render(request, self.template_name, {'question': None, 'list_choice': None})
            question=Question.objects.filter(question_type=l_question_type, 
                                        set_id=l_set_id,
                                        question_id=l_question_id).values("question_text","question_id","set_id","question_type")

            #print(question)
            _choices=Choice.objects.filter(question_type=""+l_question_type+"", 
                                        question_id=l_question_id, 
                                        set_id=l_set_id,
                                        is_valid= 'Y')

        #print(_choices)


        #question = question.object.get(btn_value==question_type.get(pk=question_id) )
        heading_message = 'Formset Demo'
        if request.method == 'GET':
            formset = BookFormset(request.GET or None)
        return render(request, self.template_name, 
            {
                'question': question[0], 
                'list_choice': _choices,
                'formset': formset,
                'heading': heading_message
                }
            )

    def post(self, request):
        global question_id
        pst_btn = request.POST.get('btn_click')
        question_reference = request.POST.get('question-id', 0)
        l_list_question_reference = list(question_reference.split('^'))
        question_type = l_list_question_reference[0]
        set_id = l_list_question_reference[1]
        _question_id = l_list_question_reference[2]
        print("BTN-PST= ",pst_btn)
        if(pst_btn == 'create'):
            if request.method == 'POST':
                formset = BookFormset(request.POST)
                if formset.is_valid():
                    for form in formset:
                        # extract name from each form and save
                        name = form.cleaned_data.get('name')
                        # save book instance
                        if name:
                            Book(name=name,
                                user_id=request.user,
                                question_id=_question_id,
                                question_type=question_type,
                                set_id=set_id).save()
                            
                            Choice(choice_text=name,
                                    question_id=question_id,
                                    set_id=set_id,
                                    question_type=question_type,
                                    is_valid='Y'
                                    ).save()
        elif(pst_btn == 'remove'):
            if request.method == 'POST':
                choice_id = request.POST.getlist('choice', 0)
                Choice.objects.filter(question_id=question_id, set_id=set_id,question_type=question_type, id__in=choice_id).update(is_valid='N')
        else:
            if(pst_btn== 1):
                choice_id = 0
            else:
                choice_id = request.POST.getlist('choice', 0)
            #user_id = request.user.pk

            
            print(choice_id, question_reference)
            model_obj = SetsAttempted(user_id=request.user, 
                                        set_id=set_id, 
                                        question_type=question_type,
                                        question_id=_question_id,
                                        Value=choice_id,
                                        datecreated=timezone.now()
                                        )

            model_obj.save()
            question_id = question_id + 1

            check = forms.BooleanField(required = True)
            
        return redirect('/blog/mcq')


       







from django.http import HttpResponse

@login_required
def home(request):
    qb = QuestionView
    global btn_value, set_id, question_id
    set_id = 0
    question_id = 1
    btn_value = request.GET.get('valuebutton')
    if(btn_value != None and btn_value != ""):
        print('Button Value'+str(btn_value))
        #return render(request, 'blog/mcq.html', context={"question":qb.get(qb, request)})
        return redirect('/blog/mcq')
    
    return render(request, 'blog/home.html')
  
def restart(request):
    request.session.flush()
    messages.add_message(request, messages.INFO, 'Here we go again! 🚀')
    return redirect(reverse('/blog/mcq'))
    #return redirect('users/login.html')
    #return render(request,'users/login.html',{'title':'home'})

	


def about(request):
	return render(request,'blog/about.html',{'title':'about'})




def index(request):

  if request.method == 'POST':
     message = request.POST['message']
     context={'name':'Rakshanda', 'email':'majorproject1108@gmail.com', 'message':message}
     template= render_to_string('blog/email.html', context)

     send_mail('Contact Form',
       template, 
       settings.EMAIL_HOST_USER,
       ['userfeedback1108@gmail.com'], 
       fail_silently=False)
  return render(request,'blog/index.html',{'title':'index'})

def create_normal(request):
    template_name = 'blog/create_normal.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    Book(name=name).save()
            # once all books are saved, redirect to book list view
            #return redirect('book_list')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })

def getQuestionIDName(q_id):
    query_questionname = Question.objects.filter(question_id=q_id).values('question_text')
    return (query_questionname[0]['question_text'])

def getChoiceName(c_id):
    query_choicename =  Choice.objects.filter(id=c_id).values('choice_text')
    return (query_choicename[0]['choice_text'])


def reform_graph(uid):
    gd = {"name":"Subjects"}
    subject_map = {
        'P': 'Physics',
        'M': 'Biology',
        'C': 'Chemistry'
    }
    children= []
    query_distinct_QuestionType = SetsAttempted.objects.filter(user_id=uid).values('question_type').distinct()
    #print(query_distinct_QuestionType)
    for value in query_distinct_QuestionType:
        question_type = value['question_type']
        obj_1_key = {"name":subject_map[question_type]}
        obj_1_children = []

        quest_distinct_QuestionID = SetsAttempted.objects.filter(user_id=uid, question_type=question_type).values('question_id').distinct()
        for value in quest_distinct_QuestionID:
            question_id = value['question_id']
            obj_2_key = {"name":getQuestionIDName(question_id)}
            obj_2_children = []

            quest_distinct_Choices = SetsAttempted.objects.filter(user_id=uid, question_type=question_type, question_id=question_id).values('Value').distinct()
            choice_list = []
            for value in quest_distinct_Choices:
                if value['Value'] == "0":
                    continue
                choice_list.extend(ast.literal_eval(value['Value']))
            #print("Choice List -> ", choice_list)

            for value in choice_list:
                obj_2_children.append({"name":getChoiceName(value)})

            obj_2_key["children"] = obj_2_children
            obj_1_children.append(obj_2_key)
        obj_1_key["children"] = obj_1_children
        children.append(obj_1_key)

    gd["children"]= children
    #print(gd)
    #gd = {"name":"flare","children":[{"name":"analytics","children":[{"name":"cluster","children":[{"name":"AgglomerativeCluster","size":3938},{"name":"CommunityStructure","size":3812},{"name":"HierarchicalCluster","size":6714},{"name":"MergeEdge","size":743}]},{"name":"graph","children":[{"name":"BetweennessCentrality","size":3534},{"name":"LinkDistance","size":5731},{"name":"MaxFlowMinCut","size":7840},{"name":"ShortestPaths","size":5914},{"name":"SpanningTree","size":3416}]},{"name":"optimization","children":[{"name":"AspectRatioBanker","size":7074}]}]}]}
    return gd


def graph_view(request):
    template_name = 'blog/graph.html'
    #graph_data = json.dumps({"name":"flare","children":[{"name":"analytics","children":[{"name":"cluster","children":[{"name":"AgglomerativeCluster","size":3938},{"name":"CommunityStructure","size":3812},{"name":"HierarchicalCluster","size":6714},{"name":"MergeEdge","size":743}]},{"name":"graph","children":[{"name":"BetweennessCentrality","size":3534},{"name":"LinkDistance","size":5731},{"name":"MaxFlowMinCut","size":7840},{"name":"ShortestPaths","size":5914},{"name":"SpanningTree","size":3416}]},{"name":"optimization","children":[{"name":"AspectRatioBanker","size":7074}]}]}]})
    graph_data = json.dumps(reform_graph(request.user))
    contex_object = {
        'title':'graph',
        'graph_data': graph_data
    }
    return render(request,
                    template_name,
                    contex_object
                )


