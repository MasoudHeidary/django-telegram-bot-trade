from Bot.models import TelegramUser


def check_user(telegram_id):
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()

    try:
        return user.profile
    except:
        return False