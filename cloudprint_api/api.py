import requests
from config import config

def get_cookies():
    cookie_raw = config["CLOUDPRINT_RAW_COOKIE"]
    cookies = {}

    for cookie in cookie_raw.split("; "):
        name, val = cookie.split("=")
        cookies[name] = val

    return cookies

# job filters
id_to_name = {"2857162788A9A790DF78": "Kyle", "2857162788A9A790DF84": "Caroline"}
waiting = lambda j: j["status"] == "waiting"
kyle = lambda j: id_to_name[j["printerId"]] == "Kyle"
caroline = lambda j: id_to_name[j["printerId"]] == "Caroline"
display = lambda q: (id_to_name[q["printerId"]], q['printerId'], q["fileName"], q["status"], q["id"])


def deploy_job(j):
    cookies = get_cookies()

    req = requests.post(
            f"https://cloudprint.makerbot.com/queue/job/{j['id']}",
            cookies=cookies,
            json={
                "jobId": j["id"],
                "printerId": j["printerId"],
            }
        )

    breakpoint()

    print(req.text)

    return req

def get_jobs():
    cookies = get_cookies()

    r = requests.get("https://cloudprint.makerbot.com/queue/jobs", cookies=cookies)

    data = r.json()

    return list(filter(waiting, data))

def get_printer_availability():
    cookies = get_cookies()

    r = requests.get("https://cloudprint.makerbot.com/org/live-printers-info",cookies=cookies)

    data = r.json()

    return [(p['id'], p['status']['current_process'] is None) for p in data]

def get_queue_count():
    jobs = get_jobs()
    n_kyle, n_caroline = len(list(filter(kyle, jobs))), len(list(filter(caroline, jobs)))
    return n_kyle, n_caroline

if __name__ == "__main__":
    jobs = (get_jobs())
    print(list(map(display, jobs)))

    for printer, available in get_printer_availability():
        print(printer, "is" if available else "is not", "available")
        if available:
            print("deploying job")
            j = next(job for job in jobs if job["printerId"] == printer)
            deploy_job(j)

    # print(get_queue_count())
