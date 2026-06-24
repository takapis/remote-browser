import streamlit as st
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
        if st.session_state.driver:
            st.session_state.driver.quit()
        
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280,720")
    
            if os.path.exists('/usr/bin/chromium-browser'):
                options.binary_location = '/usr/bin/chromium-browser'

            # Service を指定せず、Selenium に自動検出させる
            driver = webdriver.Chrome(options=options)
            driver.set_window_size(1280, 720)
            driver.get(url)
            st.session_state.driver = driver
            st.session_state.current_url = url
        except Exception as e:
            st.error(f"エラーだわよ: {e}")
            
        # 「開く」ボタンの後に以下を追加

if st.session_state.driver:
    try:
        # JavaScript でパフォーマンス情報を取得
        perf_data = st.session_state.driver.execute_script("""
            var perf = window.performance.getEntriesByType('navigation')[0];
            return {
                'dns': perf.domainLookupEnd - perf.domainLookupStart,
                'tcp': perf.connectEnd - perf.connectStart,
                'ttfb': perf.responseStart - perf.requestStart,
                'download': perf.responseEnd - perf.responseStart,
                'dom': perf.domInteractive - perf.responseEnd,
                'total': perf.loadEventEnd - perf.fetchStart
            };
        """)
        
        st.write("**📊 ネットワーク詳細:**")
        st.write(f"- DNS 解決: {perf_data['dns']:.0f}ms")
        st.write(f"- TCP 接続: {perf_data['tcp']:.0f}ms")
        st.write(f"- TTFB (初回バイト): {perf_data['ttfb']:.0f}ms")
        st.write(f"- ダウンロード: {perf_data['download']:.0f}ms")
        st.write(f"- DOM 処理: {perf_data['dom']:.0f}ms")
        st.write(f"- **合計: {perf_data['total']:.0f}ms**")
    except:
        pass


with col2:
    if st.button("↓ スクロール下"):
        if st.session_state.driver:
            st.session_state.driver.execute_script("window.scrollBy(0, 300);")

with col3:
    if st.button("↑ スクロール上"):
        if st.session_state.driver:
            st.session_state.driver.execute_script("window.scrollBy(0, -300);")

# フルサイズボタン
if st.button("フルサイズ (1920x1080)"):
    if st.session_state.driver:
        st.session_state.driver.set_window_size(1920, 1080)

# スクリーンショット表示
if st.session_state.driver:
    try:
        screenshot = st.session_state.driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        st.image(image)
    except Exception as e:
        st.error(f"スクリーンショット取得エラー: {e}")
