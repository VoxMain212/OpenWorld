from django.shortcuts import render, HttpResponse
from .forms import ArticleForm, FileArticleForm
import os
import json
import uuid


created_articles = {

}

if not os.path.exists('articles/'):
    os.makedirs('articles')

def load():
    for file in os.listdir('articles'):
        with open(f'articles\\{file}', 'r') as f:
            data = json.load(f)
            created_articles.setdefault(data['id'], data)

def add_article(article_data):
    with open(f'articles\\{article_data["id"]}', 'w') as f:        
        json.dump(article_data, f)
    created_articles.setdefault(article_data['id'], article_data)


load()


# Create your views here.
def index(req):
    theme = req.COOKIES.get('theme', 'light')

    resp = render(req, 'index.html', {'theme': theme})

    if 'theme' not in req.COOKIES:
        resp.set_cookie(
            'theme',
            'light',
            max_age=365 * 24 * 60 * 60,  # 1 год
            samesite='Lax'
        )
    return resp

def article(req):
    theme = req.COOKIES.get('theme', 'light')
    print(created_articles)
    resp = render(req, 'article.html', {'articles': created_articles.values(), 'theme': theme})

    if 'theme' not in req.COOKIES:
        resp.set_cookie(
            'theme',
            'light',
            max_age=365 * 24 * 60 * 60,  # 1 год
            samesite='Lax'
        )
    return resp

def create_article(req):
    theme = req.COOKIES.get('theme', 'light')

    resp = render(req, 'index.html', {'theme': theme})

    if 'theme' not in req.COOKIES:
        resp.set_cookie(
            'theme',
            'light',
            max_age=365 * 24 * 60 * 60,  # 1 год
            samesite='Lax'
        )

    if req.method == "POST":
        if 'title' in req.POST:
            form = ArticleForm(req.POST)
            if form.is_valid():
                data = form.cleaned_data
                data['id'] = uuid.uuid4().hex
                add_article(data)
        else:
            form  = FileArticleForm(req.POST, req.FILES)
            if form.is_valid():
                file = req.FILES['file']
                content = file.read()
                try:
                    data = json.loads(content)
                except:
                    return "Not true"
                #TODO заменить заглушку
                if 'id' in data:
                    del data['id']
                    data['id'] = uuid.uuid4().hex
                f = 1

                fields = ['title', 'category', 'tags', 'content']
                for field in fields:
                    f *= field in data
                    if not f:
                        break
                print(data)
                if f:
                    print('added')
                    add_article(data)

    return render(req, 'create_article.html', {'theme': theme})


def get_all_actricles(req):
    http_response = HttpResponse(json.dumps(created_articles), content_type='application/json')
    http_response['Content-Disposition'] = f'attachment; filename="all_articles.json"'
    return http_response

def detail(req, article_id: str):
    article = created_articles[article_id]
    return render(req, 'article_detail.html', {'article': article})
