import tkinter as tk
from tkinter import messagebox
import requests

class CentralServer:
    def __init__(self, url):
        self.url = url

    def register(self, user_id, password, role):
        """注册新用户"""
        response = requests.post(f"{self.url}/register", json={
            "user_id": user_id,
            "password": password,
            "role": role
        })
        return response.status_code == 200



    def login(self, role, user_id, password):
        """登录验证"""
        response = requests.post(f"{self.url}/login", json={
            "role": role,
            "user_id": user_id,
            "password": password
        })
        if response.status_code == 200:
            return response.json()  # 返回用户角色信息
        return None

    def send_knowledge_point(self, point):
        """发送知识点到服务器"""
        response = requests.post(f"{self.url}/send", json={"knowledge_point": point})
        return response.status_code == 200

    def get_knowledge_points(self):
        """获取知识点"""
        response = requests.get(f"{self.url}/points")
        if response.status_code == 200:
            return response.json().get("points", [])
        return []


class Application:
    def __init__(self, server):
        self.server = server
        self.window = tk.Tk()
        self.window.title("在线学习平台")

        # 注册部分
        self.register_frame = tk.Frame(self.window)
        self.register_frame.pack(pady=10)

        self.role_label = tk.Label(self.register_frame, text="身份(teacher/student):")
        self.role_label.grid(row=0, column=0)
        self.role_entry = tk.Entry(self.register_frame)
        self.role_entry.grid(row=0, column=1)

        self.user_id_label = tk.Label(self.register_frame, text="学号/工号:")
        self.user_id_label.grid(row=1, column=0)
        self.id_entry = tk.Entry(self.register_frame)
        self.id_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.register_frame, text="密码:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.register_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        self.register_button = tk.Button(self.register_frame, text="注册", command=self.register)
        self.register_button.grid(row=3, columnspan=2)

        # 登录部分
        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack(pady=10)

        self.role_label = tk.Label(self.login_frame, text="身份(teacher/student):")
        self.role_label.grid(row=0, column=0)
        self.role_entry = tk.Entry(self.login_frame)
        self.role_entry.grid(row=0, column=1)

        self.login_user_id_label = tk.Label(self.login_frame, text="学号/工号:")
        self.login_user_id_label.grid(row=1, column=0)
        self.login_id_entry = tk.Entry(self.login_frame)
        self.login_id_entry.grid(row=1, column=1)

        self.login_password_label = tk.Label(self.login_frame, text="密码:")
        self.login_password_label.grid(row=2, column=0)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.grid(row=2, column=1)

        # 修改这里：用 lambda 传入参数
        self.login_button = tk.Button(self.login_frame, text="登录", command=self.login)
        self.login_button.grid(row=3, columnspan=2)

        # 知识点部分
        self.knowledge_label = tk.Label(self.window, text="")
        self.knowledge_label.pack()

        self.point_entry = tk.Entry(self.window)
        self.point_entry.pack(pady=5)

        self.send_button = tk.Button(self.window, text="发送知识点", command=self.send_knowledge_point)
        self.send_button.pack()

        self.window.mainloop()

    def register(self):
        role = self.role_entry.get().strip().lower()
        user_id = self.id_entry.get()
        password = self.password_entry.get()

        if self.server.register(user_id, password, role):
            messagebox.showinfo("注册成功", "用户注册成功！")
        else:
            messagebox.showerror("注册失败", "用户注册失败，请重试！")

    def login(self):
        global role
        role = self.role_entry.get()  # 获取身份
        user_id = self.login_id_entry.get()  # 获取用户ID
        password = self.login_password_entry.get()  # 获取密码

        result = self.server.login(role,user_id, password)
        if result is not None:
            messagebox.showinfo("登录成功", f"欢迎，{user_id}！你是：{role}")

            # 根据角色展示相应功能
            if role == 'teacher':
                self.knowledge_label.config(text="作为教师，你可以发送知识点。")
            elif role == 'student':
                self.knowledge_label.config(text="作为学生，你可以查看知识点。")
                self.display_knowledge_points()

        else:
            messagebox.showerror("登录失败", "用户名或密码错误！")

    def send_knowledge_point(self):
        if role == 'teacher':
            point = self.point_entry.get()
            if self.server.send_knowledge_point(point):
                messagebox.showinfo("发送成功", "知识点已发送！")
            else:
                messagebox.showerror("发送失败", "知识点发送失败，请重试！")
        else:
            messagebox.showwarning("权限不足", "只有教师可以发送知识点。")

    def display_knowledge_points(self):
        points = self.server.get_knowledge_points()
        if points:
            self.knowledge_label.config(text="知识点列表：\n" + "\n".join(points))
        else:
            self.knowledge_label.config(text="没有可用的知识点。")


if __name__ == "__main__":
    server_url = "http://110.42.36.128:5000"
    server = CentralServer(server_url)
    app = Application(server)
