from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    # page 수 가져오기
    # GET 방식으로 호출된 url 에서 자동으로 page 값을 가져온다.
    # 만약 page 값이 생략되어있다면 디폴드값으로 1을 지정한다.
    page = request.GET.get('page', '1')

    # 게시글 리스트
    # 최근에 생성된 순으로 정렬
    question_list = Question.objects.order_by('-create_date')

    # 한 페이지에 10개씩 보이도록 페이징 처리
    paginator = Paginator(question_list, 10)

    # page 값에 해당하는 페이지를 가져온다
    page_obj = paginator.get_page(page)

    # 게시글 리스트로 page_obj 를 넘겨주고 렌더링
    context = {'question_list':page_obj}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()

    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
