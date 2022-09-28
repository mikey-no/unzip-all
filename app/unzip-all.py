import argparse
import datetime
import logging
import pathlib
import sys
import zipfile


# time the programme started
programme_start = datetime.datetime.now()

# label for the directory where the archives are un-compressed
unzip_postfix: str = "__unzip-all__"

app_name = "unzip-all"
version = "1.0.0"
description = (
    rf"Unzip all zip files, in place in sub folder called {unzip_postfix} \ <name of the zip file> \ ..."
    " does not overwrite existing files."
)

log_format = "[%(asctime)s.%(msecs)03d] %(levelname)-8s %(name)-12s %(lineno)d %(funcName)s - %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

# show all messages below in order of seriousness
log_level = logging.DEBUG  # shows all
# log_level = logging.INFO  # shows info and below
# log_level = logging.WARNING
# log_level = logging.ERROR
# log_level = logging.CRITICAL

logging.basicConfig(
    # Define logging level
    level=log_level,
    # Define the date format
    datefmt=log_date_format,
    # Declare the object we created to format the log messages
    format=log_format,
    # Force this log handler to take over the others that may have been declared in other modules
    # see: https://github.com/python/cpython/blob/3.8/Lib/logging/__init__.py#L1912
    force=True,
    # Declare handlers
    handlers=[
        logging.FileHandler(f"{app_name}.log", encoding="UTF-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

log = logging.getLogger(__name__)


def get_all_zip_files(folder: pathlib.Path):
    zip_file_list = []

    def get_zip_file_recursive(
        folder: pathlib.Path = folder, zip_file_list=zip_file_list
    ):
        item = None
        try:
            for item in folder.iterdir():
                if item.is_dir():
                    get_zip_file_recursive(item, zip_file_list)
                if item.is_file():
                    if item.suffix.lower() == ".zip":
                        if zipfile.is_zipfile(item):
                            # log.debug(item)
                            zip_file_list.append(item)

        except PermissionError as pe:
            log.error(f"permission denied: {item}, {pe}")
        except Exception as e:
            log.error(f"exception: : {item}, {e}")

    get_zip_file_recursive(folder)

    return zip_file_list


def extract_zip_files(
    input_folder, all_zip_files=None, unzip_postfix=unzip_postfix
) -> int:
    """
    Extract all zip files to the directory / folder where the zip file is found,
    the extract folder has a sub folder with the prefix and a further sub folder with the name of the zip archive
    :param all_zip_files: generator for all in scope zip files
    :param unzip_postfix: extraction path postfix
    :return: the number of zip file found
    """
    if all_zip_files is None:
        all_zip_files = get_all_zip_files(input_folder)

    index = 0

    def unzip_archive(archive: pathlib.Path, unzip_path: pathlib.Path):
        with zipfile.ZipFile(archive, "r") as z:
            z.extractall(unzip_path)

    for index, zip_file in enumerate(all_zip_files):
        log.debug(f"a zip: {zip_file} - {zip_file.parent} - {len(zip_file.parents)}")
        archive = zipfile.ZipFile(zip_file, "r")
        files = archive.namelist()
        if len(files) > 0:
            unzip_path = zip_file.parent / unzip_postfix / str(zip_file.name)
            if unzip_path.exists():
                log.info(f"output folder: {unzip_path}")
            else:
                log.info(f"need to create output folder: {unzip_path}")
                unzip_path.parent.mkdir(parents=True, exist_ok=True)

            unzip_archive(zip_file, unzip_path)

    return index


def main():
    args_parser = argparse.ArgumentParser(description=description)
    args_parser.add_argument(
        "-i",
        "--input",
        "--input_folder",
        "--input-folder",
        "--input-dir",
        "--input-directory",
        dest="input_folder",
        type=pathlib.Path,
        help="input folder to search for zip files",
    )

    args_parser.add_argument(
        "-v",
        "--version",
        dest="version",
        help="get version information then exit",
        action="store_true",  # no extra value after the parameter
    )
    args = args_parser.parse_args()
    log.debug(args)

    if args.version:
        print(f"{app_name} - Version: {version}")
        sys.exit(0)

    if args.input_folder is None:
        log.critical(f"input folder / directory argument missing")
        sys.exit(1)

    if args.input_folder.is_dir() is False:
        log.critical(f"input folder / directory argument is not a directory")
        sys.exit(2)

    input_folder = args.input_folder

    last_zip_count = 0
    current_zip_count = 0
    while True:
        all_zip_files = get_all_zip_files(input_folder)
        current_zip_count = len(all_zip_files)
        log.info(f"{current_zip_count} zip files found")
        if current_zip_count == last_zip_count:
            log.info("no new zip files found to unzip... stopping")
            break
        # if in this loop the number of zip files has not increased then there are no new zip files to unzip
        extract_zip_files(input_folder=input_folder, all_zip_files=all_zip_files)
        last_zip_count = current_zip_count


if __name__ == "__main__":
    main()
    logging.info(
        f"programme stop: {datetime.datetime.now()}, running time: {datetime.datetime.now() - programme_start}"
    )
    sys.exit(0)
