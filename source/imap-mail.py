
import pickle
import email
import ssl
import imaplib
import getpass
import os
import glob
from email.header import decode_header, make_header
import copy
import sys
os.system('cls')
print('')


ccd=1
while ccd==1:
    os.system('cls')
    os.chdir("./")
    print('')
    file="-a"
    ccff=0
    if file=="-a":
        co=-1
        os.system('cls')
        print('')
        print(' このツールで表示できるのはメールのほとんどが文字で構成されたhtmlメールのみです。')
        print('')
        print(' ファイルインデックスを入力してください \n インデックスは必ず0から始まります')
        print('')
        files=glob.glob(".\\*.bins")        
        for x in files:
            co=co+1
            print(' '+str(co)+":"+x)
            print('')
        print('')
        coun=len(files)-1
        print(' 最大インデックスは'+str(coun)+"です")
        print('')
        print(' -2:手動入力')
        print('')
        print(' ここにbinsファイルが表示されない場合は「-2」を入力してください')
        print('')
        ac=input(' ファイルインデックス  0～ >> ')
        ac=int(ac)
        if ac==-2:
            os.system('cls')
            print('')
            host = input(' ホスト名 >> ')
            print('')
            print(' このソフトウェアのセッションファイル自体はmail2.exeと互換性がありません')
            print('')
            file=input(' セッションファイル名 >> ')
            file=file+".bins"
            print('')
            password = 'none'
            print(' ')
            cgn=""
            host2="none"
            port="none"
            usear=[host,password,cgn,host2,port]
            f=open(file,'wb')
            pickle.dump(usear,f)
            f.close()
            ccff=1
        if coun<ac:
            ac=copy.copy(coun)
        if ccff==0:
            try:
                file=copy.copy(files[ac])
            except:
                
                os.system('cls')
                print(' エラー！：ホスト情報がありません')
                print('')
                host = input(' ホスト名 >> ')
                print('')
                print(' このソフトウェアのセッションファイル自体はmail2.exeと互換性がありません')
                print('')
                file=input(' セッションファイル名 >> ')
                file=file+".bins"
                print('')
                password = 'none'
                print(' ')
                cgn=""
                host2="none"
                port="none"
                usear=[host,password,cgn,host2,port]
                f=open(file,'wb')
                pickle.dump(usear,f)
                f.close()
                ccff=1
            g=os.path.isfile(file)
            if g==True:
                # SMTP認証情報の読み込み
                f=open(file,'rb')
                usear=pickle.load(f)
                host=copy.copy(usear[0])
                if host=="none":
                    print('')
                    print(' 自動ロードに失敗しました...')
                    print('')
                    print(' セッションファイルが対応していません')
                    host = input(' ホスト名 >> ')
            
        break

while ccd==1:
    try:
        nego_combo = ("ssl", 993) # ("通信方式", port番号)
        if nego_combo[0] == "no-encrypt":
            imapclient = imaplib.IMAP4(host, nego_combo[1])
        elif nego_combo[0] == "starttls":
            context = ssl.create_default_context()
            imapclient = imaplib.IMAP4(host, nego_combo[1])
            imapclient.starttls(ssl_context=context)
        elif nego_combo[0] == "ssl":
            context = ssl.create_default_context()
            imapclient = imaplib.IMAP4_SSL(host, nego_combo[1], ssl_context=context)
        imapclient.debug = 0  # 各命令をトレースする
    except:
        print(' 接続に失敗しました...')
        print('')
        print(' エラー：セッションファイル名 '+file)
        print('')
        print(' セッション情報を設定しなおさない場合ソフトウェアを終了します')
        print('')
        kg=input(' 手動で接続しますか? (y or n) >>')
        if kg=="y" or kg=="Y":
            host = input(' ホスト名 >> ')
           
            print('')
            password = 'none'
            print(' ')
            print(' 記憶したセッション情報をクリアするには\n アプリケーションディレクトリ内の「profile.bin」を削除してください')
            print('')
            cgn=input(' 次回からユーザー情報の入力を省略します (Enter) >>')
            host2=copy.copy(usear[3])
            port=copy.copy(usear[4])
            usear=[host,password,cgn,host2,port]
            f=open(file,'wb')
            pickle.dump(usear,f)
            f.close()
            continue
    else:
        break
while ccd==1:    
    os.system('cls')
    print('')        
    print(' ログイン')
    print('')
    username = input(' ユーザーネーム(メールアドレス) >> ')
    print('')
    password = getpass.getpass(" パスワード >> ")

    try:
        imapclient.login(username, password)
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
print('')
imapclient.select() # メールボックスの選択
typ, data = imapclient.search(None, "ALL")  # data = [b"1 2 3 4 ..."]
datas = data[0].split()
fetch_num = input(' 取得したいメッセージ数 >> ')  # 取得したいメッセージの数
fetch_num=int(fetch_num)
if (len(datas)-fetch_num) < 0:
    fetch_num = len(datas)
msg_list = []  # 取得したMIMEメッセージを格納するリスト
for num in datas[len(datas)-fetch_num::]:
    typ, data = imapclient.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    msg_list.append(msg)
imapclient.close()
imapclient.logout()


os.system('cls')
c=0
for msg in msg_list:
    print(msg)

for msg in msg_list:
    # 各ヘッダ情報はディクショナリのようにアクセスできる
    from_addr = str(make_header(decode_header(msg["From"])))
    subject = str(make_header(decode_header(msg["Subject"])))

    # 本文(payload)を取得する
    if msg.is_multipart() is False:
        # シングルパートのとき
        payload = msg.get_payload(decode=True) # 備考の※1
        charset = msg.get_content_charset()    # 備考の※2
        if charset is not None:
            payload = payload.decode(charset, "ignore")
        print(payload)
        print()
    else:
        # マルチパートのとき
        for part in msg.walk():
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            charset = part.get_content_charset()
            if charset is not None:
                payload = payload.decode(charset, "ignore")
            print(payload)
            print()
input(' メールの取得終了')