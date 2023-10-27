import cv2
import streamlit as st
import yt_dlp
from cap_from_youtube import cap_from_youtube

#url = 'https://www.youtube.com/playlist?list=PLxWXI3TDg12zAPnbxJkz99IB_npRLLB3_'

def get_yt_info(url, browser=None):
    ydl_opts = {}
    if browser!=None:
        ydl_opts = {'cookiesfrombrowser' : (browser,)}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def get_max_frame(url, browser=None):
    infolist = get_yt_info(url, browser)
    max_frame = []
    if 'entries' in infolist.keys(): infolist = infolist['entries'] 
    else: infolist = [infolist]
    for info in infolist:
        hh, mm, ss = info['duration_string'].split(':')
        max_frame.append((int(hh)*60*60 + int(mm)*60 + int(ss)) * int(info['fps']))    
    return max_frame
    
def get_yt_frame(url, browser=None):
    ydl_opts = {'cookiesfrombrowser' : (browser,)}
    cap = cap_from_youtube(url, 'best', ydl_opts)
    
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280,720))
    cv2.imshow('video', frame)
    cv2.waitKey(0)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 9999) 
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280,720))
    cv2.imshow('video', frame)
    cv2.waitKey(0)

if __name__ == '__main__':
    get_yt_frame('https://www.youtube.com/watch?v=s3jWqbVw2ds','chrome')
