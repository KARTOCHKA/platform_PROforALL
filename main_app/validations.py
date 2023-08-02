from rest_framework import serializers


class VideoValidator:
    """Валидация видео: возможно добавлять ссылку только на контент www.youtube.com"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('video')
        if video_url and 'www.youtube.com' not in video_url:
            raise serializers.ValidationError('Invalid video reference')
