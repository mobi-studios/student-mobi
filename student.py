import tkinter as tk
from tkinter import messagebox
import requests
import subprocess
import os
import time


# 服务器地址
SERVER_URL = "http://154.40.47.126:5000"

def kill_edge():
    try:
        # 使用 taskkill 命令终止 msedge.exe 进程
        subprocess.run(["taskkill", "/IM", "msedge.exe", "/F"], check=True)
        messagebox("已成功终止 Microsoft Edge 进程。上课不要走神！")
    except subprocess.CalledProcessError:
        pass

def kill_explorer():
    try:
        # 使用 taskkill 命令终止 explorer.exe 进程
        subprocess.run(["taskkill", "/IM", "explorer.exe", "/F"], check=True)
        messagebox("已成功终止 文件资源管理器 进程。上课不要走神！")
    except subprocess.CalledProcessError:
        pass

def start_all():
    try:
        subprocess.run(["explorer.exe"])
    except subprocess.CalledProcessError():
        messagebox("请启动win+r，输入explorer，确定才能正常启动任何选项！")


def send_knowledge():
    # 发送知识点，由教师发送
    try:
        response = requests.get(f"{SERVER_URL}/knowledge")
        if response.status_code == 200:
            knowledge = response.json  # 假设服务器返回知识点文本
            messagebox.showinfo("知识点", knowledge)
        else:
            messagebox.showerror("错误", "无法获取知识点，请稍后再试。")
    except Exception as e:
        messagebox.showerror("错误", f"请求失败: {e}")

def lock_features():
    try:
        response = requests.post(f"{SERVER_URL}/lock")
        if response.status_code == 200 and response.json().get('status') == 'locked':
            messagebox.showwarning("警告", "已锁定所有功能，请专心上课！")
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            if "msedge.exe" in result.stdout:
                kill_edge()
            if "explorer.exe" in result.stdout:
                kill_explorer()
        else:
            pass
    except ConnectionError as e:
        messagebox("你TM联网了吗？快检查下！")

def unlock_features():
    try:
        response = requests.post(f"{SERVER_URL}/unlock")
        if response.status_code == 200 and response.json().get('status') == 'unlocked':
            messagebox.showinfo("提示", "下课了，可以使用其他功能。")
            start_all()

        else:
            messagebox.showinfo("提示", "功能仍处于锁定状态。")
    except Exception as e:
        messagebox.showerror("错误", f"请求失败: {e}")

def start_main_app():
    # 创建主应用界面
    main_app = tk.Tk()
    main_app.title("学习助手")
    main_app.geometry("1920x1080")
    main_app.configure(bg='blue')

    title_label = tk.Label(main_app, text="欢迎来到学习助手", font=("Arial", 16), bg='blue')
    title_label.pack(pady=20)

    lock_button = tk.Button(main_app, text="刷新上课模式", command=lock_features)
    lock_button.pack(pady=10)

    unlock_button = tk.Button(main_app, text="刷新下课模式", command=unlock_features)
    unlock_button.pack(pady=10)

    send_button = tk.Button(main_app, text="获取知识点", command=send_knowledge)
    send_button.pack(pady=10)

    main_app.mainloop()
    while True:
        lock_features()
        unlock_features()

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    root.title("学生端，抱歉，登陆损坏，你可以关闭这个窗口")
    root.geometry("100x400")
    start_main_app()  # 显示登录窗口
    root.mainloop()
