#!/usr/bin/python
# coding: utf-8

import os
import sys
import codecs
import urllib
import urllib2
import simplejson

from urllib2 import urlopen
from urllib import urlencode

chinese_dict = {
    '操作系统': '作业系统',
    '计算机': '电脑',
    '源代码': '源始码',
    '文件': '档案',
    '工具栏': '工具列',
    '快捷键': '捷径键',
    '软件': '软体',
    '应用程序': '应用程式',
    '界面': '介面',
    '标签': '分页',
    '支持': '支援',
    '搜索': '搜寻',
    '文件夹': '资料夹',
    '导入': '汇入',
    '导出': '汇出',
    '智能': '智慧',
    '扩展': '附加元件',
    '插件': '外挂程式',
    '链接': '连结',
    '归档': '备存',
    '收件夹': '收件匣',
    '终端': '终端机',
    '窗口': '视窗',
    '高级': '进阶',
    '“': '「',
    '”': '」',
}

def get_splits(text, length=4500):
    '''
    Translate Api has a limit on length of text(4500 characters) that can be translated at once
    '''
    return (text[index:index+length] for index in xrange(0,len(text),length))

# The google translate API can be found here:
# http://code.google.com/apis/ajaxlanguage/documentation/#Examples
def translate(text):
    from_lang = "zh"
    to_lang = "zh-TW"
    langpair = '%s|%s' % (from_lang, to_lang)

    # OK, dirty hack, but works. ^_^
    text = 'OMG!'.join(text.split('\n'))

    base_url = 'http://ajax.googleapis.com/ajax/services/language/translate?'
    params = {'v': 1.0,
            'ie': 'UTF8',
            'q': text,
            'langpair': langpair}

    new_text = ''
    for splite in get_splits(text):
        params['q'] = splite
        data = urllib.urlencode(params)
        resp = simplejson.load(urllib.urlopen('%s' % (base_url), data=data))

        try:
            new_text += resp['responseData']['translatedText']
        except:
            pass

    # recover the word
    return '\n'.join(new_text.split('OMG!'))

if len(sys.argv) != 2:
    print 'Please follow by a file name'
    sys.exit(1)
else:
    orignal_data = open(sys.argv[1]).read()

    for k, v in chinese_dict.items():
        orignal_data = orignal_data.replace(k, v)

    new_data = translate(orignal_data)

    new_path = sys.argv[1] + '.new'
    new_file = codecs.open(new_path, 'w', 'utf-8')
    new_file.write(new_data)
    new_file.close()
