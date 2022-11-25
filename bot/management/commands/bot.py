from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Телеграм бот"

    def handle(self, *args, **options):
        from bot.views import bot
        print('bot is ready')

        bot.polling(none_stop=True, interval=0)
