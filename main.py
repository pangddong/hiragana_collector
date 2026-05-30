import tkinter as tk
import os
from tkinter import simpledialog, messagebox
from PIL import ImageGrab

hiragana_dict = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "wo", "ん": "n"
}
hiragana_list = list(hiragana_dict.keys())
hiragana_roman = list(hiragana_dict.values())
canvas_width, canvas_height = 500, 400 # 캔버스 크기(가로, 세로)
data_limit = 46 # 총 데이터 종류 개수
write_limit = 5 # 데이터 별 목표 반복 횟수
data_index = 0 # 데이터 종류 현재 위치
write_index = 1 # 데이터 별 현재 반복 횟수
last_x, last_y = 0, 0 # 캔버스 그릴때 이전 좌표
username = None

def update_write_index(): # 각 데이터 반복마다 값 업데이트
    global write_index
    if write_index > write_limit: # 데이터 종류마다 완료시
        write_index = 1
        update_data_index()
    hiragana_value = hiragana_list[data_index]
    hiragana_char.set(hiragana_value)
    write_progress_text.set(f"{write_index}/{write_limit}")

def click_complete_button(event=None):
    global write_index
    img_save()
    if data_index >= data_limit - 1 and write_index == write_limit: # 마지막 종류의 마지막 반복까지 하면 끝내기
        complete()
        return
    write_index += 1
    update_write_index()
    canvas_clear()

def update_data_index(): # 총 데이터 값 업데이트
    global data_index
    data_index += 1
    total_progress_text.set(f"{data_index + 1}/{data_limit}")

def draw_canvas(event):
    global last_x, last_y # last 사용 없이 event-1 사용시 고속이동에서 끊김
    if last_x == 0:
        last_x, last_y = event.x, event.y
        return
    canvas.create_line(last_x, last_y, event.x, event.y, fill="black", width=12, capstyle=tk.ROUND, smooth=tk.TRUE)
    last_x, last_y = event.x, event.y

def draw_reset(event): # 초기화 안하면 이전에 놓은 위치에서 쭉 이어짐
    global last_x, last_y
    last_x, last_y = 0, 0

def canvas_clear():
    canvas.delete("all")

def img_save():
    current_char = hiragana_list[data_index] # 히라가나 문자 하나 뽑아 담음
    char_roman = hiragana_dict[current_char] # 뽑은 문자의 로마자를 담음
    file_path = f'{username}_hiragana_data/{char_roman}'
    if not os.path.exists(f'{username}_hiragana_data'):
        os.mkdir(f'{username}_hiragana_data')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    # 하단: 캔버스 전체를 흑백, 가로500, 세로400으로 변환 후 저장
    x1 = canvas.winfo_rootx()
    y1 = canvas.winfo_rooty()
    x2 = x1 + canvas_width
    y2 = y1 + canvas_height
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    gray_img = img.convert("L")
    resize_img = gray_img.resize((500, 400))
    resize_img.save(f"{file_path}/{username}_{char_roman}_{write_index}.png")

def complete():
    main_frame.destroy()
    win.unbind("<Return>")
    complete_text = tk.Label(win, text='Thank you!!', font=('', 70))
    complete_text.pack(fill="both", expand=True)

def start_main():
    global username
    username = simpledialog.askstring("Username", "User Name", parent=win)
    if not username or not username.strip(): # "", None은 False 취급
        return
    show_username.set(f"UserName: {username}")

    start_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)
    total_progress_text.set(f"{data_index + 1}/{data_limit}")
    update_write_index()

def progress_load():
    global data_index
    user_input = simpledialog.askstring("Load", "hiragana in roman", parent=win)
    if user_input is None:
        return
    if user_input in hiragana_roman:
        data_index = hiragana_roman.index(user_input)
        start_main()
    else:
        messagebox.showwarning('error', 'Not Found')

win = tk.Tk()
win.title("hiragana collector")
bg_color = "#e0e0e0"
win.configure(bg=bg_color)
# 하단: 창 중앙정렬
win_width = 600
win_height = 630
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
center_x = int((screen_width - win_width) / 2)
center_y = int((screen_height - win_height) / 2)
win.geometry(f"{win_width}x{win_height}+{center_x}+{center_y}")


hiragana_char = tk.StringVar()
total_progress_text = tk.StringVar()
write_progress_text = tk.StringVar()
show_username = tk.StringVar()

start_frame = tk.Frame(win, bg=bg_color)
start_frame.pack(fill="both", expand=True)
main_frame = tk.Frame(win, bg=bg_color)

# 하단: start_frame 관리
button_container = tk.Frame(start_frame, bg=bg_color) # 버튼 두개 중앙에 모으기 위해 컨테이너 생성
button_container.pack(expand=True)
start_title = tk.Button(button_container, text='START', command=start_main, font=('',30))
start_title.pack(pady=10)
btn_load = tk.Button(button_container, text="LOAD", command=progress_load, font=("", 20))
btn_load.pack(pady=10)

# 하단: main_frame 관리
show_username_lable = tk.Label(main_frame, textvariable=show_username, font=('', 20), bg=bg_color)
show_username_lable.pack()

total_progress_text_label = tk.Label(main_frame, textvariable=total_progress_text, bg=bg_color)
total_progress_text_label.pack()

hiragana_char_lable = tk.Label(main_frame, textvariable=hiragana_char, font=("", 50), bg=bg_color)
hiragana_char_lable.pack()


write_progress_text_lable = tk.Label(main_frame, textvariable=write_progress_text, bg=bg_color)
write_progress_text_lable.pack()

canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_height, bg="#ffffff")
canvas.pack(pady=(0, 10))
canvas.bind("<B1-Motion>", draw_canvas)
canvas.bind("<ButtonRelease-1>", draw_reset)

complete_button = tk.Button(main_frame, text='complete', command=click_complete_button)
complete_button.pack()

clear_button = tk.Button(main_frame, text='clear', command=canvas_clear)
clear_button.pack(pady=(10, 0))

win.bind("<Return>", click_complete_button)
win.mainloop()