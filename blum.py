from pyautogui import *
import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import threading

mouse = Controller()
time.sleep(0.5)

new_object_range = ((200, 100, 100), (255, 150, 150))

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

def print_welcome():
        print("""
    ██████╗ ██╗     ██╗   ██╗███╗   ███╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
    ██╔══██╗██║     ██║   ██║████╗ ████║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
    ██████╔╝██║     ██║   ██║██╔████╔██║    ███████║███████║██║     █████╔╝ 
    ██╔══██╗██║     ██║   ██║██║╚██╔╝██║    ██╔══██║██╔══██║██║     ██╔═██╗ 
    ██████╔╝███████╗╚██████╔╝██║ ╚═╝ ██║    ██║  ██║██║  ██║╚██████╗██║  ██╗
    ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                                                
    [!]  -  Blum Auto Clicker V 2.0
    [!]  -  Only Support Telegram Desktop ! ( Hanya Support Telegram Desktop )
    [!]  -  Open Blum Before Start Program ! ( Buka Blum Terlebih Dahulu )
    
    [!]  -  Author : Emrido
    
    """)

def print_pause_message(paused):
        if paused:
            print('    [-] | Program Paused, press "enter" to continue.')
        else:
            print('    [+] | Resuming work.')

def print_not_found_message(window_name):
        print(f"    [-] | Window - {window_name} not found ! Please open Blum")

def print_found_message(window_name):
        print(f"    [+] | Window found - {window_name}\n    [+] | Press 'enter' to pause program.")

def print_stop_message():
        print('    [!] | Program stopped.')

print_welcome()

window_name = input('\n    [!]  -  Press 1 to select the window : ')

if window_name == '1':
    window_name = "TelegramDesktop"

check = gw.getWindowsWithTitle(window_name)
if not check:
    print_not_found_message(window_name)
else:
    print_found_message(window_name)

telegram_window = check[0]
paused = False

green_bacteria_range = ((102, 200, 0), (220, 255, 125))
bomb_range = ((50, 50, 50), (200, 200, 200))

def search_and_click_new_object():
    while True:
        time.sleep(4)  

        scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))
        width, height = scrn.size

        for x in range(0, width, 20):
            for y in range(0, height, 20):
                r, g, b = scrn.getpixel((x, y))

                if (new_object_range[0][0] <= r <= new_object_range[1][0]) and \
                    (new_object_range[0][1] <= g <= new_object_range[1][1]) and \
                    (new_object_range[0][2] <= b <= new_object_range[1][2]):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x, screen_y)
                    break

threading.Thread(target=search_and_click_new_object, daemon=True).start()

while True:
    if keyboard.is_pressed('enter'):
        paused = not paused
        print_pause_message(paused)
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False
    if pixel_found == True:
        break

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))

            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y

                is_bomb = False
                try:
                    for bx in range(-5, 6):
                        for by in range(-5, 6):
                            br, bg, bb = scrn.getpixel((x + bx, y + by))
                            if bomb_range[0][0] <= br <= bomb_range[1][0] and bomb_range[0][1] <= bg <= bomb_range[1][1] and bomb_range[0][2] <= bb <= bomb_range[1][2]:
                                is_bomb = True
                                break
                        if is_bomb:
                            break
                except:
                    continue

                if not is_bomb:
                    click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    pixel_found = True
                    break

print_stop_message()
