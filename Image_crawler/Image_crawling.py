from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

root = Tk()
root.title("Image Crawler")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')


def check():
    global search_text
    global combo_number
    global save_path
    
    search_text = ent_search_bar.get()
    combo_number = combobox.get()
    combo_number_nospace = ''.join(combo_number.split()) # 공백을 없애주는 작업 / isalpha()는 공백 있으면 False 값
    save_path = ent_dest_path.get()

    if search_text == "":
        msgbox.showwarning("Warning", "There is not any text in the search bar")
    elif combo_number == "" or combo_number_nospace.isalpha() == True:
        msgbox.showwarning("Warning", "Please, set the number of pictures")
    elif save_path == "":
        msgbox.showwarning("Warning", "The save path is empty")
    else:
        start_crawling()

# 저장경로 찾는 함수(폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "":
        return
    ent_dest_path.delete(0, END)
    ent_dest_path.insert(0, folder_selected)

# 이미지를 다운후 다운 받은 폴더 열기
def openFolder():
    global save_path
    path = os.path.realpath(save_path)
    os.startfile(path)

# 이미지 크롤링 함수
def start_crawling():
    global search_text
    global combo_number
    global save_path
    
    btn_start.config(state="disabled")

    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=ri&authuser=0& ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(search_text)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.    scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.   scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height

    p_var.set(10)
    progressbar.update()
    # lbl_percent.config(text="10%")

    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    count = 1
    picNums = int(combo_number)

    for idx, image in enumerate(images):
            try:
                if count <= picNums: 
                    image.click()
                    time.sleep(2)
                    imgURL = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
                    urllib.request.urlretrieve(imgURL, save_path + "/" + str(count) + ".jpg")
                    
                    progress = (idx + 1) / picNums * 90
                    p_var.set(progress)
                    progressbar.update()
                    # lbl_percent.config(text=str(progress) + "%")
                    count += 1
                else:
                    break
            except:
                continue


    driver.close()
    ent_search_bar.delete(0, END)
    combobox.set("Type or Select number")
    ent_dest_path.delete(0, END)
    p_var.set(0)
    progressbar.update()
    btn_start.config(state="normal")
    openFolder()

# 검색창과 사진수 선택창 묶는 프레임
search_combo_frame = Frame(root)
search_combo_frame.pack()

# 검색창 프레임
lbl_frame_for_search_bar = LabelFrame(search_combo_frame, text="Search Bar")
lbl_frame_for_search_bar.pack(side="left", padx=5, pady=5)

# 검색창
ent_search_bar = Entry(lbl_frame_for_search_bar, width=50)
ent_search_bar.pack(ipady=4, padx=5, pady=5)

# 사진수 선택창 프레임
lbl_frame_for_numPics = LabelFrame(search_combo_frame, text="Number of Pictures")
lbl_frame_for_numPics.pack(side="right", padx=5, pady=5)

# 사진수 선택창
picNums = [50*i for i in range(1, 11)] # 선택창에 넣을 숫자들
combobox = ttk.Combobox(lbl_frame_for_numPics, height=10, values=picNums)
combobox.pack(ipady=4, padx=5, pady=5)
combobox.set("Type or Select number") # 선택창에 뜨는 문구

# 저장경로 프레임
lbl_frame_save = LabelFrame(root, text="Save path")
lbl_frame_save.pack(fill="x")

# 저장경로 뜨는 텍스트 박스
ent_dest_path = Entry(lbl_frame_save)
ent_dest_path.pack(side="left", fill="x", expand=True, ipady=4, padx=5, pady=5)

# 저장경로 찾는 버튼
btn_dest_path = Button(lbl_frame_save, text="Search", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 프로그레스바 프레임
lbl_frame_probar = LabelFrame(root, text="Progress")
lbl_frame_probar.pack(fill="x", padx=5, pady=5)

# 프로그레스바
p_var = DoubleVar()
progressbar = ttk.Progressbar(lbl_frame_probar, maximum=100, variable=p_var, mode="determinate")
progressbar.pack( fill="x", padx=5, pady=5)

# lbl_percent = Label(lbl_frame_probar, text="진행상태")
# lbl_percent.pack(side="right")

#버튼 프레임
# btn_frame = Frame(root)
# btn_frame.pack(side="right")

# 시작 버튼
btn_start = Button(root, text="Start", width=10, command=check)
btn_start.pack(side="right", padx=5, pady=5)


root.mainloop()
