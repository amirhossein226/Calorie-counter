from django.shortcuts import render
from content.models import *
from content.serializers import ArticleSerializer
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse

# Create your views here.


def home(request):
    articles = Article.objects.defer("pub_date").select_related("author")
    return render(request, "content/index.html", {
        "arts": articles
    })


def articles(request, art_id):
    if request.method == "GET":
        if art_id:
            article = Article.objects.select_related("author").get(id=art_id)
            serializer = ArticleSerializer(article)

            return JsonResponse(serializer.data)
        else:
            return JsonResponse("Some Thing is Wrong!", status=404)

    elif request.method == "POST":
        print("request is Post")

    elif request.method == "PUT":
        print("request is PUT")
