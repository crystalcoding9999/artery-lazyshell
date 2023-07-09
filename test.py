import api
import os
from datetime import date, datetime
import shutil


def backup_database():
    if os.path.exists("main.sqlite"):
        now = str(date.today()) + "_" + str(datetime.now())
        now = now.replace(":", "_")

        target_dir = "./backups"
        src_file = "./main.sqlite"
        dst_file = target_dir + "/" + now + "_backup_main.sqlite"
        dst_file = dst_file.replace(" ", "_").replace("-", "_")
        shutil.copy(src_file, dst_file)

backup_database()
