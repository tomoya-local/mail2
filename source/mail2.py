
# 必要なライブラリのインポート

import smtplib, ssl
from email.mime.text import MIMEText
import pickle
import os
import sys
import copy
import configparser
import getpass
import hashlib
import glob
import datetime
ccff=0
cc=0
g=0
args = sys.argv

#ホスト情報の追加関数
def hostadd():
    print('')
    host2=input(' smtpサーバのホスト名 >> ')
    print('')
    print(' ポート番号はサーバー側から特に指定のない場合、\n SSL用ポート番号の「465」を入力してください')
    print('')
    port=input(' smtpサーバのポート番号 >> ')
    if port=="":
       port="465"
    host="none"
    account = "none"
    from_email=account
    print('')
    password = 'none'
    filename=input(' セッションファイル名 >> ')
    filename=filename+".bin"
    config = configparser.ConfigParser()
    section2 = 'profile'
    section2 = 'profile'
    try:
        config.add_section(section2)
    except configparser.DuplicateSectionError:
        pass
    config.set(section2, 'file', filename)
    try:
        cc=config.get(section2, 'hostc')
        cc=2
    except configparser.NoOptionError:
        cc=2
    config.set(section2, 'hostc', str(cc))
    with open('.\\host.ini', 'w') as file:
        config.write(file)
    print(' ')
    print(' 記憶したセッション情報をクリアするには\n アプリケーションディレクトリ内の「profile.bin」を削除してください')
    print('')
    cgn=input(' 次回からユーザー情報の入力を省略します (Enter) >>')
    usear=[host,password,cgn,host2,port]
    f=open(filename,'wb')
    pickle.dump(usear,f)
    f.close()
    os.system('cls')
    file=copy.copy(filename)
    return host2, port
ccff=1
cds=0
j=len(args)
if j==2:
    with open(args[1]) as f:
        message = f.read()
        cds=1
filecheck=os.path.exists('./host.ini')
if filecheck==0:
    host2,port=hostadd()
    ccff=0
#configの読み取り
if filecheck!=0:
    ccvg=1
    try:
        config = configparser.ConfigParser()
        config.read('./host.ini')
        section1 = 'profile'
        file=config.get(section1, 'file') # localhost
        cc=config.get(section1, 'hostc')
        g=os.path.isfile(file)
    except configparser.NoSectionError:
        g=0
else:
    ccvg=0
os.chdir("./")
os.system('cls')
cc=int(cc)

print('')
ccd=1

ffm=os.path.isfile('.\host.ini')
#セッションファイルのロード画面
while ccd==1:
    os.system('cls')
    os.chdir("./")
    print('')
    file="-a"
    if file=="-a":
        co=-1
        os.system('cls')
        print('')
        print(' ファイルインデックスを入力してください \n インデックスは必ず0から始まります')
        print('')
        files=glob.glob(".\\*.bin")        
        for x in files:
            co=co+1
            print(' '+str(co)+":"+x)
            print('')
        print('')
        coun=len(files)-1
        print(' 最大インデックスは'+str(coun)+"です")
        print('')
        print(' -2:ホスト情報の追加')
        print('')
        ac=input(' ファイルインデックス  0～ >> ')
        ac=int(ac)
        if ac==-2:
            os.system('cls')
            host2,port=hostadd()
            ccf=0
            continue
        if ac<-1:
            ac=0
        if coun<ac:
            ac=copy.copy(coun)
        break

# 表示位置調整
print('')
os.system('cls')
# デバッグ情報の表示
debag=0
def login(host2,port,server):
    while cdf==1:
        # ログイン画面
        print('')
        print(' ログイン')
        print('')
        account=input(' ユーザー名 >> ')
        print('')
        password=getpass.getpass(' アカウントパスワード>> ')
        from_email=account
        try:
            server.login(account, password)
            server.set_debuglevel(debag)
        except:
            print('')
            print(' エラー:認証に失敗しました')
            print('')
            print(' ユーザーアカウントを確認してください')
            print('')
            print(' アカウントの権限を確認してください')
            print('')
            input(' リトライするにはエンターキーを押してください')
            g=0
            os.system('cls')
            continue
        else:
            break
    return from_email,server
# SMTPサーバへの接続
cdf=1
while cdf==1:
    try:
        file=copy.copy(files[ac])
    except IndexError:
        os.system('cls')
        print(' エラー！：ホスト情報がありません')
        print('')
        host2,port=hostadd()
        ccff=0
    g=os.path.isfile(file)
    if g==True and ccvg==1:
        # SMTP認証情報の読み込み
        f=open(file,'rb')
        usear=pickle.load(f)
    if ccff==1:
        host2=copy.copy(usear[3])
        port=copy.copy(usear[4])
    try:
        server = smtplib.SMTP_SSL(host2, int(port), context=ssl.create_default_context())
    except:
        print(' 接続に失敗しました...')
        print('')
        print(' エラー：セッションファイル名 '+file)
        print('')
        print('　セッション情報を設定しなおさない場合ソフトウェアを終了します')
        print('')
        kg=input(' セッション情報を設定しなおしますか? (y or n) >>')
        if kg=="y" or kg=="Y":
            host2,port,file=hostadd()
            g=0
            continue
        else:
            sys.exit()
    else:
        print('')
        from_email,server=login(host2,port,server)        
        break

os.system('cls')
print('')

# 送信先
to_email = input(' 送信先 >> ')
print('')
 
# MIMEの作成
subject = input(' 件名 >> ')
print('')
print(' 改行するには改行タグ/nを入力してください')
print('')
print(' このメールはhtmlタグを使用できます。')
print('')

# 本文の入力（ファイルからの読み込みの場合は入力しない)
if cds==0:
    message = input(' 本文 >> ')
message1=copy.copy(message)
message=message.replace('/n','<br>')

# メールの作成
msg = MIMEText(message, "html")
msg["Subject"] = subject
msg["To"] = to_email
msg["From"] = from_email
backups="件名:"+subject+"\n送信先: "+to_email+"\n送信元:"+from_email+"\n\n本文:"+message1
print('')
print(backups)
print('')

# メールの送信
try:
    server.send_message(msg)
except:
    print(' エラー:送信に失敗しました。\n 送信先のメールアドレスを確認してください')
    print('')
    input(' 終了するにはエンターキーを押してください')
    server.quit()
    sys.exit()
else:
    server.quit()
    to="to:"+to_email
    from2="from:"+from_email
    sub="件名:"+subject
    dt_now = datetime.datetime.now()
    data=dt_now.strftime('%Y/%m/%d/ %H:%M:%S')
    msg="本文:"+message1+"\n"
    backups="\n\n件名:"+subject+"\n送信先: "+to_email+"\n送信元:"+from_email+"\n日付："+data+"\n\n本文:"+message1
    usear=[to,from2,sub,data,msg]
    with open("./mail.log", mode='a') as f:
        f.write(backups)
    f.close()
    input(' 送信しました>>')
sys.exit()
