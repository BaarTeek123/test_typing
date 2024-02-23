import threading
from os.path import isfile, join
from time import sleep

from requests import post
from os import listdir, remove
from json import load

from Config import config


class FileWatcher:
    def __init__(self, api_url, directory_path, headers=None):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        self.api_url = api_url
        self.headers = headers
        self.directory_path = directory_path
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        self.thread.start()

    def run(self):
        while True:
            try:
                # Get all file names in the directory
                filenames = [filename for filename in listdir(self.directory_path) if
                             isfile(join(self.directory_path, filename))]
                # Sort filenames as strings, which works because of the timestamp format
                filenames.sort()

                for filename in filenames:
                    config.LOGGER.debug(f"Processing {join(self.directory_path, filename)}")

                    file_path = join(self.directory_path, filename)
                    if isfile(file_path):
                        with open(file_path, 'r') as file:
                            payload = load(file)

                        response = post(self.api_url, headers=self.headers, json=payload)

                        if response.status_code == 200:  # Assuming 200 means success and file can be deleted
                            remove(file_path)
                            config.LOGGER.debug(f"File {filename} processed and removed.")
            except Exception as e:
                config.LOGGER.error(f"Error in FileWatcher: {e}")
            sleep(5)
