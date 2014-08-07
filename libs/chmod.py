import os, stat

def get_st_mode(file):
    return os.stat(file)[stat.ST_MODE]

def pretty_chmod(st_mode):
    prefix = get_prefix(st_mode)
    chmod = oct(st_mode)[-3:]
    user, group, other = chmod
    return prefix + ''.join(get_mode(mode) for mode in (user, group, other))

def get_mode(permission):
    list = {'0':'---', '1':'--x', '2':'-w-', '3':'-wx', '4':'r--',
            '5':'r-x', '6':'rw-', '7':'rwx'}
    return list[permission]

def get_prefix(st_mode):
    if stat.S_ISDIR(st_mode):
        return 'd'
    else:
        return '-'

def get_pretty_chmod(file):
    return pretty_chmod(get_st_mode(file))
