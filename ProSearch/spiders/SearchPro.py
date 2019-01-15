# -*- coding: utf-8 -*-
import scrapy
from ProSearch.items import ProsearchItem

class SearchproSpider(scrapy.Spider):

    name = 'SearchPro'  # 爬虫名称
    allowed_domains = ['fz.people.com.cn']
    # start_urls = ['http://fz.people.com.cn/skygb/sk/index.php/Index/seach']
    page = 1

    # 指定检索关键词
    keywords = ['可持续', '互联网', '大数据', '能源']
    # 角标
    index = 0
    # 年份
    years = 2018

    # POST提交参数
    formdata = {
        'xmname': '',
        'xktype': '0',
        'xmtype': '0',
        'cglevel': '0',
        'cbdate ': '0',
        'cgxs': '0',
        'lxtime': '',
        'ssxt': '0',
        'zyzw': '0',
        'dwtype': '0',
        'jxdata': '0',
        'szdq': '0',
        'pznum': '',
        'cgname': '',
        'jxnum': '',
        'cbs': '',
        'xmleader': '',
        'hj': '',
        'gzdw': '',
        'zz': ''
    }

    # 参数提交的url
    url = "http://fz.people.com.cn/skygb/sk/index.php/Index/seach"

    def start_requests(self):
        """
        POST请求实现一般是重写start_requests函数，指定第一个关键词为默认检索关键词
        :return:
        """
        self.formdata['xmname'] = '可持续'
        self.formdata['lxtime'] = str(self.years)
        yield scrapy.FormRequest(
            url=self.url,
            formdata=self.formdata,
            callback=self.parse,
            meta={'formdata': self.formdata}
        )

    def parse(self, response):
        """
        解析数据
        :param response:
        :return:
        """
        if response.meta['formdata']:
            formdata = response.meta['formdata']

        # 每行数据所在节点
        try:
            node_list = response.xpath("//div[@class='jc_a']/table/*")[1:]
        except:
            print("关键词‘{}’无搜索结果!".format(formdata['xmname']))
        for node in node_list:
            # 提取数据
            item = ProsearchItem()
            # 关键词
            item['keyword'] = formdata['xmname']
            # 项目编号
            item['pronums'] = node.xpath('./td[1]/span/text()').extract_first()
            # 项目类别
            item['protype'] = node.xpath('./td[2]/span/text()').extract_first()
            # 学科类别
            item['subtype'] = node.xpath('./td[3]/span/text()').extract_first()
            # 项目名称
            item['proname'] = node.xpath('./td[4]/span/text()').extract_first()
            # 立项时间
            item['protime'] = node.xpath('./td[5]/span/text()').extract_first()
            # 负责人
            item['leaders'] = node.xpath('./td[6]/span/text()').extract_first()
            # 工作单位
            item['workloc'] = node.xpath('./td[8]/span/text()').extract_first()
            # 单位类别
            item['orgtype'] = node.xpath('./td[9]/span/text()').extract_first()
            # 所属省市
            item['provloc'] = node.xpath('./td[10]/span/text()').extract_first()
            # 所属系统
            item['systloc'] = node.xpath('./td[11]/span/text()').extract_first()
            yield item

        # 匹配下一页的数据
        if '下一页' in response.xpath("//div[@class='page clear']/a").extract():
            self.page += 1
            n_url = self.url + '?' + 'xmname={}&p={}'.format(formdata['xmname'], self.page)
            yield scrapy.Request(url=n_url, callback=self.parse, meta={'formdata': formdata})

        # 匹配其他年份的数据
        searcy_year = int(formdata['lxtime'])
        if not searcy_year <= 2014:
            searcy_year -= 1
            formdata['lxtime'] = str(searcy_year)
            print("检索关键词：{}!".format(formdata['xmname']))
            yield scrapy.FormRequest(
                    url=self.url,
                    formdata=formdata,
                    callback=self.parse,
                    meta={'formdata': formdata}
            )
        # 其他关键词搜索
        else:
            self.index += 1
            if not self.index > len(self.keywords)-1:
                keyword = self.keywords[self.index]
                print("更新检索关键词为：{}".format(keyword))

                formdata['xmname'] = keyword
                formdata['lxtime'] = str(self.years)

                yield scrapy.FormRequest(
                        url=self.url,
                        formdata=formdata,
                        callback=self.parse,
                        meta={'formdata': formdata}
                )
