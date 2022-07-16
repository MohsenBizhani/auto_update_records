import sys
import subprocess
import pkg_resources

required = {'watchdog', 'numpy', 'pandas'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed


if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    
    
import numpy as np
import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os.path
from os import path

patterns = ["*.csv"]
ignore_patterns = None
ignore_directories = False
case_sensitive = True
my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

df = pd.DataFrame()
Path = ""



def on_created(event):
    df = pd.read_csv(event.src_path, engine = "python")
    Path = "result.csv"
    if (path.exists(Path)):
        data = pd.read_csv("result.csv", engine = "python")
        data.append(df)
        columns = ['fname', 'lname', 'mobile', 'stock']

        data.columns = columns
        data['index'] = data.index
        sh = data.shape

        dfs = data.sort_index('index')
        result = dfs.drop_duplicates('mobile', keep='last').values
        result = pd.DataFrame(result)
        columns = ['fname', 'lname', 'mobile', 'stock', 'index']
        result.columns = columns
        del result['index']
        os.remove(event.src_path)
        result.to_csv("result.csv", mode="a", index=False, sep=",")
    else:
        columns = ['fname', 'lname', 'mobile', 'stock']

        df.columns = columns
        df['index'] = df.index
        sh = df.shape

        dfs = df.sort_index('index')
        result = dfs.drop_duplicates('mobile', keep='last').values
        result = pd.DataFrame(result)
        columns = ['fname', 'lname', 'mobile', 'stock', 'index']
        result.columns = columns
        del result['index']
        os.remove(event.src_path)
        result.to_csv("result.csv", index=False, sep=",")

my_event_handler.on_created = on_created


_path = "."
go_recursively = False
my_observer = Observer()
my_observer.schedule(my_event_handler, _path, recursive=go_recursively)


my_observer.start()

try:
    while True:
        time.sleep(1000)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
