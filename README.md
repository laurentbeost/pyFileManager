pyFileManager
=============

Python web file manager

--
Forked from https://github.com/inlanger/SimplePythonFileManager, and add these features

FEATURES :
- english translation
- reverse-proxy support


TODO :
- upload and remove files
- change chmod
- ini configuration support (or SQLite)
- view files (images, text, etc)
- multilang support
- code cleanup


HOW TO USE WITH NGINX :
- change "app_dir" to desired directory
- use this location configuration with NGiNX :
```
location /directory {
    proxy_pass http://127.0.0.1:8082;
}
```
