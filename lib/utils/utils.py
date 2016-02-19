import os, time

"""Utils here."""

def get_icon(full_path, path, filename):
    """Get icon, based on file name."""
    if not path:
        path = '/'
    TEXT_TYPE = ['doc', 'docx', 'txt', 'rtf', 'odf', 'text', 'nfo']
    LANGUAGE_TYPE = ['js', 'html', 'htm', 'xhtml', 'jsp', 'asp', 'aspx', 'php', 'xml', 'css', 'py', 'bat', 'sh', 'rb', 'java']
    AUDIO_TYPE = ['aac', 'mp3', 'wav', 'wma', 'm4p', 'flac', 'ac3']
    IMAGE_TYPE = ['bmp', 'gif', 'jpg', 'jpeg', 'png','svg', 'eps', 'ico', 'psd', 'psp', 'raw', 'tga', 'tif', 'tiff', 'svg']
    VIDEO_TYPE = ['mv4', 'bup', 'mkv', 'ifo', 'flv', 'vob', '3g2', 'bik', 'xvid', 'divx', 'wmv', 'avi', '3gp', 'mp4', 'mov', '3gpp', '3gp2', 'swf', 'mpg', 'mpeg']
    ARCHIVE_TYPE = ['7z', 'dmg', 'rar', 'sit', 'zip', 'bzip', 'gz', 'tar', 'bz2', 'ace']

    if os.path.isdir(full_path + path + "/" + filename):
        return 'folder-o'
    else:
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension in AUDIO_TYPE:
            return 'music'
        elif extension in TEXT_TYPE or extension in LANGUAGE_TYPE:
            return 'file-text-o'
        elif extension in IMAGE_TYPE:
            return 'file-image-o'
        elif extension in VIDEO_TYPE:
            return 'film'
        elif extension in ARCHIVE_TYPE:
            return 'file-archive-o'
        elif extension == 'pdf':
            return 'file-pdf-o'
        return 'file-o'


def date_file(path):
    """Get date with proper format."""
    mtime = time.gmtime(os.path.getmtime(path))
    return time.strftime("%d/%m/%Y %H:%M", mtime)


def get_file_size(path):
    """Get file size, human readable."""
    bytes = float(os.path.getsize(path))
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2f TB' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2f GB' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2f MB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2f KB' % kilobytes
    else:
        size = '%.2f bytes' % bytes
    return size
