# -*- coding: utf-8 -*-
import urllib
import urllib2
import re

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()

#百度贴吧爬虫类
class BDTB:
#初始化方法，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,seeLZ,floorTag):
        self.baseURL=baseURL
        self.see_LZ='?see_lz='+str(seeLZ)
        self.floorTag=floorTag
        self.floor=1
        self.tool=Tool()
        self.file=None
        self.defaultTitle="baidu tieba"

#传入某一页的索引获得页面
    def getPage(self, pageNum):
        try:
            url=self.baseURL+self.see_LZ+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
            content=response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print u"connect error",e.code
                return None

    def getTitle(self,page):
        #得到标题的正则表达式
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            #如果存在，则返回标题
            return result.group(1).strip()
        else:
            return None
    #获取帖子一共有多少页
    def getPageNum(self,page):
        #获取帖子页数的正则表达式
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

#获取每一层楼的内容，传入页面的内容

    def getContent(self,content):
        pattern = re.compile('<div.*?class="d_post_content.*?">(.*?)</div>',re.S)
        items=re.findall(pattern,content)
        contents = []
        for item in items:
            # 将文本进行去除标签处理，同时在前后加入换行符
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents
#定义保存文件的文件名
    def setFileTitle(self,title):
        if title is not None:
            self.file = open(title + ".txt","w+")
        else:
            self.file = open(self.defaultTitle + ".txt","w+")

#写入数据

    def writeData(self,contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                #楼之间的分隔符
                floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

#开始执行
    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "invalid"
            return
        try:
            print "Total " + str(pageNum) + " page"
            for i in range(1,int(pageNum)+1):
                print "Writing " + str(i) + " Page"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        #出现写入异常
        except IOError,e:
            print "error" + e.message
        finally:
            print "completed"

# print u"Please input the number"
# baseURL = "http://tieba.baidu.com/p/" + str(raw_input(u"http://tieba.baidu.com/p/"))
# seeLZ = raw_input("lz only(是输入1，否输入0)：")
# floorTag = raw_input("floor(是输入1，否输入0):")

baseURL = r"https://tieba.baidu.com/p/5334635196"
seeLZ =1
floorTag=0
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()