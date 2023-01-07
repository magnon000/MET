import os
import time
import functools  # need pip install
import schedule  # need pip install
import datetime

ping_file = 'logs/tv.sfr.fr/ping_laciotat_tv.txt'  # change txt file name here for different Internet connections
route_file = 'logs/tv.sfr.fr/tracert_laciotat_tv.txt'
curl_file = 'logs/tv.sfr.fr/curl_laciotat_tv.txt'
tcp_file = 'logs/tv.sfr.fr/tcp_laciotat_tv.txt'

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
    # check windows security if commands can not run
    # time_now = time.asctime()
    print("ping debut")
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_ping = 'ping -c 100 -s 16 tv.sfr.fr'
    ping = os.popen(cmd_ping)
    ping_str = ping.read()
    if not ping_str:
        ping_str = 'error'
    print(time_now, ping_str)
    # record time and ping infos, check windows security if fail
    wfile = open(ping_file, 'a+')
    wfile.write(time_now+ '\n' + ping_str + '\n')
    wfile.close()
    print("ping fin")


@catch_exceptions(cancel_on_failure=False)
def route_test(wfile=route_file):
    # time_now = time.asctime()
    print("route debut")
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_route = 'traceroute tv.sfr.fr'
    route = os.popen(cmd_route)
    route_str = route.read()
    if not route_str:
        route_str = 'error'
    print(time_now, route_str)
    # record route infos, check windows security if fail
    wfile = open(route_file, 'a+')
    wfile.write(time_now + '\n' + route_str + '\n')
    wfile.close()
    print("route fin")

@catch_exceptions(cancel_on_failure=False)
def curl_test(wfile=curl_file):
    # time_now = time.asctime()
    print("curl debut")
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cmd_curl = "curl -s -w 'Testing Website Response Time for :%{url_effective}\n\nLookup Time:\t\t%{time_namelookup}\nConnect Time:\t\t%{time_connect}\nAppCon Time:\t\t%{time_appconnect}\nRedirect Time:\t\t%{time_redirect}\nPre-transfer Time:\t%{time_pretransfer}\nStart-transfer Time:\t%{time_starttransfer}\n\nTotal Time:\t\t%{time_total}\n' -o /dev/null https://www.tv.sfr.fr"
    curl = os.popen(cmd_curl)
    curl_str = curl.read()
    if not curl_str:
        curl_str = 'error'
    print(time_now, curl_str)
    # record curl infos, check windows security if fail
    wfile = open(curl_file, 'a+')
    wfile.write(time_now + '\n' + curl_str + '\n \n \n')
    wfile.close()
    print("curl fin")

@catch_exceptions(cancel_on_failure=False)
def tcp_test(wfile=tcp_file):
    print("tcp debut")
    now = datetime.datetime.now()
    time_now = now.strftime('%Y-%m-%d %H:%M:%S')
    os.popen('echo "\n \n \n \n \n'+time_now+'" >> logs/tv.sfr.fr/tcp_laciotat_tv.txt')
    cmd_tcpdump = 'timeout 30s tcpdump host tv.sfr.fr -vvv >> logs/tv.sfr.fr/tcp_laciotat_tv.txt'
    tcp = os.popen(cmd_tcpdump)
    time.sleep(2)
    os.popen('curl https://www.tv.sfr.fr -L')
    print("tcp fin")
    #tcp_str = tcp.read()
    #if not tcp_str:
    #    tcp_str = 'error'
    #print(time_now, tcp_str)
    # record tcp infos, check windows security if fail
    #wfile = open(tcp_file, 'a+')
    #wfile.write(time_now + '\n' + tcp_str + '\n')
    #wfile.close()

print("ça marche")


schedule.every(15).minutes.do(plan)


while True:
    schedule.run_pending()  # run all tasks
    time.sleep(1)
