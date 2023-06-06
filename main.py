
from tkinter import *
from PIL import ImageTk, Image
import os
import RPi.GPIO as GPIO
import time
KEY = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY, GPIO.IN)
path = '/home/pi/Documents/Pictures'
allfile = os.listdir(path)
bmpfiles = []
pngimage = []
numpage = [0]
# выбираем все фаилы с расширенем .bmp
for i in range(len(allfile)):  # получили список всех фаилом с .bmp по пути path
    if '.bmp' in allfile[i]:
        bmpfiles.append(allfile[i])
bmpfiles.sort()        
#print(bmpfiles)
# создаем рабочее окно tkinter
root = Tk()
root.overrideredirect(1)
# root.state('zoomed')
# root.wm_attributes("-topmost", 1)
# root.geometry('1280x1024')

# сохраняем картинки для ткинтер
for i in range(len(bmpfiles)):
    image = ImageTk.PhotoImage(Image.open(path + '/' + bmpfiles[i]))
    pngimage.append(image)


# создаем виджет
canvas = Canvas(root, height=1024, width=1280)
canvas.pack()

#устанавливаем стартовую картинку в окне ткинтер
canvas.create_image(0, 0, anchor='nw', image=pngimage[0])
#print(bmpfiles)

def counter_next():
    if numpage[0] >= len(bmpfiles)-1:
        numpage[0] = 0
        return 0
    currentpage = numpage[0] + 1
    numpage[0] = currentpage
    return currentpage
# счетчик  страницы назад
def counter_priv():
    if numpage[0] <= 0:
        numpage[0] = len(bmpfiles) - 1
        return len(bmpfiles)-1
    currentpage = numpage[0] - 1
    numpage[0] = currentpage
    return currentpage

#вывод изображений
def openpage(x):
    canvas.create_image(0, 0, anchor='nw', image=pngimage[x])
    canvas.update()


# функция обработки события кнопки мыши
def b1(event):
    openpage(counter_next())

def b2(event):
    root.destroy()

def b3(event):
    openpage(counter_priv())
def buttonpress(channel): 
    if GPIO.input(KEY) == 1:
        openpage(counter_next())
        print('pressed')
    time.sleep(0.5)

GPIO.add_event_detect(KEY, GPIO.FALLING, callback = buttonpress, bouncetime = 500)

    
root.bind('<Button-1>', b1)
root.bind('<Button-2>', b2)
root.bind('<Button-3>', b3)

root.mainloop()

