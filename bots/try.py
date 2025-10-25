import webbrowser
import pyautogui
import time
import random

def manual_control():
    # Open Chrome manually
    url = 'https://pixelscan.net/bot-check'
    url = "https://www.browserscan.net/browser-checker"

    # webbrowser.open('https://pixelscan.net/bot-check')
    webbrowser.open(url)
    time.sleep(5)
    
    # Simulate human behavior
    for _ in range(10):
        x = random.randint(100, 1800)
        y = random.randint(100, 900)
        pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2))
        time.sleep(random.uniform(0.5, 2))

manual_control()