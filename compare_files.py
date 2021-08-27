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
logging.getLogger().disabled = False


class ComparisonPathOfFiles(object):
    def __init__(self, BackupPathOfFiles, sourcePathOfFiles):
        # path of files in the previous directory
        self._backup_path_of_files = BackupPathOfFiles
        # path of files in the source directory
        self._source_path_of_files = sourcePathOfFiles
        # abs path used
        self._same_file_same_md5_list = None
        # abs path used
        self._src_only_file_list = None

        self._backup_only_file_list = None

        # symlinks dict from backup_dir
        self._symlinks_dict_from_backup_dir = BackupPathOfFiles.symlink_dict
        # symlinks dict from source_dir
        self._symlinks_dict_from_source_dir = sourcePathOfFiles.symlink_dict

        self._symlinks_verified_from_source_dir = OrderedDict()
        self.compare_files_md5()

    @property
    def symlinks_dict_from_backup_dir(self):
        return self._symlinks_dict_from_backup_dir

    @property
    def symlinks_dict_from_source_dir(self):
        return self._symlinks_dict_from_source_dir

    @property
    def backup_dir_prefix_path(self):
        return self._backup_path_of_files.prefix

    @property
    def source_dir_prefix_path(self):
        return self._source_path_of_files.prefix

    @property
    def backup_path_of_files(self):
        return self._backup_path_of_files

    @property
    def source_path_of_files(self):
        return self._source_path_of_files

    @property
    def hardlinks_path_from_previous_dir_list(self):
        return self._same_file_same_md5_list

    @property
    def copy_files_path_from_source_dir_list(self):
        return self._src_only_file_list

    def __str__(self):
        return "hard-links for dest dir : {}\n copy files for dest dir {}".format(
            self.hardlinks_path_from_previous_dir_list,
            self.copy_files_path_from_source_dir_list,
        )

    def compare_files_md5(self):

        """
        This function is for only files to compare. Not symlinks.
        :return:
        """
        same_file_same_md5_list = list()
        same_file_different_md5_list = list()
        src_only_file_list = list()
        backup_only_file_list = list()

        backup_rel_path_of_files_list = [
            i.replace(self.backup_dir_prefix_path, "") for i in
            self.backup_path_of_files.relative_path_of_files_list
        ]

        for prefix_rel_path_src_file in self.source_path_of_files.relative_path_of_files_list:
            rel_path_src_file = prefix_rel_path_src_file.replace(
                self.source_dir_prefix_path, "")

            if rel_path_src_file in backup_rel_path_of_files_list:
                # logging.info(rel_path_src_file)
                assert os.path.isfile(prefix_rel_path_src_file)

                rel_path_backup_file_inx = (
                    backup_rel_path_of_files_list.index(rel_path_src_file)
                )

                rel_path_backup_file = (
                    backup_rel_path_of_files_list[rel_path_backup_file_inx]
                )

                abs_path_backup_file = os.path.join(
                    self.backup_path_of_files.abs_prefix_path,
                    rel_path_backup_file)

                # logging.info(self.backup_path_of_files.abs_prefix_path)
                # logging.info(self.backup_path_of_files.prefix)

                logging.info("---begin to calculate md5 hash value---")
                logging.info(
                    "This is a path of a file in the backup directory and its md5 hash value."
                )
                logging.debug(abs_path_backup_file)
                # logging.debug(rel_path_backup_file)

                rel_backup_file_md5 = self.calculate_md5(
                    os.path.abspath(abs_path_backup_file))
                logging.debug(rel_backup_file_md5)

                logging.info(
                    "This is a path of a file in the source directory and its md5 hash value."
                )
                logging.debug(os.path.abspath(prefix_rel_path_src_file))

                rel_path_src_file_md5 = self.calculate_md5(
                    os.path.abspath(prefix_rel_path_src_file)
                )

                logging.debug(rel_path_src_file_md5)
                logging.info("---End calculating md5 hash value---")
                logging.info("\n")

                if rel_path_src_file_md5 == rel_backup_file_md5:
                    same_file_same_md5_list.append(rel_path_src_file)
                ## if files are not identical
                else:
                    same_file_different_md5_list.append(rel_path_src_file)
            ## if a file in source directory is not found in the previous directory
            else:
                ## abs_src_file = os.path.join(source_dir, src_file)
                src_only_file_list.append(rel_path_src_file)

        backup_only_file_list = list()

        source_rel_path_of_files_list = [
            i.replace(self.source_dir_prefix_path, "") for i in
            self.source_path_of_files.relative_path_of_files_list
        ]

        for prefix_rel_path_backup_file in self.backup_path_of_files.relative_path_of_files_list:
            rel_path_backup_file = prefix_rel_path_backup_file.replace(
                self.backup_dir_prefix_path, "")
            if rel_path_backup_file in source_rel_path_of_files_list:
                pass
            else:
                backup_only_file_list.append(rel_path_backup_file)

        self._same_file_same_md5_list = same_file_same_md5_list
        self._same_file_different_md5_list = same_file_different_md5_list
        self._src_only_file_list = src_only_file_list
        self._backup_only_file_list = backup_only_file_list
        return None

    def calculate_md5(self, a_file):
        with open(a_file, "rb") as fin:
            file_hash = hashlib.md5()
            chunk = fin.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = fin.read(8192)
        return file_hash.hexdigest()

    def compare_symlinks(self):

        ## calling for only a key which is abs_symlinks
        relative_path_backup_files = [
            i.replace(self.backup_dir_prefix_path)
            for i in self.symlinks_dict_from_backup_dir.keys()
        ]
        for abs_source_symlinks_file in self.symlinks_dict_from_source_dir:

            ## creating relative symlinks string
            src_symlinks_file = abs_source_symlinks_file.replace(
                self.source_dir_prefix_path + "/", ""
            )

            ## if relative src symlinks in symlinks in the backup directory
            ## Then, keep the symlinks in a dictionary
            if src_symlinks_file in relative_path_backup_files:
                self._symlinks_verified_from_source_dir[
                    abs_source_symlinks_file
                ] = self.symlinks_dict_from_source_dir[
                    abs_source_symlinks_file]

            else:
                logging.info(
                    "The below symlink file is not found in the backup dir.")
                logging.debug(abs_source_symlinks_file)
                self._symlinks_verified_from_source_dir[
                    abs_source_symlinks_file
                ] = self.symlinks_dict_from_source_dir[
                    abs_source_symlinks_file]
