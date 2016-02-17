pyFileManager
=============

A simple web file manager in Python.

--
#### FEATURES :
- english translation
- reverse-proxy support
- display chmod
- download, rename and delete files



#### TODO :
- upload files
- change chmod
- change current directory with header links
- ini configuration support (or SQLite)
- display non binary files
- multilang support
- code cleanup



#### HOW TO USE WITH NGINX :
- change "app_dir" to desired directory
- use this location configuration with NGiNX :
```
location /directory {
    proxy_pass http://127.0.0.1:8082;
}
```
