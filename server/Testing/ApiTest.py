'''
    General description:
        This is responsible to perform Selenium Testing
        All 'py files inside Testing.TestCases module and having "test"\
             in there names will be handled
'''

import importlib
import os
from concurrent.futures import ThreadPoolExecutor, wait

from settings import current_path


ONLY_FILES = [f for f in os.listdir(os.path.join(current_path, "Testing", "UnitTests"))
              if os.path.isfile(os.path.join(os.path.join(current_path, "Testing", "UnitTests"), f))
              if str(str(f).lower()).endswith(".py") if "test" in str(str(f).lower())]
# SORT FILES BY CREATE DATE
ONLY_FILES.sort(key=lambda fn: os.path.getmtime(
    os.path.join(os.path.join(current_path, "Testing", "UnitTests"), fn)))

def main():
    print "####################### START API TESTING #####################"
    futures = []
    pool = ThreadPoolExecutor(5,__name__+".export_tools_for_new_sync")
    for class_name in ONLY_FILES:
        module = importlib.import_module(
            'Testing.UnitTests.' + class_name[:-3])
        futures.append(pool.submit(module.main))
    wait(futures,timeout=len(futures)*60) # 1 min for every test case

    # CHECK EXCEPTIONS
    exceptions =[]
    for future in futures:
        if future.exception():
            exceptions.append(str(future.exception()))
    if exceptions:
        raise Exception(",".join(exceptions))            