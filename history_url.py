import urllib.request as ur
import webbrowser


def get_number(url):
    return url[43:]


def get_html(url):
    res = ur.urlopen(url)
    html = res.read().decode('utf-8')
    return html


def is_in_search(s, url):
    html = get_html(url)
    if s in html:
        return True
    else:
        return False


def get_history_url(html, begin=10):
    before_html = len(html[:begin])

    need_find = r'<li data-mw-revid="'
    url_begin = html[begin:].find(need_find) + 19 + before_html
    url_end = r'"'
    end = html[url_begin:].find(url_end)
    history_url = html[url_begin:url_begin + end]
    int(history_url)
    real_url = 'https://en.wikipedia.org/w/index.php?oldid=' + history_url

    """
    need_fine_name1 = html[begin:].find(r'<a href="/wiki/User:') + before_html + 20
    need_fine_name2 = html[begin:].find(r'<a href="/wiki/Special:Contributions/') + before_html + 37
    name_end1 = html[need_fine_name1:].find('"')
    name_end2 = html[need_fine_name2:].find('"')
    user_name1 = html[need_fine_name1:need_fine_name1+name_end1]
    user_name2 = html[need_fine_name2:need_fine_name1+name_end2]
    
    char = ['\\', '/', '"', '<', '>', '=']
"""
    # print([real_url, url_begin + end])
    return [real_url, url_begin + end]


def get_url(title):
    history_info = []
    passage_url = r'https://en.wikipedia.org/w/index.php?title=' + title + r'&offset=&limit=500&action=history'
    res = ur.urlopen(passage_url)
    html = res.read().decode('utf-8')
    history_position1 = html.find(r'<form action="/w/index.php" id="mw-history-compare">') + 52
    for i in range(500):
        try:
            history_info.append(get_history_url(html, history_position1))
        except ValueError:
            break
        history_position1 = history_info[i][1]
    print('这个条目共有' + str(len(history_info)) + '个历史版本')
    return history_info


def judge_history(history_info, text, title):
    top = 0
    foot = len(history_info) - 1
    in_top = False
    in_foot = False
    while 1:
        print('正在进行比较版本[较旧]' + get_number(history_info[foot][0]) + '与版本[较新]' + get_number(history_info[top][0]), end='，结果：')

        if text in get_html(history_info[foot][0]):
            print('√', end='')
            in_foot = True
        else:
            print('×', end='')
            in_foot = False

        if text in get_html(history_info[top][0]):
            print('√', end='\n')
            in_top = True
        else:
            print('×', end='\n')
            in_top = False

        if in_foot and foot == len(history_info) - 1:
            print()
            return history_info[len(history_info) - 1][0]

        if not in_top and not in_foot:
            top = top + 1
            foot = foot - 1
            continue

        if in_foot and not in_top:
            if foot - top == 1:
                print('找到了！在这儿：' + 'https://en.wikipedia.org/w/index.php?title='
                      + title
                      + '&diff=next'
                      + '&oldid='
                      + get_number(history_info[top+1][0])
                      )
            top = foot - (foot - top)//2

        if in_foot and in_top:
            top, foot = top + (foot - top)//2, foot + (foot - top)//2

        if not in_foot and in_top:
            foot = foot - 1

        if not in_foot and in_top:
            if foot - top == 1:
                return 'https://en.wikipedia.org/w/index.php?title=' + title + '&diff=' + get_number(history_info[foot][0]) + '&oldid='+ get_number(history_info[top][0])


if __name__ == '__main__':
    # res = ur.urlopen('https://en.wikipedia.org/w/index.php?title=God_of_War:_Ghost_of_Sparta&action=history')
    # html = res.read().decode('utf-8')
    # get_history_url(html)
    list1 = get_url('Combo_(video_gaming)')
    need_open_url = judge_history(list1, 'A combo can be very long, and in th', 'Combo_(video_gaming)')
    webbrowser.open(need_open_url)
    print('已打开链接：' + need_open_url)
