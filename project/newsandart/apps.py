from django.apps import AppConfig
import redis


class NewsandartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsandart'

    def ready(self):
        from . import signals

red = redis.Redis(
    host="redis-19191.c294.ap-northeast-1-2.ec2.cloud.redislabs.com",
    port=19191,
    password="dZKu636dUB85IYAnrnwWDhtCIJ7Okuwo"
)