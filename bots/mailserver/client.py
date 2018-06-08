
# encoding: utf-8

import sys
import shelve
import getpass
import string
import os
import email
import smtplib
import poplib
from email import parser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders


from re import *


pat = compile('([A-Z]*[a-z]*[0-9]*)+@([A-Z]*[a-z]*[0-9]*)+.([A-Z]*[a-z]*[0-9]*)')


def isGoodEmail(addr):
    return pat.search(addr)


def getUser():
    return settings.MAIL_SERVER.replace('mail', 'default')


def getPassword(user):
    return settings.MY_PD


def connect(uid, pwd):
    print 'Connecting...'
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(userid)
    pop_conn.pass_(password)
    print pop_conn.getwelcome()
    return pop_conn


def attach(files):
    path = ask('Please specify file location:')
    files.append(path)
    more = ask('More attachments?(Y/N)')
    if more == 'Y' or more == 'y':
        attach(files)


def extractMessageBody(msg):
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            return part.get_payload()


def getThisMailAction(messages, num):
    print '[OPTIONS: reply, quit...]\n'
    global userid, password
    msg = messages[num]
    action = ask('command: ')
    if action == 'reply':
        composeMail(userid, password, 1, msg)
        getInsideAction(messages)
    elif action == 'quit':
        getInsideAction(messages)
    elif action == 'help':
        print '[reply] reply this email \n [quit] quit reading this email\n'
        getThisMailAction(messages, num)
    else:
        print 'invalid command'
        getThisMailAction(messages, num)


n = 0


def getNum():
    global n
    n = n+1
    return n


def chkAttach(messages, num):  # save attachments
    # only PDF files are checked
    msg = messages[num]
    attached = False
    for part in msg.walk():
        if part.get_content_type().find('application/pdf') > -1:
            attached = True
    if attached:
        print 'Attachment(s) found!'
        ans = ask('Want to download?(Y/N)')
        if ans == 'Y' or ans == 'y':
            path = ask('Specify a path to save:')
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype.find('application/pdf') > -1:
                    ext = ctype[ctype.find('/')+1:]
                    fullpath = path+str(getNum())+'.'+ext
                    open(fullpath, "wb").write(part.get_payload(decode=True))
                    print 'Attachment saved to %s !' % fullpath


def getInsideAction(messages):
    print '[OPTIONS: ls, open, new, quit...]\n'
    global userid, password
    action = ask('command: ')
    if action == 'ls':
        print 'Inbox: %s' % len(messages)
        i = 0
        while i < len(messages):
            print '['+str(i+1)+'] ', messages[i]['subject']
            i = i+1
        getInsideAction(messages)
    elif action == 'quit':
        # pop_conn.quit()
        userid = ''  # clear the data
        password = ''
        print 'You are logged out'
        getAction()
    elif action == 'new':
        composeMail(userid, password)
        getInsideAction(messages)
    elif action == 'open':
        index = int(ask("please specify the mail number: "))
        if 0 < index <= len(messages):
            print '#'*64
            print 'SUBJECT:', messages[index-1]['Subject']
            print 'FROM:', messages[index-1]['From']
            print 'DATE:', messages[index-1]['Date']
            print '-'*24+'message below'+'-'*26+'\n'
            print extractMessageBody(messages[index-1])
            print '#'*64
            chkAttach(messages, index-1)  # check attachments
            getThisMailAction(messages, index-1)
        else:
            print 'number out of range!'
            getInsideAction(messages)
    elif action == 'help':
        print '[quit] exit login \n [new] compose new email\n [ls] list out mails in mailbox\n [open] open an email'
        getInsideAction(messages)
    else:
        print 'invalid command'
        getInsideAction(messages)


def readMail(pop_conn):  # get msg from server
    msgs = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1])+1)]
    msgs = ['\n'.join(m[1]) for m in msgs]
    msgs = [parser.Parser().parsestr(m) for m in msgs]  # a list of raw messages
    pop_conn.quit()  # maybe later?
    return msgs


def login():
    global userid, password  # maybe global is not a good solution?
    userid = getUser()
    password = getPassword(userid)
    connection = connect(userid, password)
    messages = readMail(connection)
    getInsideAction(messages)
