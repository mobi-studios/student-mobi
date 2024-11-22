import requests

class TeacherClient:
    def __init__(self, server_ip):
        self.server_url = f"http://{server_ip}:5000"

    def notify_class_start(self):
        payload = {'action': 'start'}
        response = requests.post(f"{self.server_url}/teacher/notify", json=payload)
        if response.status_code == 200:
            print("课堂开始通知成功")
        else:
            print("课堂开始通知失败:", response.json().get('message'))

    def notify_class_end(self):
        payload = {'action': 'stop'}
        response = requests.post(f"{self.server_url}/teacher/notify", json=payload)
        if response.status_code == 200:
            print("课堂结束通知成功")
        else:
            print("课堂结束通知失败:", response.json().get('message'))

    def send_topic(self, topic):
        payload = {'content': topic}
        response = requests.post(f"{self.server_url}/teacher/knowledge", json=payload)
        if response.status_code == 201:
            print("知识点发送成功")
        else:
            print("知识点发送失败:", response.json().get('message'))


if __name__ == "__main__":
    teacher_client = TeacherClient("154.40.47.126")

    while True:
        action = input("请选择操作 (s: 上课, e: 下课, t: 发送知识点, q: 退出): ").strip().lower()
        if action == 's':
            teacher_client.notify_class_start()
        elif action == 'e':
            teacher_client.notify_class_end()
        elif action == 't':
            topic = input("请输入知识点: ")
            teacher_client.send_topic(topic)
        elif action == 'q':
            break
        else:
            print("无效的操作")
