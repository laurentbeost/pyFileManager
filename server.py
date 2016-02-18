#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from bottle import(
    route, post, mako_view as view, request,
    static_file, response, redirect, run)
from bottle import mako_template as template
import libs.chmod as chmod
import libs.security as security
import sys, os, time, urllib2, json


full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
app_dir = '/filemanager'
security.accounts = {"test": "test", "test2": "test2"}
security.admins = ["test2"]
exclude = []
log_debug = True


def get_icon(filename):
    """Get icon, based on file name."""
    path = request.GET.get('path')
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


@post(app_dir+'/login')
def login():
    """Process login : set cookie when credentials are valid."""
    login = request.forms.get('login')
    password = request.forms.get('password')
    if not login or not password:
        redirect(app_dir+"/?error=empty")
    if security.can_login(login, password):
        response.set_cookie("login", login)
        response.set_cookie("password", security.encrypt_password(password))
        redirect(app_dir+"/")
    else:
        # don't indicate if that's a valid user or anything
        redirect(app_dir+"/?error=badpass")
    return ""


@route(app_dir+'/logout')
def logout():
    """Process logout : remove cookies."""
    response.set_cookie('login', '', expires=0)
    response.set_cookie('password', '', expires=0)
    redirect(app_dir+"/")


"""Handle static ressources."""
@route(app_dir+'/img/:filename')
def img_static(filename):
    return static_file(filename, root=full_path+'/views/static/img/')

@route(app_dir+'/img/view')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=full_path)

@route(app_dir+'/thumb')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=full_path)

@route(app_dir+'/img/icons/:filename')
def icons_static(filename):
    return static_file(filename, root=full_path+'/views/static/img/icons/')

@route(app_dir+'/img/fancybox/:filename')
def fancybox_static(filename):
    return static_file(filename, root=full_path+'/views/static/img/fancybox/')

@route(app_dir+'/js/:filename')
def js_static(filename):
    return static_file(filename, root=full_path+'/views/static/js/')

@route(app_dir+'/css/:filename')
def css_static(filename):
    return static_file(filename, root=full_path+'/views/static/css/')

@route(app_dir+'/fonts/:filename')
def css_static(filename):
    return static_file(filename, root=full_path+'/views/static/fonts/')


@route(app_dir+'/upload', method='POST')
def do_upload():
    """Upload files : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    name = request.forms.get('name')
    if log_debug:
        print("uploaded file : "+name)
    path = request.forms.get('path').replace("/" + name, "")
    data = request.files.get('file')
    new_file = open(full_path + path + name, "w+")
    if (os.path.exists(new_file)):
        if log_debug:
            print("user wants to move '"+repr(srcPath)+"' to '"+repr(dstPath))
        return None
    new_file.write(data.file.read())
    return redirect(app_dir+"/?path=" + path)


@route(app_dir+'/rename')
def rename():
    """Rename a file/directory : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    srcPath = full_path+'/'+request.GET.get('srcPath')
    dstPath = full_path+'/'+request.GET.get('dstPath')
    itemId = request.GET.get('itemId');
    if srcPath == dstPath:
        return None
    if log_debug:
        print("user wants to move '"+repr(srcPath)+"' to '"+repr(dstPath))
    try:
        os.rename(srcPath, dstPath)
    except:
        if log_debug:
            print("Can't rename file")
    return '{"itemId": "'+itemId+'", "filetype": "'+get_icon(dstPath)+'"}'


@route(app_dir+'/download')
def download():
    """Download a file : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    filename = request.GET.get('path')
    return static_file(filename, root=full_path, download=filename)


@route(app_dir+'/delete')
def delete():
    """Delete a file : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    filePath = full_path + request.GET.get('path')
    if log_debug:
        print("deleted file : "+filePath)
    try:
        os.unlink(filePath)
    except:
        if log_debug:
            print("File doesn't exists")
    return None


@route('/')
def redirect_home():
    """Main route : redirect to app home."""
    return redirect(app_dir+'/')


@route(app_dir+'/')
@view('main.mako')
def list():
    """App home : is building the file listing job."""
    is_auth = security.is_authenticated_user(request.get_cookie("login"), request.get_cookie("password"))
    is_admin = (is_auth and security.is_admin(request.get_cookie("login")))
    path = request.GET.get('path')
    if not path:
        path = '/'
    if path != '/':
        array = path.split("/")
        toplevel = path.replace("/" + array[path.count("/")], "")
        if not toplevel:
            toplevel  = '/'
    else:
        toplevel = False
    current_dir = full_path + path
    all_files = os.listdir(current_dir)
    dir_list = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    f = current_dir + "/.settings"
    if os.path.exists(f):
        settings_file = open(f, "r+")
        settings_json = json.load(settings_file)
        settings_file.close()
    dir_list.sort(key=lambda d: d.lower())
    file_list = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    file_list.sort(key=lambda d: d.lower())
    all_files = dir_list + file_list
    fileList = []
    id = 1
    for item in all_files:
        if item in exclude:
            pass
        else:
            if not toplevel:
                filepath = path + item
            else:
                filepath = path + "/" + item
            file = full_path + path + '/' + item
            fileList.append({"name": item, "path": filepath, "filetype": get_icon(item),
                "date": date_file(full_path +filepath), "size": get_file_size(full_path + filepath),
                "id": id, "chmod":chmod.get_pretty_chmod(file)})
            id = id + 1
    
    data = {"title": path, "full_path": full_path, "path": path, "list": all_files,
        "toplevel": toplevel, "fileList": fileList, "is_auth": is_auth,
        "is_admin": is_admin, "error": request.GET.get('error'), "app_dir": app_dir}
    return dict(data=data)


run(host='127.0.0.1', port=8082, reloader=True, debug=False)
