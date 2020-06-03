import requests
import bs4
import open_url
import openpyxl


def openurl(keyword, order, duration):
    url = "https://search.bilibili.com/all?keyword=" + keyword
    if order == "1":
        pass
    elif order == "2":
        url = url + "&order=click"
    elif order == "3":
        url = url + "&order=pubdate"
    elif order == "4":
        url = url + "&order=dm"
    elif order == "5":
        url = url + "&order=stow"

    if duration == "0":
        url = url + "&duration=" + duration
    if duration == "1":
        url = url + "&duration=" + duration
    if duration == "2":
        url = url + "&duration=" + duration
    if duration == "3":
        url = url + "&duration=" + duration
    if duration == "4":
        url = url + "&duration=" + duration

    res = open_url.open_url(url)
    return res


def boil(res):
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    return soup


def find_title(soup):
    titles = []
    result = soup.find_all("li", class_="video-item matrix")
    for each in result:
        titles.append(each.a['title'])

    return titles


def find_upper(soup):
    upper = []
    result = soup.find_all("span", title="up主")
    for each in result:
        upper.append(each.a.text)

    return upper


def find_pubdate(soup):
    pubdate = []
    result = soup.find_all("span", title="上传时间")
    for each in result:
        # strip函数可去掉字符串开始前和结尾后多余的空格和换行符
        pubdate.append(each.text.strip())

    return pubdate


def find_views(soup):
    views = []
    result = soup.find_all("span", title="观看")
    for each in result:
        views.append(each.text.strip())

    return views


def find_dm(soup):
    dm = []
    result = soup.find_all("span", title="弹幕")
    for each in result:
        dm.append(each.text.strip())

    return dm


def find_url(soup):
    urls = []
    result = soup.find_all("li", class_="video-item matrix")
    for each in result:
        # strip函数可以删除网址前面的“//”和“?from=search“
        urls.append(each.a['href'].strip('//?from=search'))

    return urls


def find_duration(soup):
    durations = []
    result = soup.find_all("span", class_="so-imgTag_rb")
    for each in result:
        durations.append(each.text)

    return durations


def to_exl(result):
    '''
    wb = openpyxl.Workbook()
    ws = wb.active
    head = ["标题", "UP主", "时间", "发布日期", "时长", "弹幕数", "网址"]
    ws.append(head)

    for each in result:
        ws.append(each)

    wb.save("result.xlsx")
    '''
    with open("result.txt", "w", encoding="utf-8") as f:
        for each in result:
            f.write(each)


def main():
    '''
    keyword = input("请输入关键字：\n")
    order = str(input("请选择排序方式：[1]综合排序 [2]最多点击 [3]最新发布 [4]最多弹幕 [5]最多收藏\n"))
    duration = str(input(
        "请选择时长：[0]全部时长 [1]10分钟以下 [2]10-30分钟 [3]30-60分钟 [4]60分钟以上\n"))
    '''
    res = openurl("编程", "5", "4")
    soup = boil(res)
    title = find_title(soup)
    upper = find_upper(soup)
    pubdate = find_pubdate(soup)
    views = find_views(soup)
    dm = find_dm(soup)
    url = find_url(soup)
    duration = find_duration(soup)

    result = []
    length = len(title)
    for i in range(length):
        result.append(title[i] + upper[i] + pubdate[i] +
                      views[i] + dm[i] + url[i] + duration[i] + '\n')
    to_exl(result)


if __name__ == "__main__":
    main()
