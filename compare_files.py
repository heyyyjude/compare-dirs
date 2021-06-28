import os
import hashlib
import logging

from collections import OrderedDict

logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)

# this is for turning off the logging
logging.getLogger().disabled = True


class ComparisonPathOfFiles(object):
    def __init__(self, BackupPathOfFiles, sourcePathOfFiles):
        # path of files in the previous directory
        self._backup_path_of_files = BackupPathOfFiles
        # path of files in the source directory
        self._source_path_of_files = sourcePathOfFiles
        # abs path used
        self._hardlinks_path_from_previous_dir_list = None
        # abs path used
        self._copy_files_path_from_source_dir_list = None

        # symlinks dict from backup_dir
        self._symlinks_dict_from_backup_dir = BackupPathOfFiles.symlink_dict
        # symlinks dict from source_dir
        self._symlinks_dict_from_source_dir = sourcePathOfFiles.symlink_dict

        self._symlinks_verified_from_source_dir = OrderedDict()
        self.source_only_files_list = list()
        self.backup_only_files_list = list()
        self.source_only_symlinks_list = list()
        self.backup_only_symlinks_list = list()
        self.compare_files()

    @property
    def symlinks_dict_from_backup_dir(self):
        return self._symlinks_dict_from_backup_dir

    @property
    def symlinks_dict_from_source_dir(self):
        return self._symlinks_dict_from_source_dir

    @property
    def backup_dir_prefix_path(self):
        return self._backup_path_of_files.prefix_path

    @property
    def source_dir_prefix_path(self):
        return self._source_path_of_files.prefix_path

    @property
    def backup_path_of_files(self):
        return self._backup_path_of_files

    @property
    def source_path_of_files(self):
        return self._source_path_of_files

    @property
    def hardlinks_path_from_previous_dir_list(self):
        return self._hardlinks_path_from_previous_dir_list

    @property
    def copy_files_path_from_source_dir_list(self):
        return self._copy_files_path_from_source_dir_list

    def __str__(self):
        return "hard-links for dest dir : {}\n copy files for dest dir {}".format(
            self.hardlinks_path_from_previous_dir_list,
            self.copy_files_path_from_source_dir_list,
        )

    def compare_files(self):
        backup_relative_path_of_files_list = self.backup_path_of_files.relative_path_of_files_list


        source_relative_path_of_files_list = self.source_path_of_files.relative_path_of_files_list

        for source_relative_path_file in self.source_path_of_files.relative_path_of_files_list:
            # logging.info(source_relative_path_file)

            if not source_relative_path_file in backup_relative_path_of_files_list:
                self.source_only_files_list.append(source_relative_path_file)

        for backup_relative_path_of_file in self.backup_path_of_files.relative_path_of_files_list:
            # logging.info(backup_relative_path_of_files_list)

            if not backup_relative_path_of_file in source_relative_path_of_files_list:
                self.backup_only_files_list.append(backup_relative_path_of_file)

    def compare_symlinks(self):
        ## calling for only a key which is abs_symlinks
        relative_path_backup_files = self.symlinks_dict_from_backup_dir.keys()

        relative_path_source_files = self.symlinks_dict_from_source_dir.keys()

        for source_symlinks_file in self.symlinks_dict_from_source_dir:

            ## if relative src symlinks in symlinks in the backup directory
            ## Then, keep the symlinks in a dictionary
            if not source_symlinks_file in relative_path_backup_files:
                self.source_only_symlinks_list.append(source_symlinks_file)

        for backup_symlinks_file in self.symlinks_dict_from_backup_dir:
            if not backup_symlinks_file in relative_path_source_files:
                self.backup_only_symlinks_list.append(backup_symlinks_file)
