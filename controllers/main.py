from bottle import route, view, request
from config import config
from security import security
from utils import utils, chmod
import os

@route('/')
def redirect_home():
    """Main route : redirect to app home."""
    return redirect(config.app_dir+'/')

@route(config.app_dir+'/')
@view('main.stpl')
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
    current_dir = config.full_path + path
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
        if item in config.exclude:
            pass
        else:
            if not toplevel:
                filepath = path + item
            else:
                filepath = path + "/" + item
            file = config.full_path + path + '/' + item
            fileList.append({"name": item, "path": filepath, "filetype": utils.get_icon(config.full_path, request.GET.get('path'), item),
                "date": utils.date_file(config.full_path +filepath), "size": utils.get_file_size(config.full_path + filepath),
                "id": id, "chmod":chmod.get_pretty_chmod(file)})
            id = id + 1

    data = {"title": path, "full_path": config.full_path, "path": path, "list": all_files,
        "toplevel": toplevel, "fileList": fileList, "is_auth": is_auth,
        "is_admin": is_admin, "error": request.GET.get('error'), "app_dir": config.app_dir}
    return dict(data=data)
