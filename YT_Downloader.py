# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 08:53:07 2024

@author: m_ali_s85f
"""
from pytubefix import YouTube
import moviepy.editor as mpe
from pathlib import Path
import os

url = input("Please Enter Video Link:")


downloads_path = str(Path.home() / "Downloads")
download_folder = downloads_path + "\YoutubeDownloads_byTuran"


yt = YouTube(url)

def get_resolutions(stream_query):
    resolutions = []
    for res in stream_query:
        if (res.resolution not in resolutions):
            resolutions.append(res.resolution)
    return resolutions


def change_url():
    url = input("Please Enter Video Link:")
    return url

def downloader(res):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    video = yt.streams.filter(res=res).first()
    if video.is_progressive == True:
        video.download()
    else:
        video.download(filename=f"{download_folder}\\video1.mp4")
        yt.streams.filter(type="audio").order_by("abr").desc().first().download(filename=f"{download_folder}\\audio1.mp3")
        video_combiner(res)
        
        
def audio_download():
    yt.streams.filter(type="audio").order_by("abr").desc().first().download(filename=f"{download_folder}\\{yt.title}.mp3")
    print("Download Completed!")
    
    
def video_combiner(res):

    my_clip = mpe.VideoFileClip(f"{download_folder}\\video1.mp4")
    audio_background = mpe.AudioFileClip(f"{download_folder}\\audio1.mp3")
    final_clip = my_clip.set_audio(audio_background)
    video_name = input("Please Enter A Video Title After Saving:")
    final_clip.write_videofile(f"{download_folder}\\{video_name}.mp4", codec="libx264")
    os.remove(f"{download_folder}\\video1.mp4")
    os.remove(f"{download_folder}\\audio1.mp3")
    print("Download Completed!")
 

while True:
    print("1-Change URL\n2-Download Video\n3-Download Audio\n0-Exit")
    cevap = int(input("Choice:"))
    if cevap == 1:
        url = change_url()
    if cevap == 2:
        resolutions = list(enumerate(get_resolutions(yt.streams.filter(file_extension="mp4",type="video").order_by("resolution"))))
        for order,res in resolutions:
            print(f"{order}-{res}")
        down_res = int(input("İndirmek istediğiniz çözünürlüğü giriniz:"))
        downloader(resolutions[down_res][1])
    if cevap == 3:
        audio_download()
    if cevap == 0:
        break