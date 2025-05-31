import re

from django.db import models  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.core.validators import (MaxValueValidator,  # type: ignore
                                    MaxLengthValidator,
                                    MinValueValidator)
from django.core.exceptions import ValidationError  # type: ignore

from .constants import (MAX_NAME_LENGTH, MAX_SLUG_LENGTH, MAX_UNIT_LENGTH,
                        MAX_INGREDIENT_AMOUNT, MIN_INGREDIENT_AMOUNT,
                        MAX_COOKING_TIME, MIN_COOKING_TIME,
                        MAX_INGREDIENT_NAME_LENGTH)
from .querysets import AnnotatedRecipeQuerySet


def validate_slug(slug):
    if len(slug) > MAX_SLUG_LENGTH:
        raise ValidationError(
            f'Длина слага не должна превышать '
            f'{MAX_SLUG_LENGTH} символов.'
        )
    if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', slug):
        raise ValidationError(
            'Слаг содержит недопустимые символы.'
        )
    return slug


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_INGREDIENT_NAME_LENGTH,
                            validators=(MaxLengthValidator,),
                            verbose_name='Название',
                            unique=True)
    measurement_unit = models.CharField(max_length=MAX_UNIT_LENGTH,
                                        validators=(MaxLengthValidator,),
                                        verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH,
                            validators=(MaxLengthValidator,),
                            verbose_name='Название',
                            unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
    )
    text = models.TextField(verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты',
                                         blank=True,
                                         )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(MAX_COOKING_TIME),
            MinValueValidator(MIN_COOKING_TIME)),
        verbose_name='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    short_url = models.TextField(verbose_name='Короткая ссылка',
                                 blank=True, unique=True)
    objects = AnnotatedRecipeQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='recipes',
                                   verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(validators=(
        MaxValueValidator(MAX_INGREDIENT_AMOUNT),
        MinValueValidator(MIN_INGREDIENT_AMOUNT)),
        verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = (
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='unique_recipe_ingredient'),
        )

    def __str__(self):
        return (f'{self.ingredient.name}: {self.amount} '
                f'{self.ingredient.measurement_unit}')
