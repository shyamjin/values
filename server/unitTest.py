'''
    General description:
        This is responsible to perform Selenium Testing
        All 'py files inside Testing.TestCases module and having "test"\
             in there names will be handled
'''

from concurrent.futures import ThreadPoolExecutor, wait

from Testing import ApiTest



if __name__ == '__main__':
    futures = []
    pool = ThreadPoolExecutor(1,__name__+".__name__")
    futures.append(pool.submit(ApiTest.main))
    wait(futures,timeout=600)

    # CHECK EXCEPTIONS
    exceptions =[]
    for future in futures:
        if future.exception():
            exceptions.append(str(future.exception()))
    if exceptions:
        for exp in exceptions:
            print exp
        raise Exception(",".join(exceptions))            