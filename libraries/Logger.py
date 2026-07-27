import logging
import os


class Logger:


    def __init__(self):

        log_directory = "logs"

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)


        logging.basicConfig(

            filename="logs/framework.log",

            level=logging.INFO,

            format=
            "%(asctime)s - %(levelname)s - %(message)s"

        )


        self.logger = logging.getLogger()



    def info(self, message):

        self.logger.info(message)



    def error(self, message):

        self.logger.error(message)



    def warning(self, message):

        self.logger.warning(message)