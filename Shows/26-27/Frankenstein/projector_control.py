import urllib.request
import urllib.error
import time

projector_ips = ["192.168.1.2", "192.168.1.3", "192.168.1.4"]

username = "EPSONWEB"
password = "12345678"

def toggle_av_mute(ip):
    timestamp = int(time.time() * 1000)
    url = f"http://{ip}/cgi-bin/Remote/directsend?KEY=3E&_={timestamp}"

    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, f"http://{ip}/", username, password)

    auth_handler = urllib.request.HTTPDigestAuthHandler(password_mgr)

    opener = urllib.request.build_opener(auth_handler)

    try:
        req = urllib.request.Request(url, method="GET")

        req.add_header("X-Requested-With", "XMLHttpRequest")
        req.add_header("Referer", f"http://{ip}/cgi-bin/Remote/Basic_Control")
        req.add_header("Accept", "text/plain, */*; q=0.1")

        with opener.open(req, timeout=3) as response:
            if response.status == 200:
                print(f"[Success] Sent AV Mute toggle to projector at {ip}")
            else:
                print(f"[Warning Projector at {ip}] responded with status: {response.status}")
    except urllib.error.HTTPError as e:
            print(f"[Error] HTTP error for {ip}: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        print(f"[Error] Could not reach projector atg {ip}: {e.reason}")
    except Exception as e:
        print(f"[Error] Unexpected error for {ip}: {e}")

def main():
    print("Sending AV Mute toggle commant to Epson PowerLite 815e projectors...")
    for ip in projector_ips:
        toggle_av_mute(ip)
    print("Done.")

if __name__ == "__main__":
    main()