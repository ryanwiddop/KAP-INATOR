import os, logging, time, requests, sys, re

logger = logging.getLogger(__name__)

def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def delete_lines(n):
    for _ in range(n):
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")
        sys.stdout.flush()

def fetch_bouts_per_hour(
    jsessionid: str,
    when: int,
    event_id: int,
    division_ids: int = -1,
    host: str = "172.16.28.210:9090",
    timeout: int = 20):
    logger.info(f"Attempting fetch of bouts per hour from: {host}\n")

    base_url = f"http://{host}"
    url = f"{base_url}/otb/mvr/boutsPerHourReport"

    params = {
        "when": when,
        "divisionIds": division_ids,
        "eventId": event_id,
        "_dc": int(time.time() * 1000),
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": f"{base_url}/event?eventId={event_id}",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
    }

    session = requests.Session()

    session.cookies.set(
        "JSESSIONID",
        jsessionid,
        domain=host.split(":")[0],
        path="/",
    )

    resp = session.get(url, params=params, headers=headers, timeout=timeout)
    resp.raise_for_status()
    logger.info("Successful fetch")
    return resp


def build_prepared_request(
    jsessionid: str,
    when: int,
    event_id: int,
    division_ids: int = -1,
    host: str = "172.16.28.210:9090",
):
    logger.info("Building request\n")
    base_url = f"http://{host}"
    url = f"{base_url}/otb/mvr/boutsPerHourReport"
    params = {
        "when": when,
        "divisionIds": division_ids,
        "eventId": event_id,
        "_dc": int(time.time() * 1000),
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": f"{base_url}/event?eventId={event_id}",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/143.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
    }

    s = requests.Session()
    req = requests.Request(
        "GET",
        url,
        headers=headers,
        params=params,
        cookies={"JSESSIONID": jsessionid},
    )
    prepped = s.prepare_request(req)
    return prepped

def get_event_id(jsessionid: str, when: int, event_id: int,
                 division_ids: int = -1, host: str = "172.16.28.210:9090"):
    return None

def mat_velocity_predictor():
    jsid = ""
    eId = 0
    startString = ""
    totalBouts = 0
    divisionId = -1
    host = "172.16.28.210:9090"
    timeout = 20
    cmd = ""
    while (cmd != "c"):
        print(f"Fill in the required fields and review optional.\nREQUIRED:")
        print(f"  (1) jsessionid:\t{jsid}")
        print(f"  (2) event id:\t\t{eId}")
        print(f"  (3) start time:\t{startString}")
        print(f"  (4) total bouts:\t{totalBouts}")
        print(f"OPTIONAL (default values loaded):")
        print(f"  (5) division id:\t{divisionId}")
        print(f"  (6) host:\t\t{host}")
        print(f"  (7) timeout:\t\t{timeout}ms")
            
        cmd = (input("\n\nEnter a line # to edit, c to continue, or q to quit: "))
        
        line_count = 13
        if cmd == 'q':
            print("Goodbye!")
            exit(1)

        while(cmd != 'c' and (int(cmd) < 1 or int(cmd) > 7)):
            delete_lines(2)
            print("Invalid input!")
            cmd = (input("Enter a line # to edit, c to continue, or q to quit: ")).lower()
        
        if cmd == 'c':
            delete_lines(1)
            continue
            
        match cmd:
            case '1':
                jsid = input("jsessionid (Inspect -> Application -> Cookies -> JSESSIONID): ")
                delete_lines(line_count + 1)
            case '2':
                eId = int(input("event id: "))
                delete_lines(line_count + 1)
            case '3':
                startString = input("start time (HH:MM AM/PM): ")
                while (re.match("([0-1]?[0-9]|2[0-3]):[0-5][0-9] ([AaPp][Mm])", startString) == None):
                    delete_lines(1)
                    startString = input("Invalid format! start time (HH:MM AM/PM): ")
                delete_lines(line_count + 1)
            case '4':
                totalBouts = int(input("total bouts: "))
                delete_lines(line_count + 1)
            case '5':
                divisionId = int(input("division id (-1 selects all): "))
                delete_lines(line_count + 1)
            case '6':
                host = input("host (IP:PORT): ")
                while(re.match(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d{1,5}", host) == None):
                    delete_lines(1)
                    print("Invalid format! host (IP:PORT): ")
                delete_lines(line_count + 1)
            case '7':
                timeout = int(input("timeout: "))
                delete_lines(line_count + 1)

    now = time.localtime()
    
    zeroed_now = time.struct_time((
        now.tm_year,
        now.tm_mon,
        now.tm_mday,
        0, 0, 0,
        now.tm_wday,
        now.tm_yday,
        now.tm_isdst,
    ))
    date_epoch = int(time.mktime(zeroed_now))
    
    # if args.prepare_only:
    #     prepped = build_prepared_request(
    #         jsessionid=jsid,
    #         when=date_epoch,
    #         event_id=args.event_id,
    #         division_ids=args.division_ids,
    #         host=args.host,
    #     )
    #     print("Prepared URL:", prepped.url)

    #     hdrs = dict(prepped.headers)
    #     if "Cookie" not in hdrs:

    #         hdrs["Cookie"] = f"JSESSIONID={jsid}"
    #     print("Prepared Headers:")
    #     print(json.dumps(hdrs, indent=2))
    #     return 0

    startHour = int(startString.split(":")[0])
    if startString.split(" ")[1] == "PM":
        startHour += 12
    startMin = int(startString.split(":")[1].split(" ")[0])
    
    startTime = time.struct_time((
        now.tm_year,
        now.tm_mon,
        now.tm_mday,
        startHour, startMin, 0,
        now.tm_wday,
        now.tm_yday,
        now.tm_isdst,
    ))
    
    while(True):
        try:
            resp = fetch_bouts_per_hour(
                jsessionid=jsid,
                when=date_epoch,
                event_id=eId,
                division_ids=divisionId,
                host=host,
                timeout=timeout,
            )
        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
            if e.response is not None:
                print("Response text:")
                print(e.response.text)
            return 2
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return 3


        try:
            logger.info("Dumping JSON of response\n")
            data = resp.json()
        except ValueError:
            print(resp.text)
            return 4

        mat_data = {}
        for mat in data["matVelocityList"]:
            mat_sequence = mat["matSequence"]
            sorted_counts = dict(sorted(mat["matHourlyBoutCount"].items(), key=lambda x: int(x[0])))
            mat_data[mat_sequence] = {
                "matId": mat["matId"],
                "matName": mat["matName"],
                "hourly_counts": sorted_counts,
            }

        # for mat_num in sorted(mat_data.keys()):
        #     info = mat_data[mat_num]
        #     print(f"\n{info['matName']} (ID: {info['matId']}):")
        #     print(f"  Hourly Bout Counts:")
        #     for epoch, count in info['hourly_counts'].items():
        #         print(f"    {epoch}: {count} bouts")
        

        elapsedBouts = 0
        currentTime = time.localtime()
        tempHours = currentTime.tm_hour + (currentTime.tm_min / 60)
        elapsedHours = int(tempHours - startHour)
        elapsedMins = int(((tempHours - int(tempHours)) - (startMin / 60)) * 60)

        for mat_num in mat_data:
            info = mat_data[mat_num]
            for epoch, count in info["hourly_counts"].items():
                elapsedBouts += count
        averageBPH = elapsedBouts / (elapsedHours + (elapsedMins / 60))
        remaingBouts = totalBouts - elapsedBouts
        
        remainingTime = (remaingBouts)/averageBPH
        # remainingHours = int(remainingTime)
        # remainingMins = int((remainingTime - int(remainingTime)) * 60)
        
        endTime = tempHours + remainingTime
        endHours = int(endTime)
        endMins = int((endTime - int(endTime)) * 60)

        endTime = time.struct_time((
            now.tm_year,
            now.tm_mon,
            now.tm_mday,
            endHours,
            endMins,
            0,
            now.tm_wday,
            now.tm_yday,
            now.tm_isdst,
        ))
        
        print(f"Time Remain:\t{int(remainingTime)}:{int((remainingTime - int(remainingTime))* 60)}")
        print(f"Total Bouts:\t{totalBouts}\n\
Elapsed Bouts:\t{elapsedBouts}\n\
Remain Bouts:\t{remaingBouts}\n\
Average BPH:\t{averageBPH}\n\
Remaing Time:\t{remainingTime}\n\
Current Time:\t{currentTime.tm_hour:02d}:{currentTime.tm_min:02d}\n\
Elapsed Time:\t{elapsedHours:02d}:{elapsedMins:02d}\n\
End Estimate:\t{endTime.tm_hour:02d}:{endTime.tm_min:02d}\n")
        
        time.sleep(5)        
