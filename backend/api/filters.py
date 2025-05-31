from django_filters import rest_framework as filters  # type: ignore

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if not value:
            return queryset.exclude(favorites__in=(user,))
        return queryset.filter(favorites__in=(user,))

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if not value:
            return queryset.exclude(shopping_cart__in=(user,))
        return queryset.filter(shopping_cart__in=(user,))
