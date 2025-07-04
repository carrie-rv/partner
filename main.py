from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import traceback

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_message(message):
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("✅ Slack 전송 성공")
        else:
            print(f"❌ Slack 전송 실패! 상태코드: {response.status_code}, 응답: {response.text}")
    except Exception as e:
        print(f"Slack 전송 중 예외 발생: {e}")

start_time = time.time()

try: 
    # 웹드라이버 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 이동 URL
    url = "https://sandbox-cms.dev.kakaopage.com/auth/login_sp"
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # 로그인 정보
    username = "carrie.rv"
    password = "#"

    # 페이지 로딩 또는 특정 요소 등장까지 대기
    wait.until(EC.visibility_of_element_located((By.NAME, "id")))

    # 아이디 입력
    username_field = wait.until(EC.element_to_be_clickable((By.NAME, "id")))
    username_field.send_keys(username)

    # 비밀번호 입력
    password_field = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
    password_field.send_keys(password)

    # 로그인 버튼 클릭
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div/form/div[3]/button")))
    login_button.click()

    # 작품 등록 화면 진입
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/nav/div[2]/div[1]/div[3]/a/span"))).click()

    # 발행자 입력
    cp_field = wait.until(EC.presence_of_element_located((By.NAME, "publisherField")))
    cp_field.send_keys("carrie02global")
    cp_field.send_keys(Keys.ENTER)

    # 작품 언어 선택
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), '언어 선택')]")
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@data-value='TH']")#태국어 TH / 한국어 KO
        )
    ).click()

    # 작품명 입력
    wait.until(EC.presence_of_element_located((By.NAME, "seriesTitle"))).send_keys("kakaowebtoon_load_250625_slack")
    wait.until(EC.presence_of_element_located((By.NAME, "seriesTitleKor"))).send_keys("kakaowebtoon_load_250625_slack")

    # 카테고리 선택
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), '카테고리 선택')]")
        )
    ).click()
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '만화')]"))
    ).click()

    # 서브 카테고리 선택
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), '장르 선택')]")
        )
    ).click()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@data-value='116']") #115 판타지/ 116 드라마/ 121 로맨스/ 69 로판/ 112 무협/ 122 액션/ 119 BL
        )
    ).click()

    # 맵핑 작품 ID 입력
    kw_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='카카오웹툰 작품 ID 입력']")))
    kw_field.send_keys("328")
    kw_field.send_keys(Keys.ENTER)

    # 연령등급 선택
    age_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '등급 선택')]"))
    )
    age_field.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='popover-inner-wrapper']/div/div/div/button[1]/div/span"))).click()

    # 작품소개 입력
    wait.until(EC.presence_of_element_located((By.NAME, "seriesDescription"))).send_keys("kakaowebtoon_load_with_selenium")

    # 작가명 입력 및 선택
    author_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='작가명 입력']")))
    author_field.send_keys("캐리_태국")
    time.sleep(1)
    author_field.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(Keys.ENTER)

    author_type_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., '글')]"))
    )
    author_type_field.click()

    # 검색 키워드 입력
    keyword_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='검색 키워드 입력']")))
    keyword_field.send_keys("캐리")
    keyword_field.send_keys(Keys.ENTER)

    # 테마 키워드 선택
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '테마키워드 추가')]"))
    ).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='modal-wrapper']/div[2]/div[1]/table/tbody/tr[3]/td/div/button[1]/span"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='modal-wrapper']/div[2]/div[2]/button[2]"))).click()

    # 면세코드 및 가격 입력
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='taxFreeInfo.taxFreeCodeInfo.taxFreeCode']"))).send_keys("9791160402254")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='taxFreeInfo.perPrice']"))).send_keys("200")

    # 이미지 업로드
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))).send_keys("/Users/kakaoent/Desktop/셀레니움/KW.jpg")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='portraitImage']")))

    # 저장 클릭 및 URL 변경 대기
    current_url = driver.current_url
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/header/div[2]/button[2]"))).click()
    wait.until(EC.url_changes(current_url))

    # 상세 페이지 로딩 후 '회차' 탭 클릭
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '회차')]"))
    ).click()

    # 회차 추가 버튼 클릭
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '회차 추가')]"))
    ).click()

    current_url = driver.current_url

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), '카카오웹툰 회차')]")
        )
    ).click()

    wait.until(EC.url_changes(current_url))

    #카카오웹툰 회차 가져오기
    checkbox = wait.until(
        EC.element_to_be_clickable((By.ID, "selectAllSeriesToChange"))
    )
    checkbox.click()

    #시리즈 가져오기
    wait.until(
        EC.element_to_be_clickable(
            (By.ID, "btnMoveSeriesToChanging")
        )
    ).click()

    #회차 심사신청 화면 이동
    wait.until(
        EC.element_to_be_clickable((By.ID, "btnImport"))
    ).click()

    # 첫 번째 '심사신청' 버튼 클릭 (팝업 내)
    current_url = driver.current_url

    first_submit = wait.until(
        EC.element_to_be_clickable((By.ID, "btnSubmit"))
    )
    first_submit.click()

    # URL 변경될 때까지 대기 (심사신청 페이지로 이동)
    wait.until(EC.url_changes(current_url))

    # 새 페이지에서 두 번째 '심사 신청하기' 버튼 클릭
    second_submit = wait.until(
        EC.element_to_be_clickable((By.ID, "btnSubmit"))
    )
    second_submit.click()

    wait.until(EC.url_changes(current_url))

    print("두 단계 심사신청 완료")

    end_time = time.time()
    execution_time = end_time - start_time

    # ✅ 성공 시 Slack 알림
    send_slack_message(f"✅ Selenium 자동화 성공!\n소요 시간: {execution_time:.2f}초\n테스트: 심사신청까지 정상 완료 🎉")

except Exception as e:
    error_msg = traceback.format_exc()
    send_slack_message(f"❌ Selenium 테스트 실패:\n```{error_msg}```")

finally:
    driver.quit()