#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-11 17:37:28
# Project: hospital

from pyspider.libs.base_handler import *
import time

class Handler(BaseHandler):
    crawl_config = {
        'headers':{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'},
    }

    @every(minutes=24 * 60)
    def on_start(self):
        template = 'https://www.91160.com/search/index/ulvl-0/ht-0/disease_id-0/utype-0/aid-7/isopen-1/p-{}/ysort-1/cid-5.html'
        page = 1
        self.crawl(template.format(page), callback=self.index_page, save={'template':template,'page':page}, validate_cert=False)

    def index_page(self, response):
        # get data
        for item in response.doc('.search_item').items():
            name = item('h2 a').text()
            grade = item('h2 span').text().strip().strip(u'［').strip(u'］')
            link = item('h2 a').attr.href
            nums = item('.right_mun strong').text()
            items = [item for item in item('.h_info p').items()]
            addr = items[1].text().strip(u'地址：')
            tel = items[2].text().strip(u'电话：')
            self.send_message(self.project_name, {
                'name':name,
                'grade':grade,
                'link':link,
                'nums':nums,
                'addr':addr,
                'tel':tel,
            }, url= '%s#%s' % (response.url, name))
        # next page
        template = response.save['template']
        page = response.save['page'] + 1
        if page < 3:
            self.crawl(template.format(page), callback=self.index_page, save={'template':template,'page':page}, validate_cert=False)

    def on_message(self, project, msg):
        return msg