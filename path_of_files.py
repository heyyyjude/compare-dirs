import logging
import os
from collections import OrderedDict

logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)

logging.getLogger().disabled = True


class PathOfFiles(object):
    def __init__(self, pre_fix_path):
        self._prefix = pre_fix_path + "/"
        self._relative_path_of_files_list = list()
        self._abs_path_of_files_list = list()
        self._symlink_dict = OrderedDict()
        self.get_path_of_files()
        self._abs_prefix_path = os.path.abspath(pre_fix_path)

    @property
    def abs_prefix_path(self):
        return self._abs_prefix_path

    @property
    def prefix(self):
        return self._prefix

    @property
    def symlink_dict(self):
        return self._symlink_dict

    @property
    def relative_path_of_files_list(self):
        return self._relative_path_of_files_list

    @property
    def abs_path_of_files_list(self):
        return self._abs_path_of_files_list

    def get_path_of_files(self):
        """
        get the absolute path of files from the previous directory or the source directory
        :set: set symlink_dict, relative_path_of_files_list
        """
        # logging.info(self.prefix_path)
        relative_path_of_files_list = list()
        for parent_dir, sub_dirs, files in os.walk(self.prefix):

            if (
                    ".git" in parent_dir
                    or ".snakemake" in parent_dir
                    or "snakemake_job_logs" in parent_dir
                    or "Thumbnail_Images" in parent_dir
            ):
                pass
            else:
                for f in files:
                    relative_path = os.path.join(parent_dir, f)
                    abs_file_path = os.path.abspath(relative_path)
                    self._abs_path_of_files_list.append(abs_file_path)
                    # logging.info(self._abs_path_of_files_list)

                    if os.path.islink(relative_path):
                        symlink_origin_path_of_file = os.readlink(
                            relative_path)
                        self._symlink_dict[
                            relative_path
                        ] = symlink_origin_path_of_file

                    elif os.path.isfile(relative_path):
                        relative_path_of_files_list.append(relative_path)

                    else:
                        print("---error---")
                        print(self.prefix, relative_path)
                        raise ValueError("This is not a file nor a link")
        self._relative_path_of_files_list = relative_path_of_files_list

    def validate_files_path(self):
        """
        validate files in lists
        :return: None or Error raised.
        """

        if not os.path.isdir(self.prefix):
            print("This is a directory!")
            print(self.prefix)
            raise ValueError()
