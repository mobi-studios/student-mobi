import tkinter as tk
from tkinter import messagebox
import requests

class CentralServer:
    def __init__(self, base_url):
        self.base_url = base_url

    def register(self, identity, id_number, password):
        response = requests.post(f"{self.base_url}/register", json={
            "role": identity,
            "id_number": id_number,
            "password": password
        })
        return response.json()

    def login(self, identity, id_number, password):
        response = requests.post(f"{self.base_url}/login", json={
            "role": identity,
            "id_number": id_number,
            "password": password
        })
        return response.json()

    def send_knowledge_point(self, title, content, user_id):
        response = requests.post(f"{self.base_url}/send_knowledge_point", json={
            "title": title,
            "content": content,
            "user_id": user_id
        })
        return response.json()

    def get_knowledge_points(self):
        response = requests.get(f"{self.base_url}/get_knowledge_points")
        return response.json()


class Application(tk.Tk):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.title("在线学习平台")
        self.geometry("400x300")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.role_label = tk.Label(self, text="身份 (teacher/student):")
        self.role_label.pack()
        self.role_entry = tk.Entry(self)
        self.role_entry.pack()

        self.id_label = tk.Label(self, text="学号/工号:")
        self.id_label.pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        self.password_label = tk.Label(self, text="密码:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="登录", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self, text="注册", command=self.register)
        self.register_button.pack()
        
        self.message_label = tk.Label(self, text="")
        self.message_label.pack()

    def clear_fields(self):
        self.role_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def login(self):
        role = self.role_entry.get().strip().lower()
        id_number = self.id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not role or not id_number or not password:
            messagebox.showerror("错误", "所有字段都是必填的！")
            return

        response = self.server.login(role, id_number, password)
        if response.get("status") == "success":
            self.clear_fields()
            messagebox.showinfo("成功", "登录成功!")
            # 在这里添加进一步逻辑，例如显示知识点或发送知识点
        else:
            messagebox.showerror("错误", response.get("message", "登录失败！"))

    def register(self):
        role = self.role_entry.get().strip().lower()
        id_number = self.id_entry.get().strip()
        password = self.password_entry.get().strip()

        if not role or not id_number or not password:
            messagebox.showerror("错误", "所有字段都是必填的！")
            return

        response = self.server.register(role, id_number, password)
        if response.get("status") == "success":
            self.clear_fields()
            messagebox.showinfo("成功", "注册成功，请登录！")
        else:
            messagebox.showerror("错误", response.get("message", "注册失败！"))


if __name__ == "__main__":
    server = CentralServer("http://110.42.36.128:5000")  # 替换为你的服务器地址
    app = Application(server)
    app.mainloop()
