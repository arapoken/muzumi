import tkinter as tk
import pyautogui as pt
import random
import os
aaa= os.path.dirname(os.path.abspath(__file__))
print(aaa)
os.chdir(aaa)
retval = os.getcwd()
print ("当前工作目录为 %s" % retval)
flag=1
# 获取主屏幕分辨率
WIDTH, HEIGHT = pt.size()
# 任务栏高度
taskbarHeight = 40
# GIF图片的宽度和高度
imgWidth, imgHeight = 500, 370
# 窗口的初始位置
posX, posY = int(WIDTH / 2 - imgWidth / 2), 0
 
# 创建主窗口
root = tk.Tk()
# 设置窗口大小和位置
root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
root.overrideredirect(1)
# 设置背景颜色为黑色
root.configure(bg='black')
# 设置背景为透明
root.attributes('-transparentcolor', 'black')
# 始终在最上层
root.wm_attributes('-topmost', 1)
 
# 读取图片函数
def load_images(file_path, frame_count):
    images = []
    for i in range(frame_count):
        try:
            img = tk.PhotoImage(file=file_path, format=f'gif -index {i}')
            images.append(img)
        except tk.TclError:
            break
    return images
 
# 读取图片
idleRight = load_images("muzumigif/1.gif", 15)
idleLeft = load_images("muzumigif/2.gif", 15)
runRight = load_images("muzumigif/3.gif", 15)
runLeft = load_images("muzumigif/4.gif", 15)
fall = load_images("muzumigif/5.gif", 15)
del (idleRight[1])
del (runLeft[1:3])
 
# 设置状态字典
status = {
    0: fall,
    1: idleRight,
    2: idleLeft,
    3: runRight,
    4: runLeft
}
# 初始化当前状态
status_num = 0
 
# 创建标签对象
player = tk.Label(root, image=idleLeft[0], bg='black', bd=0)
player.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
 
def changeStatus():  # 改变角色的状态
    global status_num
    status_num = random.randint(1, 4)
    # 每隔随机毫秒数循环一次
    root.after(random.randint(1000, 5000), changeStatus)
 
def falling():  # 掉落状态，应该在其他函数前面调用
    global status_num, posX, posY,flag
    # 如果角色正在掉落，改变状态
    if root.winfo_y() + imgHeight < HEIGHT - taskbarHeight and flag==1:
        status_num = 0
        posY += 1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    # 在地面上
    elif root.winfo_y() + imgHeight == HEIGHT - taskbarHeight and status_num == 0 and flag==1:
        status_num = 0
    elif root.winfo_y() + imgHeight > HEIGHT - taskbarHeight and flag==1:
        status_num = 0
        posY -= 1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    root.after(1, falling)
 
def moving():  # 根据角色的状态移动窗口
    global status_num, posX
    if status_num == 3 and root.winfo_x() + imgWidth < WIDTH:
        posX += 1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    elif status_num == 3 and root.winfo_x() + imgWidth >= WIDTH:
        status_num = 1
 
    if status_num == 4 and root.winfo_x() > 0:
        posX -= 1
        root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")
    elif status_num == 4 and root.winfo_x() <= 0:
        status_num = 2
    root.after(3, moving)
 
def Anim(num, rate):  # 使动画生效
    global player
    if num < len(status[status_num]) - 1:
        num += 1
    else:
        num = 0
    player.config(image=status[status_num][num])
    root.after(rate, lambda: Anim(num, rate))
 
# 鼠标点击事件
def on_click(event):
    global status_num
    status_num = random.randint(1, 4)  # 每次点击时随机改变状态
 
# 鼠标拖动事件
def on_drag(event):
    global status_num
    global posX, posY,flag
    flag=0
    status_num=0
    posX = event.x_root - imgWidth // 2
    posY = event.y_root - imgHeight // 2
    root.geometry(f"{imgWidth}x{imgHeight}+{posX}+{posY}")

def release(event):
    global status_num
    global posX, posY,flag
    flag=1

# 绑定鼠标事件
root.bind("<Button-1>", on_click)
root.bind("<B1-Motion>", on_drag)
root.bind("<ButtonRelease-1>",release)
 
changeStatus()
falling()
moving()
Anim(0, 150)
root.mainloop()