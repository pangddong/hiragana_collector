import tkinter as tk
import os
from tkinter import simpledialog, messagebox
from PIL import ImageGrab

hangul_dict = {
    "ㄱ": "g",
    "ㄴ": "n",
    "ㄷ": "d",
    "ㄹ": "r",
    "ㅁ": "m",
    "ㅂ": "b",
    "ㅅ": "s",
    "ㅇ": "ng",
    "ㅈ": "j",
    "ㅊ": "ch",
    "ㅋ": "k",
    "ㅌ": "t",
    "ㅍ": "p",
    "ㅎ": "h"
}
hangul_list = list(hangul_dict.keys())
hangul_roman = list(hangul_dict.values())
canvas_width, canvas_height = 500, 400 # 캔버스 크기(가로, 세로)
data_limit = 14 # 총 데이터 종류 개수
write_limit = 10 # 데이터 별 목표 반복 횟수
data_index = 0 # 데이터 종류 현재 위치
write_index = 1 # 데이터 별 현재 반복 횟수
last_x, last_y = 0, 0 # 캔버스 그릴때 이전 좌표
username = None
undo_stack = []
current_storke = []

def update_write_index(): # 각 데이터 반복마다 값 업데이트
    global write_index
    if write_index > write_limit: # 데이터 종류마다 완료시
        write_index = 1
        update_data_index()
    hangul_value = hangul_list[data_index]
    hangul_char.set(hangul_value)
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
    line_id = canvas.create_line(last_x, last_y, event.x, event.y, fill="black", width=12, capstyle=tk.ROUND, smooth=tk.TRUE)
    current_storke.append(line_id)
    last_x, last_y = event.x, event.y

def draw_reset(event): # 초기화 안하면 이전에 놓은 위치에서 쭉 이어짐
    global last_x, last_y, current_storke, undo_stack
    last_x, last_y = 0, 0
    if current_storke:
        undo_stack.append(current_storke)
        current_storke = []

def undo(event=None):
    global undo_stack
    if undo_stack:
        last_stroke = undo_stack.pop()
    for line_id in last_stroke:
        canvas.delete(line_id)

def canvas_clear(event=None):
    global undo_stack, current_storke
    canvas.delete("all")
    undo_stack = []
    current_storke = []

def img_save():
    current_char = hangul_list[data_index] # 히라가나 문자 하나 뽑아 담음
    char_roman = hangul_dict[current_char] # 뽑은 문자의 로마자를 담음
    file_path = f'{username}_hangul_data/{char_roman}'
    if not os.path.exists(f'{username}_hangul_data'):
        os.mkdir(f'{username}_hangul_data')
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
    username_error_none.pack_forget()
    username_error_roman.pack_forget()
    if not username or not username.strip(): # "", None은 False 취급
        username_error_none.pack()
        return
    if not (username.isalnum() and username.isascii()):
        username_error_roman.pack()
        return
    show_username.set(f"UserName: {username}")

    start_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)
    total_progress_text.set(f"{data_index + 1}/{data_limit}")
    update_write_index()

def progress_load():
    global data_index
    user_input = simpledialog.askstring("Load", "hangul in roman", parent=win)
    if user_input is None:
        return
    if user_input in hangul_roman:
        data_index = hangul_roman.index(user_input)
        start_main()
    else:
        messagebox.showwarning('error', 'Not Found')

win = tk.Tk()
win.title("hangul collector")
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

hangul_char = tk.StringVar()
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
username_error_none = tk.Label(start_frame, text="Enter name", font=('', 30), fg="#ff0000", bg=bg_color)
username_error_roman = tk.Label(start_frame, text="English and numbers", font=('', 30), fg="#ff0000", bg=bg_color)

# 하단: main_frame 관리
show_username_lable = tk.Label(main_frame, textvariable=show_username, font=('', 20), bg=bg_color)
show_username_lable.pack()

total_progress_text_label = tk.Label(main_frame, textvariable=total_progress_text, bg=bg_color)
total_progress_text_label.pack()

hangul_char_lable = tk.Label(main_frame, textvariable=hangul_char, font=("", 50), bg=bg_color)
hangul_char_lable.pack()


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

win.bind("<Escape>", canvas_clear)
win.bind("<Return>", click_complete_button)
win.bind("<space>", click_complete_button)
win.bind("<Control-z>", undo)
win.bind("<Control-Z>", undo)
win.mainloop()