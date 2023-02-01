from asyncio.windows_events import NULL
from pickle import LIST, TRUE
import smtplib
import os
import mimetypes
import openpyxl
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import time
import xlsxwriter

global start_time
start_time = time.time()

def form_the_list(filename):
    global book
    book = openpyxl.open(filename)

    global sheet
    sheet = book.active
    row = 1
    
    global spisok 
    spisok = []
    
    global endf
    endf = sheet.max_row
    print(endf)
    
    while row <= endf:
        spisok.append(sheet[row][0].value)
        row = row + 1
    
    print(spisok)


def send_email(text=None, template=None):
    sender = "user"
    password = "passwords"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    spisok_local = spisok
    i = 0
    server.login(sender, password)

    try:
        with open(template, encoding='utf-8') as file:
            template = file.read()
    except IOError:
            template = None

    try:
        with open(text) as file:
            text = file.read()
    except IOError:
            text = None

    while i < endf:
        reciever = spisok_local[i]
        worksheet_done.write(i, 0, reciever)
        worksheet_done.write(i, 1, "done")
 
        i = i + 1
        print("Send to", reciever, i)
       

        try: 
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = reciever
            msg["Subject"] = "Тема сообщения"

            if text:
                msg.attach(MIMEText(text))

            if template:
                msg.attach(MIMEText(template, "html"))

            print("Collecting attachments")
            for file in tqdm(os.listdir("attachments")):
                filename = os.path.basename(file)
                ftype, encoding = mimetypes.guess_type(file)
                file_type, subtype = ftype.split("/")
            
                if file_type == "text":
                    with open(f"attachments/{file}") as f:
                        file = MIMEText(f.read())
                elif file_type == "image":
                    with open(f"attachments/{file}", "rb") as f:
                        file = MIMEImage(f.read(), subtype)
                elif file_type == "audio":
                    with open(f"attachments/{file}", "rb") as f:
                        file = MIMEAudio(f.read(), subtype)
                elif file_type == "application":
                    with open(f"attachments/{file}", "rb") as f:
                        file = MIMEApplication(f.read(), subtype)
                else:
                    with open(f"attachments/{file}", "rb") as f:
                        file = MIMEBase(file_type, subtype)
                        file.set_payload(f.read())
                        encoders.encode_base64(file)

      

                file.add_header('content-disposition', 'attachment', filename=filename)
                msg.attach(file)

            print("\nSending...")
            server.sendmail(sender, reciever, msg.as_string())
            print("Successfully! The message was sent to", reciever)
            print(time.time() - start_time, "\n")
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password"

def main(text, template, adresses):
    global workbook_done
    global worksheet_done
    workbook_done  = xlsxwriter.Workbook('mails_done.xlsx')
    worksheet_done = workbook_done.add_worksheet()

    form_the_list(addresses)
    continue_q = input("Would you like to continue\n yes/no\n")
    if continue_q == "yes":
        print(send_email(text=text, template=template))
        workbook_done.close()
    else:
        print("exit")
        return NULL

   
if __name__ == "__main__":
    main()
