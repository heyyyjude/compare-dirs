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
        self._prefix_path = pre_fix_path
        self._relative_path_of_files_list = None
        self._symlink_dict = OrderedDict()
        self.get_path_of_files()

    @property
    def prefix_path(self):
        return self._prefix_path

    @property
    def symlink_dict(self):
        return self._symlink_dict

    @property
    def relative_path_of_files_list(self):
        return self._relative_path_of_files_list

    def get_path_of_files(self):
        """
        get the absolute path of files from the previous directory or the source directory
        :set: set symlink_dict, relative_path_of_files_list
        """
        logging.info(self.prefix_path)
        relative_path_of_files_list = list()
        for parent_dir, sub_dirs, files in os.walk("./"):

            if (
                ".git" in parent_dir
                or ".snakemake" in parent_dir
                or "snakemake_job_logs" in parent_dir
                or "Thumbnail_Images" in parent_dir
            ):
                pass
            else:
                for f in files:
                    relative_path = ""
                    if parent_dir == self.prefix_path:
                        relative_path = os.path.join(parent_dir, f)
                    else:

                        relative_sub_dir = parent_dir.replace(self.prefix_path, "")
                        relative_path = os.path.join(relative_sub_dir, f)
                        # logging.info(parent_dir)
                        # logging.info(relative_sub_dir)
                        # logging.info(relative_path)

                        if os.path.islink(relative_path):
                            symlink_origin_path_of_file = os.readlink(relative_path)
                            self._symlink_dict[
                                relative_path
                            ] = symlink_origin_path_of_file

                        elif os.path.isfile(relative_path):
                            relative_path_of_files_list.append(relative_path)

                        else:
                            print("---error---")
                            print(self.prefix_path, relative_path)
                            print(relative_path)
                            raise ValueError("This is not a file nor a link")
        self._relative_path_of_files_list = relative_path_of_files_list

    def validate_files_path(self):
        """
        validate files in lists
        :return: None or Error raised.
        """

        if not os.path.isdir(self.prefix_path):
            print("This is a directory!")
            print(self.prefix_path)
            raise ValueError()
