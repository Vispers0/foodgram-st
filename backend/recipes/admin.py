from django.contrib import admin  # type: ignore
from django.contrib.auth.models import Group  # type: ignore
from rest_framework.authtoken.admin import TokenAdmin  # type: ignore
from rest_framework.authtoken.models import Token  # type: ignore

from .models import Ingredient, Recipe, RecipeIngredient
from users.models import ShoppingCart, Favorite


TokenAdmin.verbose_name = 'Токен'
TokenAdmin.verbose_name_plural = 'Токены'
Token._meta.verbose_name = 'Токен'
Token._meta.verbose_name_plural = 'Токены'
admin.site.site_header = 'Административная панель'
admin.site.site_title = 'Административная панель'
admin.site.index_title = 'Административная панель'


class BaseAdmin(admin.ModelAdmin):
    actions = ('change_selected',
               'delete_selected')
    empty_value_display = '-пусто-'


class RecipeAdmin(BaseAdmin):
    list_display = ('name',
                    'author',
                    'favorite_count',
                    'image',
                    'text',
                    'cooking_time',
                    'short_url')
    fields = ('name',
              'author',
              'image',
              'text',
              'cooking_time',
              'short_url')
    search_fields = ('name', 'author__username')
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'

    def favorite_count(self, recipe):
        return recipe.favorites.count()


class IngredientAdmin(BaseAdmin):
    list_display = ('name', 'measurement_unit')
    fields = ('name', 'measurement_unit')
    search_fields = ('name',)
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class RecipeIngredientAdmin(BaseAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    fields = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name',)
    verbose_name = 'Ингредиент в рецепте'
    verbose_name_plural = 'Ингредиенты в рецепте'


class FavoriteAdmin(BaseAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')
    search_fields = ('user__username',)
    verbose_name = 'Избранное'
    verbose_name_plural = 'Избранное'


class ShoppingCartAdmin(BaseAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')
    search_fields = ('user__username',)
    verbose_name = 'Список покупок'
    verbose_name_plural = 'Список покупок'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.unregister(Group)
