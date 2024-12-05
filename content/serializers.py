from rest_framework import serializers
from content.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name")

    class Meta:
        model = Article
        fields = ["id", "headline", "content",
                  "last_update", "author", "picture", "author_name"]
