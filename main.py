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
        "{:<70s}{:70s}".format(backup_dir, source_dir)
    )

    print("-" * 70)

    for i in comparison._backup_only_file_list:
        print("{:<70s}{:70s}".format(i, "Not found"))


    for i in comparison._src_only_file_list:
        print("{:<70s}{:70s}".format("Not found", i))

    print("-" * 70)

    print("**Same file name but different md5 value**")
    for i in comparison._same_file_different_md5_list:
        print("{:<70s}".format(i))

    print("-" * 70)

    print("**Same file name and Same md5 value**")
    for i in comparison._same_file_same_md5_list:
        print("{:<70s}".format(i))


def main(backup_dir, source_dir):
    # os.chdir(backup_dir)
    backup_dir_files_path = PathOfFiles(backup_dir)
    # os.chdir("../")
    # os.chdir(source_dir)
    source_dir_files_path = PathOfFiles(source_dir)
    comparison = ComparisonPathOfFiles(backup_dir_files_path,
                                       source_dir_files_path)
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
