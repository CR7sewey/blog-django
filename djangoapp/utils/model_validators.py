from django.core.exceptions import ValidationError


def validate_png(image):
    if not image.name.lower().endswith('.png'):
        # not png
        raise ValidationError('The image needs to be .png')
