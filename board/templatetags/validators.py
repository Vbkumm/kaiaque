

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg', '.gif', '.jpeg', '.jpg', '.png', '.heic', '.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Arquivo não suportado!')

