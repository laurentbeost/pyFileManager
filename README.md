pyFileManager
=============

Python web file manager

--
FEATURES :
- english translation
- reverse-proxy support
- display chmod
- download, rename and delete files



TODO :
- upload files
- change chmod
- change current directory with header links
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
