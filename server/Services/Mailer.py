"""
Created on Mar 16, 2016

@author: PDINDA
"""
from datetime import datetime
import logging
import os
import socket
import traceback

from autologging import logged
from flask import Flask, render_template
from flask_mail import Mail, Message

from DBUtil import Emails, EmailTemplate, Config,SystemDetails
from settings import current_path,mongodb


@logged(logging.getLogger("Mailer"))
class Mailer(object):

    def str_to_bool(self, s):
        """# Converter Function"""
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False

    def __init__(self, db=None):
        # init db conneciton
        if db is None:
            self.db = mongodb

        """# Init's Data"""
        self.app = Flask(__name__)
        self.mail = Mail(self.app)

        self.app.config.from_object(__name__)
        self.app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
        ###############
        # Collection
        ##############
        self.templatedb = EmailTemplate.EmailTemplate(self.db)
        self.emaildb = Emails.Emails(self.db)
        self.configdb = Config.Config(self.db)
        self.SystemDetailsDb = SystemDetails.SystemDetails(self.db)
        # Initialize Email Configuration
        self.result = self.configdb.getConfigByName("Mailer")  # 1 is for mailer configuration
        if self.result is None:
            raise Exception("Config not found for Mailer")
        self.app.config.update(
            DEBUG=self.str_to_bool(str(self.result['debug']).strip()),
            MAIL_HOST=str(self.result['host']).strip(),
            MAIL_SERVER=str(self.result['server']).strip(),
            MAIL_PORT=int(str(self.result['port']).strip()),
            MAIL_USE_TLS=self.str_to_bool(str(self.result['tls']).strip()),
            MAIL_USE_SSL=self.str_to_bool(str(self.result['ssl']).strip()),
            MAIL_USERNAME=str(self.result['username']).strip(),
            MAIL_PASSWORD=str(self.result['password']).strip(),
            DEFAULT_MAIL_SENDER=str(self.result['defaultsender']).strip()
        )
        # Setup socket Info
        socket.getaddrinfo(str(self.result['socketip']).strip(), str(
            self.result['socketport']).strip())
        # Env Variable
        self.mailfrom = str(self.result['defaultsender']).strip()

    def send_plain_notification(self, to, bcc, cc, subject, body):
        """
        # Returns 404 when not found occurs
        # Returns 200 on success"""
        templateid = None  # Plain messages do not have a template
        if (to and subject and body) in [None, "None", ""]:
            print "Mandatory fields : to,subject,body is missing"
            return "Mandatory fields : to,subject,body is missing"
        # save email in db
        return self.save_email_to_db(to, bcc, cc, subject, body, templateid, 'plain')

    # data is a json  of  params in template
    # Example of JSON:
    #    Input :
    #         {
    #         "name":"Pradeep",
    #         "name1":"Piyush"
    #        }
    #     For :#
    #     <p>Dear {{ data.name }},</p>
    #
    # <p> Your password has been reset. {{ data.name1 }} knows it.</p>
    # <p>Regards,</p>
    # <p>The <code>System</code> Team</p>
    # Returns 404 when not found occurs
    # Returns 200 on success
    def send_html_notification(self, to, bcc, cc, templateid, data):
        """ convert data to html mail template using render template
         and save it to database
        """
        if (to and templateid and data) in [None, "None", ""]:
            print "Mandatory fields : to,template,data is missing"
            return "Mandatory fields : to,template,data is missing"
        # Get Template from Db
        result = self.templatedb.GetTemplateByTemplateId(templateid)
        if result is None:
            print "Email Template id : " + str(templateid) + " was not found."
            return "Email Template id : " + str(templateid) + " was not found."
        subject = result["subject"]
        htmlFileName = result["html"]
        sys_det=self.SystemDetailsDb.get_system_details_single()
        dpm_url = "https://"+ sys_det.get("hostname") + ":" + sys_det.get("port") + "/"
        footer_data = {"url": dpm_url, "account_name" : sys_det.get("account_name"), "host_name" : sys_det.get("hostname")}
        with self.app.app_context():
            header = render_template("header.html",
                                        data=data)
            footer = render_template('footer.html',
                                        data=footer_data)
            body = render_template(htmlFileName,
                                        data=data)
            emaildata= header+body+footer
            # save email in db # passing to as string
            return self.save_email_to_db(to, bcc, cc, subject, emaildata, templateid, 'html')

    def save_email_to_db(self, to, bcc, cc, subject, msg, templateid, msgtype):
        """
        # Saves email to db
        # Return 404 when error occurs while saving to db
        # Returns 200 when success
        # Returns 500 on unexpected exception"""
        try:
            data = {'to': to, 'cc': cc, 'bcc': bcc, 'subject': subject, 'msg': msg,
                    'msgtype': msgtype, 'status': 'New',
                    'retrycount': 0, 'templateid': templateid, 'credt': datetime.now(),
                    'upddt': datetime.now()}
            result = self.emaildb.AddEmail(data)
            if result is None:
                print "Failed to save email" + str(result)
                return "Failed to save email", 404
            else:
                print "Email saved in db with _id " + str(result)
                return "Email saved in db with _id " + str(result), 200
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            print "Failed to save email" + str(e), 500

    def send_email(self, to, cc, bcc, subject, emaildata, emailtype):
        """
         # Sends the email
        # Returns 404 when invalid email type,mandatory not found
        # Returns 200 on success
        # Returns 500 on unexpected exception
        ######################################################################
        # THIS METHOD SHOULD ONLY BE CALLED FROM handle_pending_notification(id)
        ######################################################################"""
        if (to and subject and emaildata and emailtype) in [None, "None", ""]:
            return Exception("Mandatory fields : to,subject,emaildata,emailtype is missing")
        try:
            msg = Message(subject, sender=self.mailfrom, recipients=to)
            if cc is not None:
                msg.cc = cc
            if bcc is not None:
                msg.bcc = bcc
            if emailtype.lower() in ['html']:
                msg.html = emaildata
            elif emailtype.lower() in ['plain']:
                msg.body = emaildata
            else:
                return Exception("Invalid email type detected. Found :" + emailtype)

            # ATACH LOGO FILE
            static = os.path.join(os.path.dirname(current_path),"client","static")
            assets = os.path.join(static, "assets")
            images = os.path.join(assets, "images")
            icons = os.path.join(images, "icons")
            imageFile = os.path.join(icons, "dm_logo.png")

            if os.path.isfile(imageFile):
                with self.app.open_resource(imageFile) as fp:
                    msg.attach(os.path.basename(imageFile),
                               "image/png", fp.read())

            # SEND EMAIL
            with self.app.app_context():
                self.mail.send(msg)
                print "Email was successfully send"
                return "Email was successfully send", 200
        except Exception as e:  # catch *all* exceptions
            print "Unable to send email.Reason :" + str(e)
            return Exception("Unable to send email.Reason :" + str(e)), 404

    def handle_pending_notification(self, id):
        """
         # Check pending email's in db and retry sending them
        # Returns 200 when record handled
        # Returns 404 not found
        # Return 500 when error occurs while sending email"""
        try:
            result = self.emaildb.GetEmailById(id)
            cclist = None
            bcclist = None
            if result is None:  # No pending email's found
                print "Email with _id" + str(id) + " was not found."
                return "Email with _id" + str(id) + " was not found."
            if result['status'] in ['Successful']:  # No pending email's found
                print "Email with id :" + str(id) + " is already sent."
                return "Email with id :" + str(id) + " is already sent."
            tolist = result['to'].encode('utf-8').split(',')
            cc = result['cc']
            if cc is not None:
                cclist = cc.encode('utf-8').split(',')
            bcc = result['bcc']
            if bcc is not None:
                bcclist = bcc.encode('utf-8').split(',')
            response = self.send_email(tolist, cclist, bcclist, result['subject'].encode(
                'utf-8'), result['msg'].encode('utf-8'), result['msgtype'].encode('utf-8'))
            if response[1] in [200]:
                self.emaildb.UpdateEmailStatus(result['_id'], 'Successful')
                return "Email was successfully send with _id" + str(result['_id'])
            else:
                raise Exception(response[0])
        except Exception as e:  # catch *all* exceptions
            count = result['retrycount'] + 1
            if count in [4]:
                self.emaildb.UpdateEmailStatus(result['_id'], 'Failed', str(e))
            else:
                self.emaildb.UpdateEmailStatus(
                    result['_id'], 'Pending', str(e))
                self.emaildb.UpdateRetryCount(
                    result['_id'], result['retrycount'] + 1)
            return str(e)
