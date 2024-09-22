import datetime

from rest_framework import serializers

from reviews.constants import MAX_NAME_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        """
        Проверяет, что пользователь не оставил отзыв на это произведение ранее.
        """
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                    title_id=title_id, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('id', 'rating')
        model = Title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug
        }
        return representation

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли.')
        return value

    # def validate_name(self, value):
    #     if len(value) > MAX_NAME_LENGTH:
    #         raise serializers.ValidationError(
    #             f'Название произведения не может быть длиннее '
    #             f'{MAX_NAME_LENGTH} символов'
    #         )
