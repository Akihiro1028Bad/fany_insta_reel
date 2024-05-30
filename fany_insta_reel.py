# 必要なライブラリをインポート
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# 必要なモジュールをインポート
from selenium.webdriver.support.ui import WebDriverWait  # ウェブページの要素が読み込まれるのを待つためのモジュール
from selenium.webdriver.support import expected_conditions as EC  # 期待する条件を確認するためのモジュール
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import configparser
import tkinter.simpledialog as simpledialog



# InstagramDownloaderという名前のクラスを定義
class InstagramDownloader:
    # 初期化メソッド
    def __init__(self):

        # 以下の3行を追加
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")

        # self.driver = webdriver.Chrome(options=options)
        


        self.driver = webdriver.Chrome()


        self.driver.delete_all_cookies()


    # 入力されたURLからダウンロードリンクを取得するメソッド
    def get_download_link(self, input_url):

        # インスタグラムの動画ページにアクセス
        self.driver.get(input_url)

        wait = WebDriverWait(self.driver, 10)

        # Instagram Video Downloaderのサイトを開く
        self.driver.get("https://indown.io/reels")  # 実際のURLに置き換える必要がある

        # 検索ボックスを見つけて、URLを入力
        #search_box = self.driver.find_element_by_id("link")    # 実際の要素のIDやセレクタに置き換える
        search_box =self.driver.find_element(By.ID, "link")
        search_box.send_keys(input_url)

        # 検索ボタンを見つけてクリック
        search_button = self.driver.find_element(By.ID, "get") # 実際の要素のIDやセレクタに置き換える
        search_button.click()

        # WebDriverWaitオブジェクトを作成。これを使用して、特定の要素が読み込まれるまで最大10秒間待機できる
        wait = WebDriverWait(self.driver, 10)


        # 最初のセレクタで要素を探す
        # 最初のセレクタで要素を探す
        try:

            video_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video.img-fluid")))
            source_element = video_element.find_element(By.TAG_NAME, "source")
        except NoSuchElementException:
            source_element = None


        # 見つかった要素から href 属性を取得して返す
        print(source_element.get_attribute("src"))
        return source_element.get_attribute("src")

    # 入力されたURLからユーザ名を取得するメソッド
    def get_username_from_url(self, input_url):

        self.driver.get(input_url)

        wait = WebDriverWait(self.driver, 10)

        user_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._acan._acao._acat._acaw")))
        if user_element.text:
            print(user_element.text)
        else:
            print("Element has no text.")

        return "@" + user_element.text

    # 取得したダウンロードリンクからコンテンツをダウンロードするメソッド
    def download_content(self, download_link):

        # download_linkがNoneかどうかを確認
        if download_link is None:
            print("Error: Download link not found!")
            return None

        

        b_response200 = False
        while(not b_response200):

            # ダウンロードリンクからコンテンツを取得
            response = requests.get(download_link)
            
            # 応答が正常であることを確認（HTTPステータスコードが200の場合）
            if response.status_code == 200:
                # コンテンツをローカルファイルに保存
                with open('downloaded_file.mp4', 'wb') as file:
                    file.write(response.content)
                b_response200 = True # レスポンス200が返ってきて正常な動作をするまで繰り返す
            else:
                print(f"Error: Unable to download the content. HTTP Status Code: {response.status_code}")

                #try:
                    # 失敗している場合、再度ダウンロードリンクを取得
                    #video_element = EC.presence_of_element_located((By.CSS_SELECTOR, "video.img-fluid"))
                    #source_element = video_element.find_element(By.TAG_NAME, "source")
                #except NoSuchElementException:
                    #source_element = None


        # 見つかった要素から href 属性を取得して返す
        #print(source_element.get_attribute("src"))

        return 'downloaded_file.mp4'

    # ダウンロードしたコンテンツをインスタグラムにアップロードするメソッド
    def upload_to_instagram(self, file_path, user_input_text, login_user_name, login_password):

        # インスタグラムのログインページを直接開く
        self.driver.get('https://www.instagram.com/accounts/login/')

       # WebDriverWaitオブジェクトを作成。これを使用して、特定の要素が読み込まれるまで最大10秒間待機できる
        wait = WebDriverWait(self.driver, 10)  # 10秒待機

        # 要素が読み込まれたら、その要素を変数`username_input`に代入
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        # `username_input`に文字列を入力
        username_input.send_keys(login_user_name)  # 'あなたのユーザー名'の部分は実際のユーザー名に置き換えてください

        # 要素が読み込まれたら、その要素を変数`password_input`に代入
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        # `password_input`に文字列を入力
        password_input.send_keys(login_password)  # 'あなたのパスワード'の部分は実際のパスワードに置き換えてください
        password_input.submit()

        # 少し待機（ページが完全に読み込まれるのを待つため）
        wait = WebDriverWait(self.driver, 10)  # 10秒待機
        
        #try:
            # 指定のCSSセレクタを持つ要素を探す(ログイン情報を保存しますか？)
            #element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w")))
            # 要素が存在する場合、クリックする
            #if element:
                #element.click()
        #except TimeoutException:
            #print("「ログイン情報を保存しますか？」のボタンが見つかりませんでした。処理を続行します。")

        # 指定のCSSセレクタを持つ要素を探す(お知らせ機能をオンにしますか？)
        #self.driver.save_screenshot('C:\\Users\\ttmak\\screenshot.png')
        #try:
            
            #button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="_a9-- _ap36 _a9_1" and text()="後で"]')))
            # 要素が存在する場合、クリックする
            #if button:
                #button.click()
        #except TimeoutException:
            #print("「後で」のボタンが見つかりませんでした。処理を続行します。")

        # 新しい投稿ボタンをクリック（PC版のWebインターフェースでは通常この機能は利用できません。モバイル版のエミュレートが必要となる場合があります）
        try:
            new_post_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div svg[aria-label="新規投稿"]')))
            new_post_btn.click()
        except TimeoutException:
            print("新規投稿ボタンが見つかりませんでした。セレクタやページの状態を確認してください。")

        try:
            new_post_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span svg[aria-label="投稿"]')))
            new_post_btn.click()
        except TimeoutException:
            print("新規投稿ボタンが見つかりませんでした。セレクタやページの状態を確認してください。")

        # ファイル選択ダイアログにファイルパスを入力
        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[type="file"]._ac69')))

         # 絶対パスを取得
        absolute_path = os.path.abspath(file_path)
        file_input.send_keys(absolute_path)

        # りールが～できるようになりました。のボタン
        button_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'button._acan._acap._acaq._acas._acav._aj1-[type="button"]')))
        button_element.click()

        # 対象のdiv要素を特定するためのCSSセレクター
        css_selector = "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.xl56j7k svg[aria-label='切り取りを選択']"

        # 指定された要素が見つかるまで待機
        div_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )

        # div要素をクリック
        div_element.click()


        # 対象のdiv要素を特定するためのCSSセレクター
        css_selector = "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xz9dl7a.xn6708d.xsag5q8.x1ye3gou.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 svg[aria-label='縦型トリミングアイコン']"

        # 指定された要素が見つかるまで待機
        div_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )

        # div要素をクリック
        div_element.click()

        # テキスト内容 "次へ" を持つdiv要素を全て取得　3回表示される
        next_button = wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="次へ"]')))
        next_button.click()

        next_button1 = wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="次へ"]')))
        next_button1.click()

        # キャプション入力エリアを見つける
        caption_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[aria-label="キャプションを入力…"]')))
        # キャプション入力エリアにテキストを入力
        #caption_area.send_keys(username + "様" + "\n" + user_input_text)
        caption_area.send_keys(user_input_text + " #面白い #おもしろ動画 #衝撃 #衝撃映像 #やば")

        # シェアボタンをクリック
        share_button = wait.until(EC.presence_of_element_located((By.XPATH,'//div[text()="シェア"]')))
        share_button.click()

        # 指定された要素が表示されるのを最大3分待機
        element = WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="リール動画がシェアされました"]'))
        )

    # ブラウザを閉じるメソッド
    def close(self):
        self.driver.close()



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Instagram Downloader and Uploader")
        self.geometry("450x720")

        # URL入力ラベルとエントリー
        self.url_label = tk.Label(self, text="Reel URL:")
        self.url_label.pack(pady=10)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=10)

        # 本文入力ラベルとテキストウィジェット
        self.text_label = tk.Label(self, text="本文テキスト:")
        self.text_label.pack(pady=10)
        self.text_entry = tk.Text(self, width=45, height=20)  # 複数行入力のためのテキストウィジェット
        self.text_entry.bind('<Key>', lambda e: self.limit_size(e, 200))  # 文字数制限のイベントを追加
        self.text_entry.pack(pady=5)
        # 定型文選択ボタン
        self.preset_button = tk.Button(self, text="定型文を選択する", command=self.open_preset_window)
        self.preset_button.pack(pady=10)


        # 実行ボタン
        self.execute_button = tk.Button(self, text="実行", command=self.process)
        self.execute_button.pack(pady=20)

        # 設定を読み込み
        self.load_settings()

    def limit_size(self, event, max_chars):  # 文字数制限のためのメソッド
        value = self.text_entry.get(1.0, tk.END)
        if len(value) > max_chars + 1:  # +1 は末尾の改行をカウントするため
            self.text_entry.delete(1.0, tk.END)
            self.text_entry.insert(1.0, value[:max_chars])

    # 定型文選択編集画面を開くメソッド
    def open_preset_window(self):
        self.preset_window = PresetWindow(self)

    def load_settings(self):
            config = configparser.ConfigParser()
            config.read('settings.ini')

            if 'Instagram' in config:
                self.username_entry.insert(0, config['Instagram'].get('username', ''))
                self.password_entry.insert(0, config['Instagram'].get('password', ''))

    def save_settings(self):
        config = configparser.ConfigParser()

        config['Instagram'] = {
            'username': self.username_entry.get(),
            'password': self.password_entry.get()
        }

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

            messagebox.showinfo("Success", "設定が保存されました")

    def process(self):
        # ユーザの入力を取得
        user_input_url = self.url_entry.get()
        user_input_text = self.text_entry.get(1.0, tk.END)

        # 上記のメイン処理をここに追加...
        # ▼以下がメインの処理です

        # 実際の処理の流れ
        downloader = InstagramDownloader()  # インスタンスを作成
        #username = downloader.get_username_from_url(user_input_url)#ユーザ名を取得
        download_link = downloader.get_download_link(user_input_url)  # ダウンロードリンクを取得
        file_path = downloader.download_content(download_link)  # コンテンツをダウンロード
        downloader.upload_to_instagram(file_path,user_input_text,"ak10280322","1028Akihiro")  # インスタグラムにアップロード
        downloader.close()  # ブラウザを閉じる

        # 処理完了メッセージ
        messagebox.showinfo("Success", "処理が完了しました")

# 定型文編集画面本体
class PresetWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("定型文の選択と編集")
        self.geometry("500x500")

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self, text="追加", command=self.add_preset)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = tk.Button(self, text="編集", command=self.edit_preset)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self, text="削除", command=self.delete_preset)  # 削除ボタンを追加
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.select_button = tk.Button(self, text="選択", command=self.select_preset)
        self.select_button.pack(side=tk.LEFT, padx=10)

        # ここで定型文をロードするためのメソッドを呼び出す
        self.load_presets()

    def load_presets(self):
        # ここで設定ファイルから定型文をロードする
        config = configparser.ConfigParser()
        config.read('presets.ini')
        if 'Presets' in config:
            for key in config['Presets']:
                self.listbox.insert(tk.END, config['Presets'][key])
        pass

    def add_preset(self):
        # 定型文を追加するためのロジック
        preset = self.multiple_line_input("新しい定型文", "新しい定型文を入力してください:")
        if preset:
            self.listbox.insert(tk.END, preset)
            self.save_presets()
        pass

    def edit_preset(self):
        # 選択した定型文を編集するためのロジック
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        initial_preset = self.listbox.get(selected_index)
        new_preset = self.multiple_line_input("定型文の編集", "定型文を編集してください:", initial_preset)
        
        if new_preset:
            self.listbox.delete(selected_index)
            self.listbox.insert(selected_index, new_preset)
            self.save_presets()

    def select_preset(self):
        selected_index = self.listbox.curselection()
        if not selected_index:  # 何も選択されていない場合はreturn
            return
        selected_preset = self.listbox.get(selected_index)
        self.master.text_entry.delete(1.0, tk.END)
        self.master.text_entry.insert(tk.END, selected_preset)
        self.destroy()  # この行を追加

    def save_presets(self):
        config = configparser.ConfigParser()
        presets = [self.listbox.get(idx) for idx in range(self.listbox.size())]
        config['Presets'] = {f"Preset_{idx}": preset for idx, preset in enumerate(presets)}
        with open('presets.ini', 'w') as configfile:
            config.write(configfile)

    def multiple_line_input(self, title, prompt, initial_value=""):
        # 複数行の入力ダイアログを表示
        result = None

        def on_ok():
            nonlocal result
            result = text_widget.get(1.0, tk.END).strip()
            dialog.destroy()

        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("400x400")
        label = tk.Label(dialog, text=prompt)
        label.pack(pady=10)
        text_widget = tk.Text(dialog, height=20, width=45, wrap=tk.WORD)
        text_widget.insert(tk.END, initial_value)
        text_widget.pack(pady=5)
        ok_button = tk.Button(dialog, text="保存", command=on_ok)
        ok_button.pack(pady=20)
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)

        return result

    def limit_size(self, event, max_chars, widget):  # 文字数制限のためのメソッド
        value = widget.get(1.0, tk.END)
        if len(value) > max_chars + 1:  # +1 は末尾の改行をカウントするため
            widget.delete(1.0, tk.END)
            widget.insert(1.0, value[:max_chars])

    def delete_preset(self):  # 定型文を削除するための新しいメソッド
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        self.listbox.delete(selected_index)
        self.save_presets()


if __name__ == "__main__":
    app = App()
    app.mainloop()



