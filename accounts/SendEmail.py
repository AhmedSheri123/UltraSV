import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver, username, Subject, lang, domain, confirm_url):
    sender_email = "sheri.hack.123@gmail.com"
    receiver_email = receiver
    password = "ohklaidwgqdhqhwk"

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    
    message = MIMEMultipart("alternative")
    message["Subject"] = Subject
    message["From"] = sender_email
    message["To"] = receiver_email

    html_content_ar = f"""
    <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:526px; background:none; " id="container_8538c1f">
  <div style="margin: 10px; display: block; " id="container_8538c1f_padding" >
    <div style="text-align:left;">
      <div style="vertical-align: top; border-radius: 10px; position:relative; display: inline-block; width:100%; min-height:273px; background-color:#434FFF; " id="container_26be2b">
        <div style="margin: 10px; display: block; " id="container_26be2b_padding" >
          <div style="text-align:center;">
            <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_e4bf9ac">
              <div style="text-align:left;">
                <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">UltraSV</span>
                </div>
              </div>
            </div>
          <div style="text-align:left;">
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:59px; background:none; " id="container_45c793e9">
              <div style="margin: 10px; display: block; " id="container_45c793e9_padding" >
                <div style="text-align:right;">
                  <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">مرحبا بك يا {username} على موقع خدمات فائقة سوف نقدم لك اغلب الخدمات والادوات المهمة لاستفادة منها او الربح منها  لتأكيد حسابك يرجى الضغط على الزر الموجود في الاسفل</span>
                  </div>
                </div>
              </div>
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:150px; background:none; " id="container_555429bd">
              <div style="margin: 10px; display: block; " id="container_555429bd_padding" >
                <div style="text-align:center;">
                  <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_365f079f">
                    <div style="text-align:left;">
                      <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">لتاكيد حسابك اضغط الزر التالي</span>
                      </div>
                    </div>
                  </div>
                <div style="text-align:left;">
                  <div style="vertical-align: top; position:relative; display: inline-block; margin:20px 0px 0px 0px;width:100%; min-height:83px; background:none; " id="container_2cc87846">
                    <div style="margin: 10px; display: block; " id="container_2cc87846_padding" >
                      <div style="text-align:center;">
                        <a href="https://{domain}/{confirm_url}" style="text-decoration:none"><div style="vertical-align: bottom; border-radius: 5px; position:relative; display: inline-block; width:150px; height:40px; background-color:#FF8080; box-shadow: 7px 7px 10px -5px rgba(0, 0, 0, 0.784314); " id="button_30ba40bc">
                          <div style="display: table; width: 100%; height: 100%;"><div style="display: table-cell; vertical-align: middle;">                            <div style="text-align:center;">
                              <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">تاكيد الحساب</span>
                              </div>
                            <div style="text-align:left;">
                              </div>
                            </div></div>
                          </div></a>
                        </div>
                      <div style="clear:both"></div>
                      </div>
                    </div>
                  </div>
                <div style="clear:both"></div>
                </div>
              </div>
            </div>
          <div style="clear:both"></div>
          </div>
        </div>
      </div>
    <div style="clear:both"></div>
    </div>
  </div>

    
    """





    html_content_en = f"""
     <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:526px; background:none; " id="container_8538c1f">
  <div style="margin: 10px; display: block; " id="container_8538c1f_padding" >
    <div style="text-align:left;">
      <div style="vertical-align: top; border-radius: 10px; position:relative; display: inline-block; width:100%; min-height:273px; background-color:#434FFF; " id="container_26be2b">
        <div style="margin: 10px; display: block; " id="container_26be2b_padding" >
          <div style="text-align:center;">
            <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_e4bf9ac">
              <div style="text-align:left;">
                <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">UltraSV</span>
                </div>
              </div>
            </div>
          <div style="text-align:left;">
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:59px; background:none; " id="container_45c793e9">
              <div style="margin: 10px; display: block; " id="container_45c793e9_padding" >
                <div style="text-align:right;">
                  <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">Welcome, {username}, to the Ultra Services website. We will provide you with most of the important services and tools to benefit from or earn from. To confirm your account, please click on the button below.</span>
                  </div>
                </div>
              </div>
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:150px; background:none; " id="container_555429bd">
              <div style="margin: 10px; display: block; " id="container_555429bd_padding" >
                <div style="text-align:center;">
                  <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_365f079f">
                    <div style="text-align:left;">
                      <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">To verify your account, click the following button</span>
                      </div>
                    </div>
                  </div>
                <div style="text-align:left;">
                  <div style="vertical-align: top; position:relative; display: inline-block; margin:20px 0px 0px 0px;width:100%; min-height:83px; background:none; " id="container_2cc87846">
                    <div style="margin: 10px; display: block; " id="container_2cc87846_padding" >
                      <div style="text-align:center;">
                        <a href="https://{domain}/{confirm_url}" style="text-decoration:none"><div style="vertical-align: bottom; border-radius: 5px; position:relative; display: inline-block; padding: 10px 20px; background-color:#FF8080; box-shadow: 7px 7px 10px -5px rgba(0, 0, 0, 0.784314); " id="button_30ba40bc">
                          <div style="display: table; width: 100%; height: 100%;"><div style="display: table-cell; vertical-align: middle;">                            <div style="text-align:center;">
                              <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">Account Confirmation</span>
                              </div>
                            <div style="text-align:left;">
                              </div>
                            </div></div>
                          </div></a>
                        </div>
                      <div style="clear:both"></div>
                      </div>
                    </div>
                  </div>
                <div style="clear:both"></div>
                </div>
              </div>
            </div>
          <div style="clear:both"></div>
          </div>
        </div>
      </div>
    <div style="clear:both"></div>
    </div>
  </div>
    """



    # Create the plain-text and HTML version of your message
    text = """"""
    html = ''
    if lang == 'ar':
        html = html_content_ar
    else:
        html = html_content_en
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 









def send_email_reset_password(receiver, username, Subject, lang, domain, confirm_url):
    sender_email = "sheri.hack.123@gmail.com"
    receiver_email = receiver
    password = "ohklaidwgqdhqhwk"

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    
    message = MIMEMultipart("alternative")
    message["Subject"] = Subject
    message["From"] = sender_email
    message["To"] = receiver_email

    html_content_ar = f"""
    <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:526px; background:none; " id="container_8538c1f">
  <div style="margin: 10px; display: block; " id="container_8538c1f_padding" >
    <div style="text-align:left;">
      <div style="vertical-align: top; border-radius: 10px; position:relative; display: inline-block; width:100%; min-height:273px; background-color:#434FFF; " id="container_26be2b">
        <div style="margin: 10px; display: block; " id="container_26be2b_padding" >
          <div style="text-align:center;">
            <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_e4bf9ac">
              <div style="text-align:left;">
                <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">UltraSV</span>
                </div>
              </div>
            </div>
          <div style="text-align:left;">
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:59px; background:none; " id="container_45c793e9">
              <div style="margin: 10px; display: block; " id="container_45c793e9_padding" >
                <div style="text-align:right;">
                  <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">مرحبا بك يا {username} على موقع خدمات فائقة سوف نقدم لك اغلب الخدمات والادوات المهمة لاستفادة منها او الربح منها لتغير كلمة مرور حسابك يرجى الضغط على الزر الموجود في الاسفل</span>
                  </div>
                </div>
              </div>
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:150px; background:none; " id="container_555429bd">
              <div style="margin: 10px; display: block; " id="container_555429bd_padding" >
                <div style="text-align:center;">
                  <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_365f079f">
                    <div style="text-align:left;">
                      <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">لتغير كلمة مرور حسابك اضغط الزر التالي</span>
                      </div>
                    </div>
                  </div>
                <div style="text-align:left;">
                  <div style="vertical-align: top; position:relative; display: inline-block; margin:20px 0px 0px 0px;width:100%; min-height:83px; background:none; " id="container_2cc87846">
                    <div style="margin: 10px; display: block; " id="container_2cc87846_padding" >
                      <div style="text-align:center;">
                        <a href="https://{domain}/{confirm_url}" style="text-decoration:none"><div style="vertical-align: bottom; border-radius: 5px; position:relative; display: inline-block; padding: 10px 20px; background-color:#FF8080; box-shadow: 7px 7px 10px -5px rgba(0, 0, 0, 0.784314); " id="button_30ba40bc">
                          <div style="display: table; width: 100%; height: 100%;"><div style="display: table-cell; vertical-align: middle;">                            <div style="text-align:center;">
                              <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">تغير كلمة المرور</span>
                              </div>
                            <div style="text-align:left;">
                              </div>
                            </div></div>
                          </div></a>
                        </div>
                      <div style="clear:both"></div>
                      </div>
                    </div>
                  </div>
                <div style="clear:both"></div>
                </div>
              </div>
            </div>
          <div style="clear:both"></div>
          </div>
        </div>
      </div>
    <div style="clear:both"></div>
    </div>
  </div>

    
    """





    html_content_en = f"""
     <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:526px; background:none; " id="container_8538c1f">
  <div style="margin: 10px; display: block; " id="container_8538c1f_padding" >
    <div style="text-align:left;">
      <div style="vertical-align: top; border-radius: 10px; position:relative; display: inline-block; width:100%; min-height:273px; background-color:#434FFF; " id="container_26be2b">
        <div style="margin: 10px; display: block; " id="container_26be2b_padding" >
          <div style="text-align:center;">
            <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_e4bf9ac">
              <div style="text-align:left;">
                <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">UltraSV</span>
                </div>
              </div>
            </div>
          <div style="text-align:left;">
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:59px; background:none; " id="container_45c793e9">
              <div style="margin: 10px; display: block; " id="container_45c793e9_padding" >
                <div style="text-align:right;">
                  <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">Welcome, {username}, to the Ultra Services website. We will provide you with most of the important services and tools to benefit from or earn from. To reset your account password, please click on the button below.</span>
                  </div>
                </div>
              </div>
            <div style="vertical-align: top; position:relative; display: inline-block; width:100%; min-height:150px; background:none; " id="container_555429bd">
              <div style="margin: 10px; display: block; " id="container_555429bd_padding" >
                <div style="text-align:center;">
                  <div style="vertical-align: bottom; position:relative; display: inline-block; margin:20px 0px 0px 0px;background:none; " id="text_365f079f">
                    <div style="text-align:left;">
                      <span style="font-size:20pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">To reset your account password, click the following button</span>
                      </div>
                    </div>
                  </div>
                <div style="text-align:left;">
                  <div style="vertical-align: top; position:relative; display: inline-block; margin:20px 0px 0px 0px;width:100%; min-height:83px; background:none; " id="container_2cc87846">
                    <div style="margin: 10px; display: block; " id="container_2cc87846_padding" >
                      <div style="text-align:center;">
                        <a href="https://{domain}/{confirm_url}" style="text-decoration:none"><div style="vertical-align: bottom; border-radius: 5px; position:relative; display: inline-block; padding: 10px 20px; background-color:#FF8080; box-shadow: 7px 7px 10px -5px rgba(0, 0, 0, 0.784314); " id="button_30ba40bc">
                          <div style="display: table; width: 100%; height: 100%;"><div style="display: table-cell; vertical-align: middle;">                            <div style="text-align:center;">
                              <span style="font-size:12pt; font-family:Arial, Helvetica, sans-serif; color:#FFFFFF; font-weight:bold; ">Reset Password</span>
                              </div>
                            <div style="text-align:left;">
                              </div>
                            </div></div>
                          </div></a>
                        </div>
                      <div style="clear:both"></div>
                      </div>
                    </div>
                  </div>
                <div style="clear:both"></div>
                </div>
              </div>
            </div>
          <div style="clear:both"></div>
          </div>
        </div>
      </div>
    <div style="clear:both"></div>
    </div>
  </div>
    """



    # Create the plain-text and HTML version of your message
    text = """"""
    html = ''
    if lang == 'ar':
        html = html_content_ar
    else:
        html = html_content_en
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        # TODO: Send email here
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 
