
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import time
import csv

# アクセスしたいWebサイトのトップページ
url = "https://www.musashino-u.ac.jp/"

# 同一ドメインを判定するための情報
domain = urlparse(url).netloc

# URLをキー、titleを値にする辞書
sitemap = {}

# これからアクセスするURL
url_list = [url]

# すでにアクセスしたURL
visited = set()

# Webサイトにアクセスする間隔（秒）
sleep_seconds = 1

# Webサイトにアクセスする前に robots.txt などの
# 巡回ルールを確認してから実行すること

while len(url_list) > 0:

    # URLを1つ取り出す
    current_url = url_list.pop(0)

    # URLの#以降を取り除く
    current_url = urldefrag(current_url)[0]

    # アクセス済みならスキップ
    if current_url in visited:
        continue

    # 同一ドメイン以外にはアクセスしない
    if urlparse(current_url).netloc != domain:
        continue

    # アクセス済みとして登録
    visited.add(current_url)

    try:
        # サーバーへの負荷を軽減するために待機
        time.sleep(sleep_seconds)

        # Webサーバーにリクエストを送る
        res = requests.get(current_url, timeout=15)

        # HTTPエラーを確認
        res.raise_for_status()

        # HTML以外のファイルは対象外
        content_type = res.headers.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            continue

        # HTMLをBeautifulSoupオブジェクトに変換
        html_soup = BeautifulSoup(res.content, "html.parser")

        # titleタグからタイトルを取得
        title_tag = html_soup.find("title")

        if title_tag is not None:
            title = title_tag.get_text(strip=True)
        else:
            title = ""

        # URLをキー、タイトルを値にして辞書に格納
        sitemap[current_url] = title

        print("URL：", current_url)
        print("タイトル：", title)
        print("--------------------------")

        # ページ内のaタグをすべて取得
        a_list = html_soup.find_all("a", href=True)

        for a in a_list:

            # 相対URLを絶対URLに変換
            next_url = urljoin(res.url, a["href"])

            # #以降を取り除く
            next_url = urldefrag(next_url)[0]

            # URLの情報を取得
            parsed_url = urlparse(next_url)

            # HTTPまたはHTTPSのリンクだけを対象にする
            if parsed_url.scheme not in ["http", "https"]:
                continue

            # 同じドメインのリンクだけを追加
            if parsed_url.netloc == domain:

                # アクセス済みでなければ追加
                if next_url not in visited:
                    if next_url not in url_list:
                        url_list.append(next_url)

    except requests.RequestException as e:
        print("アクセスエラー：", current_url)
        print(e)

# 辞書型変数の内容をCSVファイルに保存
with open(
    "musashino_university_sitemap.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)

    # CSVの見出し
    writer.writerow(["URL", "Title"])

    # 辞書の内容を書き込む
    for page_url, page_title in sitemap.items():
        writer.writerow([page_url, page_title])

print("サイトマップの抽出が終了しました")
print("取得したページ数：", len(sitemap))
print("CSVファイル：musashino_university_sitemap.csv")
