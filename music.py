import requests
import open_url
import json
import bs4


def get_data(url):
    data = []
    url = list(url)
    url[22] = ''
    url[23] = ''
    url = ''.join(url)
    res = open_url.open_url(url)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    name = soup.find("meta", property="og:title")['content']
    info = soup.find_all("p", class_="des s-fc4")

    artist = info[0].get_text()
    album = info[1].get_text()

    data.append(name)
    data.append(artist)
    data.append(album)

    return data


def get_hot_comments(res):
    comment_json = json.loads(res.text)
    if comment_json['hotComments'] == []:
        hot_comments = comment_json['comments']
    else:
        hot_comments = comment_json['hotComments']

    return hot_comments


def get_comments(url):
    name_id = url.split('=')[1]

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36"}
    data = {"params": "ULb1PEJpkuh95295STOT764rtsMm4uannacFGmqB5umRAdilkv8wWt7UD+kBS8U5qiAikwOOEaMX9AEP+/GEkrT/l6Dk3dV5Tv1baHi4xuwhl2KVKcnJ7df6ZRySMOrDAj20ZgRoTL+uyi4qMoKzzzcQ8R1j59LMgnnj/vPBhd9s7m5dui+R9j/N2YtiMmK1",
            "encSecKey": "cceee9f18dd9efba49a0b9be045f86c851892ded316eaac5b6547734d1faf6146e818ea54f013520ca156e44a90993fb2a89673fb444782dedd5cdb348c7a755121e89587b767dbfb4b1dd895c1a9673919fb070e8b0f43655a96f16b4a99f141fee404101434f232dfb1bcf7bba001ea11a823af5a00a16164fb7ed1e7cdedf"
            }

    target_url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(
        name_id)

    res = requests.post(target_url, headers=headers, data=data)

    return res


def main():
    url = input("请输入网址:")
    res = get_comments(url)
    hot_comments = get_hot_comments(res)
    data = get_data(url)

    with open("{}.txt".format(data[0]), "w", encoding="utf-8") as file:
        file.write("《{}》".format(data[0]) + "\n" +
                   data[1] + "\n" + data[2] + "\n")
        file.write("-----------------------------------------------\n")

        for i in hot_comments:
            if i['beReplied'] != []:
                file.write(i['user']['nickname'] + '    回复    ')

                for each in i['beReplied']:
                    file.write(each['user']['nickname'] + '：' + "\n")
                    try:
                        file.write("“" + each['content'] + "”" + "\n" + "\n")
                    except TypeError:
                        file.write("（该评论已被删除）" + "\n" + "\n")

            else:
                file.write(i['user']['nickname'] + '：''\n\n')

            file.write(i['content'] + '\n')
            file.write("👍：")
            file.write(str(i['likedCount']) + '\n')
            file.write("--------------------------------\n")


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        print("网址错误")
    else:
        print("Done.")
