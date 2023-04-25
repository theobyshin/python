import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, datetime, string

url_login = 'https://futuredesigner.net/login/email'
url_point_reg = ''
fcp_id = ''
fcp_pw = ''

# 로그인
driver = webdriver.Chrome('/Users/jake/Desktop/theo/python/터져라 사이트/chromedriver')
driver.get(url_login)
time.sleep(1)

input = driver.find_elements(By.TAG_NAME, 'input')
input[0].send_keys(fcp_id)
input[1].send_keys(fcp_pw)
input[1].send_keys(Keys.RETURN)
time.sleep(1)

# 포인트 발급페이지 접근
driver.get(url_point_reg)
time.sleep(1)

points = 0
email_address = ''
input_validate = ''
use_validate = ''

# 발급한 포인트 가져오기
point_div = driver.find_elements(By.CLASS_NAME, 'pointreg_1_td')
points = point_div[2].find_element(By.TAG_NAME, 'input').get_attribute('placeholder')

# 입력유효기간
input_date = driver.find_elements(By.CLASS_NAME, 'react-datepicker__input-container')
input_validate = input_date[1].find_element(By.TAG_NAME, 'input').get_attribute('placeholder')[:-6]

# 사용유효기간
use_date = driver.find_elements(By.CLASS_NAME, 'pointreg_1_td')
use_validate = use_date[4].find_element(By.TAG_NAME, 'input').get_attribute('placeholder')

# 포인트 정보 담을 어레이 생성
point_arr = []

# 칼럼명 주워담기 (0번째에 넣기)
point_arr.append(['순서', '포인트', '코드번호', '메일주소', '입력유효기간', '사용유효기간'])

# 갯수 확인
p_count_div = 4
count = driver.find_element(By.CLASS_NAME, 'pointreg_1-div')
p_count = int(count.find_element(By.TAG_NAME, 'input').get_attribute('placeholder'))

if p_count%p_count_div == 0:
    page = p_count//p_count_div
else:
    page = (p_count//p_count_div) + 1

# print('페이지', page)
# p_count/4 했을 때 몫이 2 이상이면 클릭해서 데이터 긁어야 함
# 나머지가 없으면 그 페이지까지, 나머지가 있으면 +1페이지까지 해야 함

code_index = 1
active_page = 0

for i in range(1, page+1):
    # 테이블 데이터 접근
    table = driver.find_element(By.CLASS_NAME, 'pointreg_table')
    point_code = table.find_elements(By.CLASS_NAME, 'pointreg_tb_code') #리스트
    # 이메일도 이런 형식으로 가져오면 될 듯

    # 필요한 데이터 수집해서 넣기
    for value in point_code:
        value = value.get_attribute('innerText')
        point_arr.append([code_index, points, value, '', input_validate, use_validate])
        code_index += 1

    print('{} 페이지 데이터 긁기 완료'.format(i))

    if page == 1 or i == page :
        break

    else:
        # 다음 페이지 접근
        # 페이지 접근 관련 
        page_class = driver.find_element(By.CLASS_NAME, 'pagination')
        pagenation = page_class.find_elements(By.TAG_NAME, 'li')
        
        for x, y in enumerate(pagenation):
            
            if y.get_attribute('class') == 'active':
                active_page = x
                break
        
        pagenation[active_page+1].find_element(By.TAG_NAME, 'a').send_keys(Keys.RETURN)
        # time.sleep(1)
        print('다음 {}페이지 이동완료'.format(i+1))
        print()

dt_now = str(datetime.datetime.now().date())[2:]
dt_now = dt_now.translate(str.maketrans('', '', string.punctuation))

# 다운로드
df = pd.DataFrame(columns=point_arr[0], data = point_arr[1:])
df.to_csv('/Users/jake/Desktop/'+'[{}]포인트_코드발급.csv'.format(dt_now) , encoding='utf-8-sig')