import os
import time
import functools  # need pip install
import schedule  # need pip install
import datetime

ping_file = 'ping_quantic_direct_ipv4.txt'  # change txt file name here for different Internet connections
route_file = 'tracert_quantic_direct_ipv4.txt'


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


@catch_exceptions(cancel_on_failure=False)
def ping_test(wfile=ping_file):
    # check windows security if commands can not run
    # time_now = time.asctime()
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_ping = 'ping sfr.fr -4'
    ping = os.popen(cmd_ping)
    ping_str = ping.read()
    if not ping_str:
        ping_str = 'error'
    print(time_now, ping_str)
    # record time and ping infos, check windows security if fail
    wfile = open(ping_file, 'a+')
    wfile.write(time_now + ping_str + '\n')
    wfile.close()


@catch_exceptions(cancel_on_failure=False)
def route_test(wfile=ping_file):
    # time_now = time.asctime()
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_route = 'tracert -4 sfr.fr'
    route = os.popen(cmd_route)
    route_str = route.read()
    if not route_str:
        route_str = 'error'
    print(time_now, route_str)
    # record route infos, check windows security if fail
    wfile = open(route_file, 'a+')
    wfile.write(time_now + route_str + '\n')
    wfile.close()


schedule.every(2).minutes.do(ping_test)
schedule.every(2).minutes.do(route_test)

while True:
    schedule.run_pending()  # run all tasks
    time.sleep(1)
