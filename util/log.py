from config.config import Config
import time


class Logger:
    @classmethod
    def log(cls, string):
        file = Config.ROOT_PATH + "/log/api.log"
        with open(file, 'a') as f:
            string = "\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + string
            f.write(string)
            print(string)
