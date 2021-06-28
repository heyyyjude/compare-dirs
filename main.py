import argparse
import logging
import os

from compare_files import ComparisonPathOfFiles
from path_of_files import PathOfFiles

logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.DEBUG,
)

# this is for turning off the logging
logging.getLogger().disabled = False


def run(comparison, backup_dir, source_dir):
    print(
        "Files from the {} are not found in the {}.".format(backup_dir, source_dir)
    )
    print("------start--------")
    for i in comparison.backup_only_files_list:
        print(i)
    print("-------end---------")

    print("Files from the {} are not found in the {}.".format(source_dir, backup_dir))
    print("------start--------")
    for i in comparison.source_only_files_list:
        print(i)
    print("-------end---------")

    print("symlinks from {} are not found in the {}.".format(backup_dir, source_dir))
    print("------start--------")
    for i in comparison.backup_only_symlinks_list:
        print(i)
    print("-------end---------")

    print("symlinks from the {} are not found in the {}.".format(source_dir, backup_dir))
    print("------start--------")
    for i in comparison.source_only_symlinks_list:
        print(i)
    print("-------end---------")


def main(backup_dir, source_dir):
    os.chdir(backup_dir)
    backup_dir_files_path = PathOfFiles(backup_dir)
    os.chdir("../")
    os.chdir(source_dir)
    source_dir_files_path = PathOfFiles(source_dir)
    comparison = ComparisonPathOfFiles(backup_dir_files_path, source_dir_files_path)
    run(comparison, backup_dir, source_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Python scripts for comparing the location of files from two different directory"
    )

    parser.add_argument(
        "-b",
        "--backup_dir",
        action="store",
        type=str,
        required=True,
        help="backup-dir",
    )

    parser.add_argument(
        "-s",
        "--source_dir",
        action="store",
        type=str,
        required=True,
        help="source-dir",
    )
    args = parser.parse_args()

    main(args.backup_dir, args.source_dir)
