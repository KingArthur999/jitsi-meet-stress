from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

MEET_URL = (
    "https://meet.armonia.fund/test1"
    "#config.startWithVideoMuted=false"
    "&config.startWithAudioMuted=false"
    "&config.requireDisplayName=true"
)

def chrome_options():
    o = Options()
    # ❗ 不要 headless，方便你亲眼看
    o.add_argument("--use-file-for-fake-video-capture=/root/fake.y4m")

    o.add_argument("--no-sandbox")
    o.add_argument("--disable-gpu")
    o.add_argument("--use-fake-ui-for-media-stream")
    o.add_argument("--use-fake-device-for-media-stream")
    return o

if __name__ == "__main__":
    print("[DEBUG] launching single client")

    driver = webdriver.Chrome(
        service=Service("/usr/local/bin/chromedriver")
,  # 本机路径
        options=chrome_options()
    )

    driver.get(MEET_URL)
    print("[DEBUG] joined meeting")

    # 保持 5 分钟，方便你观察
    time.sleep(300)

    driver.quit()
