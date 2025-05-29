from django.core.cache import cache  # type: ignore
from django.conf import settings  # type: ignore


class CacheResponseMixin:

    cache_timeout = settings.CACHE_TIMEOUT

    def get_queryset(self):
        if not self.cache_timeout:
            return super().get_queryset()
        cache_key = (f'drf:{self.cache_timeout}:{self.request.method}:'
                     f'{self.request.path_info}')
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        queryset = super().get_queryset()
        cache.set(cache_key, queryset, self.cache_timeout)
        return queryset
