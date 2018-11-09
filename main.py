import webbrowser
import history_url


def main():
    title = input('请输入您要查找的enwiki标题')
    text = input('请输入需要查询的段落')

    list1 = history_url.get_url(title)
    need_open_url = history_url.judge_history(list1, text, title)
    webbrowser.open(need_open_url)
    print('已打开链接：' + need_open_url)


if __name__ == '__main__':
    main()
    
