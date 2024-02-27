def build_media_url(request, media_file=None):
    if media_file is None:
        return ''
    return request.build_absolute_uri(media_file.url)
    