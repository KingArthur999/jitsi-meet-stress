import time
import multiprocessing
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

# =====================
# Chrome 配置
# =====================

def create_chrome_options():
    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")

    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--window-size=1280,720")

    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")

    return options


# =====================
# Worker
# =====================

def meeting_worker(worker_id, meet_url, duration, max_retry):
    for attempt in range(1, max_retry + 1):
        try:
            print(f"[Worker-{worker_id}] attempt {attempt}")

            service = Service(CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(
                service=service,
                options=create_chrome_options()
            )

            driver.get(meet_url)
            print(f"[Worker-{worker_id}] joined meeting")

            time.sleep(duration)
            driver.quit()

            print(f"[Worker-{worker_id}] exited normally")
            return

        except Exception as e:
            print(f"[Worker-{worker_id}] failed attempt {attempt}: {e}")
            time.sleep(10)

    print(f"[Worker-{worker_id}] give up after {max_retry} retries")


# =====================
# Main
# =====================

def main():
    parser = argparse.ArgumentParser("Jitsi meeting stress test")

    parser.add_argument("--server", default="https://meet.armonia.fund")
    parser.add_argument("--room", default="test1")
    parser.add_argument("--users", type=int, default=10)
    parser.add_argument("--duration", type=int, default=6000)
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--batch-interval", type=int, default=10)
    parser.add_argument("--retry", type=int, default=3)

    args = parser.parse_args()

    meet_url = (
        f"{args.server}/{args.room}"
        "#config.testing.testMode=true"
        "&config.disableNS=true"
        "&config.testing.noAutoPlayVideo=true"
        "&config.disableAEC=true"
        "&config.analytics.disabled=true"
        "&interfaceConfig.SHOW_CHROME_EXTENSION_BANNER=false"
        "&config.disable1On1Mode=false"
        "&config.p2p.useStunTurn=true"
        "&config.prejoinConfig.enabled=false"
        "&config.p2p.enabled=true"
        "&config.requireDisplayName=false"
        "&config.toolbarConfig.alwaysVisible=true"
        "&config.gatherStats=false"
        "&config.debug=false"
        "&config.enableTalkWhileMuted=false"
        "&config.startWithVideoMuted=true"
        "&config.callStatsID=false"
        "&interfaceConfig.DISABLE_FOCUS_INDICATOR=true"
    )

    print("[Main] starting meeting stress test")
    print(f"[Main] server={args.server}")
    print(f"[Main] room={args.room}")
    print(f"[Main] users={args.users}")
    print(f"[Main] duration={args.duration}s")

    multiprocessing.set_start_method("spawn", force=True)

    processes = []

    for i in range(0, args.users, args.batch_size):
        print(f"[Main] starting batch {i + 1} ~ {min(i + args.batch_size, args.users)}")

        for j in range(i, min(i + args.batch_size, args.users)):
            p = multiprocessing.Process(
                target=meeting_worker,
                args=(j + 1, meet_url, args.duration, args.retry)
            )
            p.start()
            processes.append(p)

        time.sleep(args.batch_interval)

    for p in processes:
        p.join()

    print("[Main] all workers finished")


if __name__ == "__main__":
    main()
