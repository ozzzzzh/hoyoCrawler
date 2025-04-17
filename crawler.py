from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def vSeleniumInit():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def pstGetAllArticle(pstDriver, pcUrl):
    pstDriver.get(pcUrl)
    pcHtml = pstDriver.page_source
    print("主页加载完成，开始解析文章链接...")
    soup = BeautifulSoup(pcHtml, 'html.parser')  
    # 提取文章链接
    articles = soup.find_all('a', class_='mhy-article-card__link')  # 根据实际的HTML结构调整类名
    article_urls = ['https://www.miyoushe.com' + a['href'] for a in articles]
    print(f"共找到 {len(article_urls)} 篇文章") 
    return article_urls

def pstGetAllDataFromArticle(pstArticles, pstCrawlerDriver):
    # 遍历每篇文章
    for url in pstArticles:
        print(f"正在打开文章：{url}")
        pstCrawlerDriver.get(url)
        time.sleep(3)  # 等待页面加载完成
        article_html = pstCrawlerDriver.page_source
        article_soup = BeautifulSoup(article_html, 'html.parser')

        # 提取创作声明信息
        auth_label_span = article_soup.find('span', class_='auth-type__label')
        auth_message = auth_label_span.get_text(strip=True) if auth_label_span else '无创作声明信息'
        print(f"创作声明信息: {auth_message}")

        # 创作声明标识：0 = 允许转载，1 = 禁止转载，2 = 无声明
        if "允许规范转载" in auth_message:
            can_repost = 0
        elif "禁止转载" in auth_message:
            can_repost = 1
        else:
            can_repost = 2

        # 提取作者姓名
        author_span = article_soup.find('span', class_='mhy-account-title__name')
        author_name = author_span.get_text(strip=True) if author_span else '无作者'
        print(f"作者: {author_name}")

        # 提取头像
        avatar_div = article_soup.find('div', class_='mhy-avatar mhy-user-card__avatar mhy-avatar__xl')
        avatar_img = avatar_div.find('img') if avatar_div else None
        author_avatar = avatar_img['src'] if avatar_img and 'src' in avatar_img.attrs else '无头像'
        print(f"头像: {author_avatar}")

        # 提取标题
        title_tag = article_soup.find('h1')
        if not title_tag:
            title_container = article_soup.find('div', class_='mhy-video-article-container__info-title')
            if title_container:
                title_tag = title_container.find('div', class_='title-text')
        title = title_tag.get_text(strip=True) if title_tag else '无标题'
        print(f"提取到标题: {title}")

        # 提取内容
        content_div = article_soup.find('div', class_='mhy-article-page__content')
        if content_div:
            combined_parts = []
            link_text_nodes = set()
            for elem in content_div.descendants:
                if elem.name == 'a' and 'href' in elem.attrs:
                    link_text = elem.get_text(strip=True)
                    href = elem['href']
                    combined_parts.append(f"[{link_text}]({href})")
                    # Store text children to skip them later
                    link_text_nodes.update(elem.strings)

            for elem in content_div.descendants:
                if isinstance(elem, str):
                    if elem in link_text_nodes:
                        continue  # Skip text that was already part of a hyperlink
                    parent = elem.parent
                    if parent and parent.name == 'a':
                        continue
                    stripped = elem.strip()
                    if stripped:
                        combined_parts.append(stripped)
                elif elem.name == 'div' and 'ql-image-box' in elem.get('class', []):
                    image_url = elem.get('data-url')
                    if image_url:
                        combined_parts.append(f"[图片]({image_url})")
                        
            content = '\n'.join(combined_parts)
        else:
            content = '无内容'
        #print(content)
        
        # 提取视频资源信息
        video_tag = article_soup.find('div', class_='mhy-video-player__video')
        video_src = video_tag.find('video')['src'] if video_tag and video_tag.find('video') else '无视频链接'

        cover_div = article_soup.find('div', class_='mhy-video-player__cover')
        if cover_div and 'style' in cover_div.attrs:
            style_attr = cover_div['style']
            match = re.search(r'url\("(.*?)"\)', style_attr)
            video_cover = match.group(1) if match else '无封面链接'
        else:
            video_cover = '无封面链接'

        print(f"视频链接: {video_src}")
        print(f"视频封面: {video_cover}")