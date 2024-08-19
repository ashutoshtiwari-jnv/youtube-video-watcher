import os
import time
import threading
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyautogui

# YouTube Data API configuration
def get_channel_id_from_url(url):
    query = urlparse(url).query
    params = parse_qs(query)
    return params.get('channel', [None])[0]

def get_latest_videos(api_key, channel_id, max_results):
    print('API KEY nreee:',api_key)
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Fetch the latest videos from the channel
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=max_results,
        order='date',
        type='video'
    )
    response = request.execute()
    print('response:',response)

    video_urls = ['https://www.youtube.com/watch?v=' + item['id']['videoId'] for item in response['items']]
    return video_urls

def watch_video(video_url, output_text, rewatch_count):
    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()))
    driver.get(video_url)
    
    # Wait for the video to load
    time.sleep(5)
    
    # Get video duration and wait for that time to simulate watching
    duration = driver.execute_script("return document.querySelector('.video-stream').duration;")
    print('duration:', duration)
    print('rewatch_count:',rewatch_count)
    
    for i in range(rewatch_count):
        print('watching start')
        pyautogui.press('space')
        output_text.insert(tk.END, f'Watching video {i+1}/{rewatch_count}: {video_url}\n')
        print('waiting 16 second')
        time.sleep(duration)  # Simulate watching the video
        print('watching completed')
        output_text.insert(tk.END, f"Finished watching {i+1}/{rewatch_count}: {video_url}\n")
    
    print('rewatch completed')
    driver.quit()

def execute_task(api_key, channel_id, video_count, rewatch_count, output_text):
    print('api_key:', api_key)
    print('channel_id:', channel_id)
    # channel_id = get_channel_id_from_url(channel_id)
    print('channel_id:', channel_id)
    if not channel_id:
        output_text.insert(tk.END, "Invalid Channel URL.\n")
        return
    print('going to this function')
    video_urls = get_latest_videos(api_key, channel_id, video_count)
    print('video_urls',video_urls)
    
    # Watch each video the specified number of times
    for url in video_urls:
        watch_video(url, output_text, rewatch_count)
        time.sleep(2)  # Small delay before watching the next video

def start_task(api_key, channel_id, video_count, rewatch_count, times_per_day, output_text):
    for _ in range(times_per_day):
        threading.Thread(target=execute_task, args=(api_key, channel_id, video_count, rewatch_count, output_text)).start()
        time.sleep(24 * 3600)  # Wait until the next day to run again

def create_ui():
    window = tk.Tk()
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.title("YouTube Video Watcher")

    # API Key Entry
    tk.Label(window, text="YouTube API Key:").grid(row=0, column=0, padx=10, pady=10)
    api_key_entry = tk.Entry(window, width=40)
    api_key_entry.grid(row=0, column=1, padx=10, pady=10)
    api_key_entry.insert(0, "AIzaSyD8-I8KqrDwYgW4tcf9B_ys5YZ0rvM3-vU")

    # Channel URL Entry
    tk.Label(window, text="Channel Id:").grid(row=1, column=0, padx=10, pady=10)
    channel_id = tk.Entry(window, width=40)
    channel_id.grid(row=1, column=1, padx=10, pady=10)
    channel_id.insert(0, "UCHQcojfM8lWYx11Jrj3j5-A")

    # Video Count Entry
    tk.Label(window, text="Number of Videos:").grid(row=2, column=0, padx=10, pady=10)
    video_count_entry = tk.Entry(window, width=40)
    video_count_entry.grid(row=2, column=1, padx=10, pady=10)
    video_count_entry.insert(0, "5")

    # Rewatch Count Entry
    tk.Label(window, text="Rewatch Count:").grid(row=3, column=0, padx=10, pady=10)
    rewatch_count_entry = tk.Entry(window, width=40)
    rewatch_count_entry.grid(row=3, column=1, padx=10, pady=10)
    rewatch_count_entry.insert(0, "1")

    # Times Per Day Entry
    tk.Label(window, text="Times Per Day:").grid(row=4, column=0, padx=10, pady=10)
    times_per_day_entry = tk.Entry(window, width=40)
    times_per_day_entry.grid(row=4, column=1, padx=10, pady=10)
    times_per_day_entry.insert(0, "1")

    # Output Area
    output_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20)
    output_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Start Button
    start_button = tk.Button(window, text="Start Watching", 
                             command=lambda: start_task(api_key_entry.get(), channel_id.get(), 
                                                        int(video_count_entry.get()), int(rewatch_count_entry.get()), 
                                                        int(times_per_day_entry.get()), output_text))
    start_button.grid(row=6, column=0, columnspan=2, pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_ui()


    