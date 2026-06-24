import streamlit as st
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import io

st.title("学習助男(すけお) by Koshkin")

# セッション状態の初期化
if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""

# URL 入力
url = st.text_input("URL を入力してください:", value="https://www.google.com")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("開く"):
        # 既存のドライバーを閉じる
        if st.session_state.driver:
            st.session_state.driver.quit()
        
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Renderでは /usr/bin/chromium-browser
            if os.path.exists('/usr/bin/chromium-browser'):
                options.binary_location = '/usr/bin/chromium-browser'

            driver = webdriver.Chrome(options=options)
            driver.set_window_size(1920, 1080)
            driver.get(url)
            st.session_state.driver = driver
            st.session_state.current_url = url
        except Exception as e:
            st.error(f"エラー: {e}")

with col2:
    if st.button("↓ スクロール下"):
        if st.session_state.driver:
            st.session_state.driver.execute_script("window.scrollBy(0, 300);")

with col3:
    if st.button("↑ スクロール上"):
        if st.session_state.driver:
            st.session_state.driver.execute_script("window.scrollBy(0, -300);")

# スクリーンショット表示
if st.session_state.driver:
    try:
        screenshot = st.session_state.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        st.image(image)
    except Exception as e:
        st.error(f"スクリーンショット取得エラー: {e}")
