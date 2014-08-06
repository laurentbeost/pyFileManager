import os, stat


class chmod():
    @staticmethod
    def get_chmod(file):
        return oct(os.stat(file)[stat.ST_MODE])[-3:]

    @staticmethod
    def pretty_chmod(this_chmod):
        user = this_chmod[0]
        group = this_chmod[1]
        other = this_chmod[2]
        user_pmode = chmod.get_mode(user)
        group_pmode = chmod.get_mode(group)
        other_pmode = chmod.get_mode(other)
        return user_pmode+group_pmode+other_pmode

    @staticmethod
    def get_mode(permission):
        list = {'0':'---', '1':'--x', '2':'-w-', '3':'-wx', '4':'r--',
                '5':'r-x', '6':'rw-', '7':'rwx'}
        return list[permission]

    @staticmethod
    def get_pretty_chmod(file):
        return chmod.pretty_chmod(chmod.get_chmod(file))

