import requests
from bs4 import BeautifulSoup

# 设置目标网址
url = 'https://book.douban.com/'

# 设置请求头（模拟浏览器访问）
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

# 发起请求
response = requests.get(url, headers=headers)
print(f"请求状态码: {response.status_code}")
if response.status_code != 200:
    print("请求失败，退出程序。")
    exit()

# 解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')
print("开始解析页面内容...")

# 抓取所有书籍标题（这里只是示意）
titles = soup.select('div[class="title"]')

# 打印标题
if not titles:
    print("未找到任何匹配的标题，可能是选择器有误或内容是动态加载的。")
else:
    print(f"共找到 {len(titles)} 个标题：")
    
for idx, title in enumerate(titles, 1):
    #print(f"调试：抓取的原始元素 HTML -> {title}")
    print(f"{idx}. {title.get_text(strip=True)}")