import os
import streamlit as st
import sys
from module.streamlit_youtube import (
    get_max_frame, 
    get_yt_frame, 
    save_upload_file
)
from streamlit import session_state as state

def get_state(value):
    if value not in state:
        state[value] = False

def set_state(value):
    state[value] = True

# 収集モードのオプション設定
def collection_mode():
    
    col = st.columns([1.5,8.5])
    col[0].write('YouTube URL')
    playlistURL_type = "https://www.youtube.com/playlist?list="
    singleURL_type = "https://www.youtube.com/watch?v="
    
    # 入力するURLがプレイリストなのかを設定
    playlist_flag = col[1].checkbox(label='playlist')
    if playlist_flag: 
        value_type=playlistURL_type
    else: 
        value_type=singleURL_type
    url = st.text_input(
        label=" ",
        label_visibility='collapsed',
        value=value_type
    )

    # メンバー限定動画なのかを設定
    browser = None
    if st.checkbox(label='members-only'):
        # 使用するクッキーのブラウザを選択
        browser = st.radio(
            label='Unused browser type in your having (Unlocked cookie type)',
            options=('chrome', 'edge'),
            index=0,
            horizontal=True,
        )
        # クッキーキーとクッキーをアップロード(一時利用)
        if browser=='chrome': 
            eg_key_path = 'C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Local State'
            eg_cookies_path = 'C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies'
        else:
            eg_key_path = 'C:\\Users\\user\\AppData\\Local\\Microsoft\\Edge\\User Data\\Local State'
            eg_cookies_path = 'C:\\Users\\user\\AppData\\Local\\Microsoft\\Edge\\User Data\\Profile 1\\Network\\Cookies'
        save_upload_file('Local State', eg_key_path)
        cookies_path = save_upload_file('Cookies', eg_cookies_path)
        if cookies_path!=None: cookies_dir = os.path.dirname(cookies_path)
    
    get_state('check_yt_clicked')
    if st.button('Check YouTube URL'): set_state('check_yt_clicked')
    if state.check_yt_clicked:
        get_state('yt_slider_changed')
        if not state.yt_slider_changed:
            state.max_frame_list = get_max_frame(url, browser, cookies_dir)
        for max_frame in state.max_frame_list:
            if st.slider('Frame position of YouTube', 0, max_frame) >= 0: set_state('yt_slider_changed')

    target_1p_chara_list = st.multiselect(
        label='Characters you want to study',
        options=('BYLETH','KAMUI','REFLET')
    )
    
    title_category = st.radio(
        label='YouTube title category',
        options=('VIP', 'smashmate', 'online', 'offline', 'other'),
        index=0,
        horizontal=True,
    )

# 対戦データを収集するモードにするか、対戦動画を観賞するモードにするか、を選択
def mode_select():
    mode = st.radio(
        label='App mode',
        options=('collection', 'veiwer'),
        index=0,
        horizontal=True,
    )
    if mode=='collection': 
        collection_mode()
        
if __name__ == '__main__':
    if st.button('All Parameters Reset'):
        for key in state.keys():
            del state[key]
    st.title('SSBU 1on1 Collection APP\nfor online matches only')
    st.write(sys.platform)
    mode_select()
