#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from bottle import *
import libs.chmod as chmod
import sys, os, time, md5, urllib2, json

app = Bottle()
full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
app_dir = '/filemanager'
accounts = {"test": "test", "test2": "test2"} 
admins = ["test2"]
exclude = []

# get file type based on filename
def get_file_type(filename):
    path = request.GET.get('path')
    if not path:
        path = '/'
    TEXT_TYPE = ['doc', 'docx', 'txt', 'rtf', 'odf', 'text', 'nfo']
    AUDIO_TYPE = ['aac', 'mp3', 'wav', 'wma', 'm4p', 'flac']
    IMAGE_TYPE = ['bmp', 'gif', 'jpg', 'jpeg', 'png','svg']
    IMAGESOURCE_TYPE = ['eps', 'ico', 'psd', 'psp', 'raw', 'tga', 'tif', 'tiff', 'svg']
    VIDEO_TYPE = ['mv4', 'bup', 'mkv', 'ifo', 'flv', 'vob', '3g2', 'bik', 'xvid', 'divx', 'wmv', 'avi', '3gp', 'mp4', 'mov', '3gpp', '3gp2', 'swf', 'mpg', 'mpeg']
    ARCHIVE_TYPE = ['7z', 'dmg', 'rar', 'sit', 'zip', 'bzip', 'gz', 'tar', 'ace']
    EXEC_TYPE = ['exe', 'msi', 'mse']
    SCRIPT_TYPE = ['js', 'html', 'htm', 'xhtml', 'jsp', 'asp', 'aspx', 'php', 'xml', 'css', 'py', 'bat', 'sh', 'rb', 'java']

    if os.path.isdir(full_path + path + "/" + filename):
        return "folder"
    else:
        extension = os.path.splitext(filename)[1].replace('.','')
        if extension in TEXT_TYPE:
            type_file = 'text'
        elif extension in AUDIO_TYPE:
            type_file = 'audio'
        elif extension in IMAGE_TYPE:
            type_file = 'image'
        elif extension in IMAGESOURCE_TYPE:
            type_file = 'imagesource'
        elif extension in VIDEO_TYPE:
            type_file = 'video'
        elif extension in ARCHIVE_TYPE:
            type_file = 'archive'
        elif extension in EXEC_TYPE:
            type_file = 'exec'
        elif extension in SCRIPT_TYPE:
            type_file = 'script'
        elif extension == 'pdf':
            type_file = 'pdf'
        else:
            type_file = 'unknow'
        return type_file

# get date with proper format
def date_file(path):
    mtime = time.gmtime(os.path.getmtime(path))
    return time.strftime("%d/%m/%Y %H:%M:%S", mtime)

# get file size - human readable
def get_file_size(path):
    bytes = float(os.path.getsize(path))
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2f Tb' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2f Gb' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2f Mb' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2f Kb' % kilobytes
    else:
        size = '%.2f Bytes' % bytes
    return size

# process login
@app.post(app_dir+'/login')
def login():
    login = request.forms.get('login')
    password = request.forms.get('password')
    if not login or not password:
        redirect(app_dir+"/?error=empty")
    if login in accounts:
        if accounts[login] == password:
            hash = md5.new()
            hash.update(password)
            response.set_cookie("login", login)
            response.set_cookie("password", hash.hexdigest())
            redirect(app_dir+"/")
        else:
            redirect(app_dir+"/?error=badpass")
    else:
	# don't indicate if that's a valid user
        redirect(app_dir+"/?error=badpass")
    return ""

# process logout
@app.route(app_dir+'/logout')
def logout():
    response.set_cookie("login", "")
    response.set_cookie("password", "")
    redirect(app_dir+"/")

# handle static files
@app.route(app_dir+'/img/:filename')
def img_static(filename):
    return static_file(filename, root=full_path+'/views/static/img/')

@app.route(app_dir+'/img/view')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=full_path)

@app.route(app_dir+'/thumb')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=full_path)

@app.route(app_dir+'/img/icons/:filename')
def icons_static(filename):
    return static_file(filename, root=full_path+'/views/static/img/icons/')

@app.route(app_dir+'/img/fancybox/:filename')
def fancybox_static(filename):
    return static_file(filename, root=full_path+'/views/static/img/fancybox/')

@app.route(app_dir+'/js/:filename')
def js_static(filename):
    return static_file(filename, root=full_path+'/views/static/js/')

@app.route(app_dir+'/css/:filename')
def css_static(filename):
    return static_file(filename, root=full_path+'/views/static/css/')

@app.route(app_dir+'/fonts/:filename')
def css_static(filename):
    return static_file(filename, root=full_path+'/views/static/fonts/')

# upload files
@app.route(app_dir+'/upload', method='POST')
def do_upload():
    name = request.forms.get('name')
    print name
    path = request.forms.get('path').replace("/" + name, "")
    data = request.files.get('file')
    if not os.path.isdir(full_path + path + "/.thumbs"):
        os.mkdir(full_path + path + "/.thumbs")
    try:
        os.remove(full_path + path + "/.thumbs/" + name + ".jpg")
    except:
        print "File doesn't exists"
    thumb = open(full_path + path + "/.thumbs/" + name + ".jpg", "w+")
    thumb.write(data.file.read())
    return redirect(app_dir+"/?path=" + path)

# delete files
@app.route(app_dir+'/delete')
def delete():
    try:
        os.remove(full_path + request.GET.get('path'))
        print full_path + request.GET.get('path')
    except:
        print "File doesn't exists"
    return redirect(app_dir+"/?path=" + str(request.GET.get('return')))

# download file
@app.route(app_dir+'/download')
def download():
    filename = request.GET.get('path')
    return static_file(filename, root=full_path, download=filename)

# redirect to app_dir
@app.route('/')
def redirect_home():
    return redirect(app_dir+'/')

# handle main page
@app.route(app_dir+'/')
@view('main')
def list():
    if request.get_cookie("login") in admins:
        is_admin = True
    else:
        is_admin = False
    for header in response.headers:
        print header
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
    dir_list.sort()
    file_list = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    file_list.sort()
    all_files = dir_list + file_list
    output = []
    i = 1
    for item in all_files:
        if item in exclude:
            pass
        else:
            if not toplevel:
                filepath = path + item
            else:
                filepath = path + "/" + item
            if os.path.exists(full_path + path + "/.thumbs/" + item + ".jpg"):
                preview = path + "/.thumbs/" + item + ".jpg"
            else:
                preview = False
            file = full_path + path + '/' + item
            output.append({"name": item, "path": filepath, "type": get_file_type(item),
                "date": date_file(full_path +filepath), "size": get_file_size(full_path + filepath),
                "preview": preview, "counter": i, "chmod":chmod.get_pretty_chmod(file)})
            i = i + 1
    data = {"title": path, "full_path": full_path, "path": path, "list": all_files,
        "toplevel": toplevel, "output": output, "login": request.get_cookie("login"),
        "password": request.get_cookie("password"), "error": request.GET.get('error'),
        "is_admin": is_admin, "app_dir": app_dir}
    return dict(data=data)

run(app, host='127.0.0.1', port=8082, reloader=True, debug=False)
