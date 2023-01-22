from flask import Flask, request, render_template
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



app = Flask(__name__)

@app.route('/')
def upload_file():
   return render_template('index.html')

@app.route('/run_program', methods = ['GET', 'POST'])
def run_program():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
      string1 = request.form['string1']
      string2 = request.form['string2']
      string3 = request.form['string3']

      os.system("python3 ho\ ja\ yaar/WebApp/topsis.py" + f.filename + " " + string1 + " " + string2 + " " + string3)
      # Email credentials
      username = "auviya023@gmail.com"
      password = "hndwjgmirxqqeudu"

      # Recipient and sender email addresses
      to_email = string3
      from_email = username

      # File attachment
      file_path = 'ho ja yaar/WebApp/result.csv'
      file_name = 'result.csv'

      # Email subject and message
      subject = 'Here are your Results!'
      message = 'Thank you for using our webapp'

      msg = MIMEMultipart()
      msg['From'] = from_email
      msg['To'] = to_email
      msg['Subject'] = subject
      msg.attach(MIMEText(message))

      part = MIMEBase('application', "octet-stream")
      part.set_payload(open(file_path, "rb").read())
      encoders.encode_base64(part)
      part.add_header('Content-Disposition', 'attachment', filename=file_name) 
      msg.attach(part)

      # Send the email
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(username, password)
      server.sendmail(from_email, to_email, msg.as_string())
      server.quit()

      print("Email sent successfully!")
      return "Program run successfully"

if __name__ == '__main__':
   app.run(debug = True)
