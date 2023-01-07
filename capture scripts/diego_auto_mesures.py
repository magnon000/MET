import os
import time
import functools  # need pip install
import schedule  # need pip install
import datetime

ping_file = 'logs/sfr.fr/ping_laciotat.txt'  # change txt file name here for different Internet connections
route_file = 'logs/sfr.fr/tracert_laciotat.txt'
curl_file = 'logs/sfr.fr/curl_laciotat.txt'
tcp_file = 'logs/sfr.fr/tcp_laciotat.txt'

compteur_tcp = 5

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

def plan():
    print("debut nouveau cycle")
    global compteur_tcp
    ping_test()
    route_test()
    curl_test()
    if(compteur_tcp>3):
        tcp_test()
        compteur_tcp = -1
    compteur_tcp += 1
    print("fin cycle")



@catch_exceptions(cancel_on_failure=False)
def ping_test(wfile=ping_file):
    print("debut ping")
    # check windows security if commands can not run
    # time_now = time.asctime()
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_ping = 'ping -c 100 -s 16 sfr.fr'
    ping = os.popen(cmd_ping)
    ping_str = ping.read()
    if not ping_str:
        ping_str = 'error'
    print(time_now, ping_str)
    # record time and ping infos, check windows security if fail
    wfile = open(ping_file, 'a+')
    wfile.write(time_now+ '\n' + ping_str + '\n')
    wfile.close()
    print("fin ping")


@catch_exceptions(cancel_on_failure=False)
def route_test(wfile=route_file):
    print("debut route")
    # time_now = time.asctime()
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_route = 'traceroute sfr.fr'
    route = os.popen(cmd_route)
    route_str = route.read()
    if not route_str:
        route_str = 'error'
    print(time_now, route_str)
    # record route infos, check windows security if fail
    wfile = open(route_file, 'a+')
    wfile.write(time_now + '\n' + route_str + '\n')
    wfile.close()
    print("fin route")

@catch_exceptions(cancel_on_failure=False)
def curl_test(wfile=curl_file):
    print("debut curl")
    # time_now = time.asctime()
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_curl = "curl -s -w 'Testing Website Response Time for :%{url_effective}\n\nLookup Time:\t\t%{time_namelookup}\nConnect Time:\t\t%{time_connect}\nAppCon Time:\t\t%{time_appconnect}\nRedirect Time:\t\t%{time_redirect}\nPre-transfer Time:\t%{time_pretransfer}\nStart-transfer Time:\t%{time_starttransfer}\n\nTotal Time:\t\t%{time_total}\n' -o /dev/null https://www.sfr.fr"
    curl = os.popen(cmd_curl)
    curl_str = curl.read()
    if not curl_str:
        curl_str = 'error'
    print(time_now, curl_str)
    # record curl infos, check windows security if fail
    wfile = open(curl_file, 'a+')
    wfile.write(time_now + '\n' + curl_str + '\n \n \n')
    wfile.close()
    print("fin curl")

@catch_exceptions(cancel_on_failure=False)
def tcp_test(wfile=tcp_file):
    print("debut tcp")
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    os.popen('echo "\n \n \n \n \n'+time_now+'" >> logs/sfr.fr/tcp_laciotat.txt')
    cmd_tcpdump = 'timeout 30s tcpdump host sfr.fr -vvv >> logs/sfr.fr/tcp_laciotat.txt'
    tcp = os.popen(cmd_tcpdump)
    time.sleep(2)
    os.popen('curl https://www.sfr.fr -L')
    #tcp_str = tcp.read()
    #if not tcp_str:
    #    tcp_str = 'error'
    #print(time_now, tcp_str)
    # record tcp infos, check windows security if fail
    #wfile = open(tcp_file, 'a+')
    #wfile.write(time_now + '\n' + tcp_str + '\n')
    #wfile.close()
    print("fin tcp")

print("ça marche")


plan()
schedule.every(15).minutes.do(plan)


while True:
    schedule.run_pending()  # run all tasks
    time.sleep(1)
