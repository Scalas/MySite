from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
import logging

from ..models import Question

logger = logging.getLogger('pybo')


def index(request):
    logger.info('INFO 레벨로 출력')
    # page 수 가져오기
    # GET 방식으로 호출된 url 에서 자동으로 page 값을 가져온다.
    # 만약 page 값이 생략되어있다면 디폴드값으로 1을 지정한다.
    page = request.GET.get('page', '1')

    # 검색어
    # 검색어가 따로 없다면 디폴트로 ''를 설정
    kw = request.GET.get('kw', '')

    # 정렬기준
    # 디폴트값은 최신순
    so = request.GET.get('so', 'recent')

    # 게시글 리스트
    # 정렬기준에 따라 정렬
    if so == 'recommended': # 추천순
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':   # 인기순(답글갯수순)
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:                   # 최신순
        question_list = Question.objects.order_by('-create_date')

    # 검색어 처리
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                 # 제목검색
            Q(content__icontains=kw) |                 # 내용검색
            Q(author__username__icontains=kw) |        # 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답글 글쓴이 검색
        ).distinct()

    # 한 페이지에 10개씩 보이도록 페이징 처리
    paginator = Paginator(question_list, 10)

    # page 값에 해당하는 페이지를 가져온다
    page_obj = paginator.get_page(page)

    # 페이징 처리된 게시글 리스트를 넘겨주고 렌더링
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
