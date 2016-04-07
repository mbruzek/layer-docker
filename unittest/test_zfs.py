import os
import shutil
import sys
import tempfile
import unittest

from shlex import split
from subprocess import check_call
from subprocess import check_output

from zfs import ZfsPool


class TestZfs(unittest.TestCase):

    def setUp(self):
        '''Run operations once before this class.'''
        self.directory = tempfile.mkdtemp()
        self.mount_point = tempfile.mkdtemp()
        self.devices = []
        print('Creating files in {0}'.format(self.directory))
        # The command to create multiple images to mount zfs.
        image = 'dd if=/dev/zero of={0} bs=1M count=150'
        for a in range(6):
            output_file = '{0}/zfs{1}.img'.format(self.directory, str(a))
            print(image.format(output_file))
            # Create the files
            check_call(split(image.format(output_file)))
            self.devices.append(output_file)
        print('File creation complete.')

    def test_adding(self):
        '''Test the init method of the ZfsPool.'''
        pool_name = 'test-zfs-pool-1'
        # Create zfs pool by name.
        pool = ZfsPool(pool_name)
        print('Adding the first 3 devices.')
        pool.add(self.devices[0:3])
        print('Adding the last 3 devices.')
        pool.add(self.devices[3:6])
        # Run a command that lists the zfs pool pool.
        cmd = 'sudo zpool list -H {0}'.format(pool_name)
        output = check_output(split(cmd))
        print(output)
        destroy = 'sudo zpool destroy -f {0}'.format(pool_name)
        check_call(split(destroy))
        print('Pool {0} destroyed.'.format(pool_name))
        assert(pool_name in output[0], 'Pool name not in zfs pool listing.')

    def test_create(self):
        '''Test the create model of the ZfsPool.'''
        print('Creating a pool with the first 3 devices.')
        pool = ZfsPool.create(self.mount_point, self.devices[0:3])
        pool_name = pool.pool_name
        print('Adding 3 more devices')
        pool.add(self.devices[3:6])
        cmd = 'sudo zpool list -H {0}'.format(pool_name)
        output = check_output(split(cmd))
        print(output)
        destroy = 'sudo zpool destroy -f {0}'.format(pool_name)
        check_call(split(destroy))
        print('Pool {0} destroyed.'.format(pool_name))
        assert(pool_name in output[0], 'Pool name not in zfs pool listing.')

    def tearDown(self):
        '''Operations run once at the end of the tests.'''
        # Delete the directory of temporary files.
        shutil.rmtree(self.directory)
        # Delete the mount point directory.
        shutil.rmtree(self.mount_point)
