from rest_framework import serializers

from blog.models import Comment
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.StringRelatedField(many=True, read_only=True)
    saves = serializers.StringRelatedField(many=True, read_only=True)
    total_likes = serializers.SerializerMethodField()
    total_saves = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "likes",
            "total_likes",
            "saves",
            "total_saves",
        ]
        read_only_fields = [
            "id",
            "author",
            "likes",
            "total_likes",
            "saves",
            "total_saves",
        ]

    def get_total_likes(self, obj):
        return obj.total_likes()

    def get_total_saves(self, obj):
        return obj.total_saves()

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, source="name")
    likes = serializers.StringRelatedField(many=True, read_only=True)
    replies = serializers.SerializerMethodField()
    total_clikes = serializers.SerializerMethodField()
    comment_body = serializers.CharField(source="body")

    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "comment_body",
            "date_added",
            "likes",
            "total_clikes",
            "reply",
            "replies",
        ]
        read_only_fields = [
            "id",
            "post",
            "name",
            "date_added",
            "likes",
            "total_clikes",
            "replies",
        ]

    def get_total_clikes(self, obj):
        return obj.total_clikes()

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True, context=self.context).data

    def create(self, validated_data):
        request = self.context.get("request")
        post_id = self.context.get("post_id")
        validated_data["name"] = request.user
        validated_data["post_id"] = post_id
        return super().create(validated_data)
