#!/usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
import re
import os
import threading
import urllib.request
import signal
import argparse
import json
import sys
from colorama import Fore, Style, init
import ipdb
from queue import Queue

init()

# this ANSI code lets us erase the current line
ERASE_LINE = "\x1b[2K"

COLOR_NAME_TO_CODE = {
    "default": "",
    "red": Fore.RED,
    "green": Style.BRIGHT + Fore.GREEN,
}


def print_text(
    text, color="default", in_place=False, **kwargs
):  # type: (str, str, bool, any) -> None
    """
    print text to console, a wrapper to built-in print

    :param text: text to print
    :param color: can be one of "red" or "green", or "default"
    :param in_place: whether to erase previous line and print in place
    :param kwargs: other keywords passed to built-in print
    """
    if in_place:
        print("\r" + ERASE_LINE, end="")
    print(COLOR_NAME_TO_CODE[color] + text + Style.RESET_ALL, **kwargs)


def create_url(url):
    """
    From the given url, produce a URL that is compatible with Github's REST API. Can handle blob or tree paths.
    """
    repo_only_url = re.compile(
        r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$"
    )
    re_branch = re.compile("/(tree|blob)/(.+?)/")

    # Check if the given url is a url to a GitHub repo. If it is, tell the
    # user to use 'git clone' to download it
    if re.match(repo_only_url, url):
        print_text(
            "✘ The given url is a complete repository. Use 'git clone' to download the repository",
            "red",
            in_place=True,
        )
        sys.exit()

    # extract the branch name from the given url (e.g master)
    branch = re_branch.search(url)
    download_dirs = url[branch.end() :]
    api_url = (
        url[: branch.start()].replace("github.com", "api.github.com/repos", 1)
        + "/contents/"
        + download_dirs
        + "?ref="
        + branch.group(2)
    )
    return api_url, download_dirs


def __download_file(url, output_dir):
    """
    Download a file from the given url to the given output directory.
    """
    # get the file name from the url
    file_name = url.split("/")[-1]

    # create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # download the file to the output directory
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        response = urllib.request.urlretrieve(url)
    except KeyboardInterrupt:
        # when CTRL+C is pressed during the execution of this script,
        # bring the cursor to the beginning, erase the current line, and dont make a new line
        print_text("✘ Got interrupted", "red", in_place=True)
        sys.exit()

    # print a message to the console
    print_text("✔ Downloaded " + file_name, "green", in_place=True)


def download(repo_url, output_dir="./"):
    """Downloads the files and directories in repo_url. If flatten is specified, the contents of any and all
    sub-directories will be pulled upwards into the root folder."""

    # generate the url which returns the JSON data
    api_url, download_dirs = create_url(repo_url)

    # ipdb.set_trace()

    # print("Output directory: " + output_dir)
    # print("Downloading from: " + api_url)
    # print("Download dirs: " + download_dirs)

    # ipdb.set_trace()

    dir_out = [d for d in download_dirs.split("/") if d != ""]
    dir_out = os.path.join(output_dir, *dir_out)
    # if len(download_dirs.split(".")) == 0:
    #     dir_out = os.path.join(output_dir, download_dirs)
    # else:
    #     dir_out = os.path.join(output_dir, *download_dirs.split("/")[:-1])

    # print(f"Downloading {repo_url} to: " + dir_out)

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        response = urllib.request.urlretrieve(api_url)
    except KeyboardInterrupt:
        # when CTRL+C is pressed during the execution of this script,
        # bring the cursor to the beginning, erase the current line, and dont make a new line
        print_text("✘ Got interrupted", "red", in_place=True)
        sys.exit()

    os.makedirs(dir_out, exist_ok=True)

    # total files count
    total_files = 0

    max_concurrent_downloads = 10

    with open(response[0], "r") as f:
        data = json.load(f)
        # getting the total number of files so that we
        # can use it for the output information later
        total_files += len(data)

        # If the data is a file, download it as one.
        if isinstance(data, dict) and data["type"] == "file":

            # download the file
            dest = os.path.join(dir_out, data["name"])
            __download_file(data["download_url"], dest)

        for file in data:
            file_url = file["download_url"]
            file_name = file["name"]
            file_path = file["path"]

            path = file_path

            if file_url is not None:
                dest = os.path.join(dir_out, file_name)
                __download_file(file_url, dest)
            else:
                download(file["html_url"], output_dir)

    return total_files


class GitDownloader:
    def __init__(self, url: str, output_dir: str, max_concurrent_downloads: int = 2):
        self.url = url
        self.output_dir = output_dir
        self.max_concurrent_downloads = max_concurrent_downloads
        self.queue = Queue()
        self.thread_pool = Queue()
        self.add_download(url, output_dir)

    def __download_file(self, url: str, out: str):
        """
        Download a file from the given url to the given output directory.
        """
        # get the file name from the url
        file_name = url.split("/")[-1]

        # create the output directory if it doesn't exist
        if not os.path.exists(out):
            os.makedirs(out)

        # download the file to the output directory
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-agent", "Mozilla/5.0")]
            urllib.request.install_opener(opener)
            response = urllib.request.urlretrieve(url)
        except KeyboardInterrupt:
            # when CTRL+C is pressed during the execution of this script,
            # bring the cursor to the beginning, erase the current line, and dont make a new line
            print_text("✘ Got interrupted", "red", in_place=True)
            sys.exit()

        # print a message to the console
        print_text("✔ Downloaded " + file_name, "green", in_place=True)

    def start_download(self):

        # check from queue
        while not self.queue.empty():

            # check max concurrent downloads
            if threading.active_count() < self.max_concurrent_downloads // 2:
                # get item from queue
                item = self.queue.get()
                # api_url, download_dirs = create_url(item)
                # create thread
                t = threading.Thread(
                    target=self.__download_file, args=(item["url"], item["out"])
                )
                # start thread
                self.thread_pool.put(t)
                t.start()

                # self.thread_pool.submit(self.add_download, item["url"], item["out"])
                # join thread
                # t.join()
                # task done
                # self.queue.task_done()

        # check if all threads are done
        
        while not self.thread_pool.empty():
            t = self.thread_pool.get()
            t.join()
        

    def add_download(self, url, output_dir):

        api_url, download_dirs = create_url(self.url)

        dir_out = [d for d in download_dirs.split("/") if d != ""]
        dir_out = os.path.join(self.output_dir, *dir_out)

        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-agent", "Mozilla/5.0")]
            urllib.request.install_opener(opener)
            response = urllib.request.urlretrieve(api_url)
        except KeyboardInterrupt:
            # when CTRL+C is pressed during the execution of this script,
            # bring the cursor to the beginning, erase the current line, and dont make a new line
            print_text("✘ Got interrupted", "red", in_place=True)
            sys.exit()

        os.makedirs(dir_out, exist_ok=True)

        # total files count
        total_files = 0

        with open(response[0], "r") as f:
            data = json.load(f)
            # getting the total number of files so that we
            # can use it for the output information later
            total_files += len(data)

            # If the data is a file, download it as one.
            if isinstance(data, dict) and data["type"] == "file":

                # download the file
                dest = os.path.join(dir_out, data["name"])
                self.queue.put({"url": data["download_url"], "out": dest})
                # self.__download_file(data["download_url"], dest)

            for file in data:
                file_url = file["download_url"]
                file_name = file["name"]
                file_path = file["path"]
                # path = file_path
                if file_url is not None:
                    dest = os.path.join(dir_out, file_name)
                    self.queue.put({"url": file_url, "out": dest})
                    # self.__download_file(file_url, dest)
                else:
                    self.add_download(file["html_url"], self.output_dir)


def main():
    if sys.platform != "win32":
        # disbale CTRL+Z
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)

    parser = argparse.ArgumentParser(
        description="Download directories/folders from GitHub"
    )
    parser.add_argument(
        "urls", nargs="+", help="List of Github directories to download."
    )
    parser.add_argument(
        "--output_dir",
        "-d",
        dest="output_dir",
        default="./",
        help="All directories will be downloaded to the specified directory.",
    )

    parser.add_argument(
        "--flatten",
        "-f",
        action="store_true",
        help="Flatten directory structures. Do not create extra directory and download found files to"
        " output directory. (default to current directory if not specified)",
    )

    args = parser.parse_args()

    flatten = args.flatten
    for url in args.urls:
        total_files = download(url, flatten, args.output_dir)

    print_text("✔ Download complete", "green", in_place=True)


if __name__ == "__main__":
    main()
