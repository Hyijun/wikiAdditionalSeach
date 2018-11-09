import urllib.request as ur



def main():
    title = 'https://en.wikipedia.org/wiki/' + input('请输入您要查找的enwiki标题')
    text = input('请输入需要查询的段落')

    print(is_in_search(text, title))


if __name__ == '__main__':
    main()
