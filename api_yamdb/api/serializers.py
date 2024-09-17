from rest_framework import serializers
from reviews.models import Comment, Review, Title


class TitleReadSerializer(serializers.ModelSerializer):
    pass

    def get_rating(self, obj):
        """
        Получает средний рейтинг произведения.
        """
        return obj.rating


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Review.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            author = request.user
            if Review.objects.filter(title_id=title_id,
                                     author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Comment.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
