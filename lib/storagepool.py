
class StoragePool(object):
    '''A generic class for a pool of storage devices.'''

    def __init__(self, reference):
        '''Return an existing StoragePool object by string reference name.'''
        self.reference = reference

    @property
    def size(self):
        '''Return a tuple used and total size.'''
        return self.used, self.total

    def add(self, device):
            '''Add a device to a storage pool.'''
            pass

    @classmethod
    def create(cls, mountPoint, devices=[], force=False):
        '''Return a new StoragePool object of devices at the mount point.'''
        pass

    def mount(self, device, mountPoint):
        '''Mount a filesystem.'''
        pass

    def umount(self, device='', mountPoint='', force=False):
        '''Detatch the file system from the file hierarchy.'''
        pass


class ToolsNotFound(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)
