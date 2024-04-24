import requests
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 定义发送邮件的函数
def send_email(file_path,password,from_email,to_email):

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "恭喜！2024MCM结果已出!"

    # 添加附件
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_path}",
    )

    msg.attach(part)

    # 发送邮件
    server = smtplib.SMTP_SSL('smtp.163.com', 465)  # 设置SMTP服务器地址和端口
    server.login(from_email, password)  # 使用你的邮箱地址和密码登录
    print("login susses!")
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# 请求网站并下载PDF文件
def download_pdf(url,password,from_email,to_email):
    response = requests.get(url)
    if response.status_code == 200:  # 检查状态码是否为200（表示成功）
        with open("result.pdf", "wb") as f:
            f.write(response.content)
        send_email("result.pdf",password)
        print("邮件发送成功！")
    else:
        print("PDF文件未找到或无法访问！")

# 主函数
def main():
    password = os.environ["PASSWORD"]
    url = os.environ["URL"]
    from_email = os.environ["FROMEMAIL"]  # 发送邮件的邮箱地址
    to_email = os.environ["TOEMAIL"]  # 接收邮件的邮箱地址

    download_pdf(url,password,from_email,to_email)

if __name__ == "__main__":
    main()
