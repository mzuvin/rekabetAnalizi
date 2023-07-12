#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
sys.getdefaultencoding()
import json as j
import webapp2
import urllib2

def newLine(text):
    text=text.replace('\n','')
    return text


def req2Html(url):
    a=urllib2.Request(url)
    a.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')
    a=urllib2.urlopen(a)
    sonuc=a.read()
    return sonuc

def wwwN11RegexLst():
    rgxlist=[]
    rgxIsim = r"<h1 class=\"proName\">\s+(.+)\s+<\/h1>"
    rgxUrunId = r"class=\"productId\" value=\"([0-9]+)\"\/>"
    rgxKategoriId = r"class=\"categoryId\" value=\"([0-9]+)\"\/>"
    rgxMagazaIsmi = r"main-seller-name\".+\">(.+)<\/a>"
    rgxResimler = r"data-full=\"(.+)\".data-zoom"
    rgxAyrinti = r"<div class=\"unf-info\" id=\"unf-info\">([\s.\S]+)<\/div>\n.+<div class=\"unf-white-section"
    rgxMemnuniyet = r"<span class=\"point\">(.+)</span>"
    rgxEskiFiyat = r"<del class=\"oldPrice\">(.+)</del>"
    rgxKargoZaman = r"<i class=\"cargoTime\">(.+)</i>"
    rgxFiyat = r"<ins content=\"(.+)\">(.+)<span content=\"(.+)\">TL</span></ins><span class=\"kdv\">KDV <br>DAHİL</span>"
    rgxKazanc = r"<span class=\"discTL\">(.+)</span>"
    rgxYuzdeIndirim= r"<span class=\"ratio\">(.+)</span>"
    rgxStokAdet = r"skuStock\".value=\"(.+)\""
    #rgxUrunGereklilik =  r"<div class=\"unf-prop-context\">([\s.\S]+)<p class=\"unf-prop-more\">"
    rgxUrunGereklilik = r"<div class=\"unf-prop-context\">([\s.\S]+)<div class=\"unf-white-section\""
    rgxlist.append(rgxIsim)
    rgxlist.append(rgxFiyat)
    rgxlist.append(rgxMagazaIsmi)
    rgxlist.append(rgxMemnuniyet)
    rgxlist.append(rgxResimler)
    rgxlist.append(rgxKargoZaman)
    rgxlist.append(rgxEskiFiyat)
    rgxlist.append(rgxYuzdeIndirim)
    rgxlist.append(rgxAyrinti)
    rgxlist.append(rgxKazanc)
    rgxlist.append(rgxKategoriId)
    rgxlist.append(rgxUrunId)
    rgxlist.append(rgxStokAdet)
    rgxlist.append(rgxUrunGereklilik)
    return rgxlist


def n11RegexLst():
    rgxlist=[]
    #Regex Listem
    rgxIsim = r"\"name\": \"(.+)\",\n.+\"description"
    rgxFiyat = r"<ins content=\"(.+)\">(.+)<span content=\"(.+)\">TL</span></ins><span class=\"kdv\">KDV <br>DAHİL</span>"
    rgxMagazaIsmi = r"<h3>.+<a href=\"(.+)\" title=\"(.+)\">(.+)</a>"
    rgxMemnuniyet = r"<span class=\"point\">(.+)</span>"
    rgxResimler = r"\"@type\":.+\"ImageObject\",\n.+\"contentUrl\":.+\"(.+)\""
    rgxKargoZaman = r"<i class=\"cargoTime\">(.+)</i>"
    rgxEskiFiyat = r"<del class=\"oldPrice\">(.+)</del>"
    rgxYuzdeIndirim= r"<span class=\"ratio\">(.+)</span>"
    rgxKazanc = r"<span class=\"discTL\">(.+)</span>"
    rgxAyrinti = r"<h4 class=\"title\">Ayrıntılar<\/h4>((\n.+)+)"
    rgxUrunGereklilik=r"(<section class=\"tabPanelItem features\">\n.+<h4>Ürün Özellikleri<\/h4>(\n+.+)+<h4 class=\"title\">Ayrıntılar<\/h4>)"
    rgxUrunId=r"<input type=\"hidden\" class=\"productId\" value=\"([0-9]+)\"\/>"
    rgxKategoriId=r"<input type=\"hidden\" class=\"categoryId\" value=\"([0-9]+)\"\/>"
    rgxStokAdet = r"stockCount\".value=\"([0-9]+)\"\/>"
    #listeye ekleniyor.
    rgxlist.append(rgxIsim)
    rgxlist.append(rgxFiyat)
    rgxlist.append(rgxMagazaIsmi)
    rgxlist.append(rgxMemnuniyet)
    rgxlist.append(rgxResimler)
    rgxlist.append(rgxKargoZaman)
    rgxlist.append(rgxEskiFiyat)
    rgxlist.append(rgxYuzdeIndirim)
    rgxlist.append(rgxAyrinti)
    rgxlist.append(rgxKazanc)
    rgxlist.append(rgxKategoriId)
    rgxlist.append(rgxUrunId)
    rgxlist.append(rgxStokAdet)
    rgxlist.append(rgxUrunGereklilik)
    return rgxlist


def hpsBrdRegexLst():
    rgxlist=[]
    rgxFiyat = r"product_prices\":\[\"([0-9.]+)\"\]"
    rgxEskiFiyat = r"hasDiscountPrice}\">(.+)<\/del>"
    rgxIsim= r"product_names\":\[\"(.+)\"\],\"product_category"
    rgxStokKod = r"product_skus\":\[\"(.+)\"\],\"product_ids\""
    rgxResimler = r"data-img=\"(.+)\"|data-src=\"(.+)\""
    rgxUrunBilgi = r"<div id=\"tabProductDesc\"([^\n]*\n+)+<span id=\"captchaScriptCont\"><\/span>"
    #rgxDigerSaticiFiyat = r"<div class=\"last-price hb-pl-cn\">([^\n]*\n+)+<!--\/ko-->"
    #rgxAyrinti= r"<table class=\"data-list tech-spec\">((\n.+)+)<\/tr>"
    ##rgxAyrinti = r"<div id=\"tabProductDesc\" class=\"list-item-detail product-detail box-container\">((\n+.+)+)<div id=\"ctl00"
    ###rgxAyrinti = r"<div id=\"tabProductDesc\" class=\"list-item-detail product-detail box-container\">((\n+.+)+)<span id=\"captchaScriptCont\"><\/span>"
    ####rgxAyrinti = r"<div id=\"tabProductDesc\" class=\"list-item-detail product-detail box-container\">([\s\S]+)<span id=\"captchaScriptCont\"><\/span>"
    #regex Son
    rgxAyrinti = r"description\":\"(.+)\",\"hasExtraFee\":false,"
    rgxUrunId = r"<input type=\"hidden\"\s+name=\"productId\"\s+value=\"([A-Za-z0-9]+)\""
    rgxKategoriId = r"product_category_ids\":\[\"([0-9]+)\"\]"
    rgxMemnuniyet = r"<span itemprop=\"ratingValue\" content=\"([0-9,]+)\"><\/span>" #birinci eleman cekilecek.
    rgxStokAdet = r"dealOfTheDayStock\(\)\">([0-9]+)"
    rgxKazanc = r""
    rgxYuzdeIndirim = r"<span data-bind=\"markupText: 'discountRate'\">([0-9]+)<\/span>"
    rgxMagazaIsmi = r"merchant_names\":\[\"(.+)\"\],\"merchant"
    rgxRekabet = r"merchantName\":\"([A-Za-zığüşöçĞÜŞİÖÇ ]+)\",\"merchantPageUrl\":\"[A-Za-z/-]+\",\"dispatchTime\":[0-9]+,\"priceText\":\"([0-9,]+)"
    #rgxUrunGereklilik = r""

    #regex listeye ekleniyor.
    rgxlist.append(rgxIsim)
    rgxlist.append(rgxFiyat)
    rgxlist.append(rgxMagazaIsmi)
    rgxlist.append(rgxMemnuniyet)
    rgxlist.append(rgxResimler)
    #rgxlist.append(rgxKargoZaman)#kargo zamnı sürekli yenileniyor -
    rgxlist.append(rgxEskiFiyat)
    rgxlist.append(rgxYuzdeIndirim)
    rgxlist.append(rgxAyrinti)
    #rgxlist.append(rgxKazanc)
    rgxlist.append(rgxKategoriId)
    rgxlist.append(rgxUrunId)
    rgxlist.append(rgxStokAdet)
    #rgxlist.append(rgxUrunGereklilik)
    rgxlist.append(rgxRekabet)
    return rgxlist


def hepsiBurada(url):
    html=req2Html(url)
    json={}
    isimler=["isim","fiyat","magazaismi","memnuniyet","resimler","eskifiyat","yuzdeindirim","ayrinti","kategoriid","urunid","stokadet","rekabet"]#,"urungereklilik"]
    for i in isimler:
        json[i]=""
    for i, regex in enumerate(hpsBrdRegexLst()):
        data=re.findall(regex,html)

        #print isimler[i]+"  "+str(data)
        for k, val in enumerate(data):
            #print isimler[i]
            if isimler[i]=="magazaismi":
                json[isimler[i]]=val.decode('utf8')
            elif isimler[i]=="fiyat":
                json[isimler[i]]=val
            elif isimler[i]=="ayrinti":
                json[isimler[i]]=val.decode('utf8')
            elif isimler[i]=="rekabet":
                if k==0:
                    json[isimler[i]]={}
                json[isimler[i]][val[0]]=val[1]

            elif isimler[i]=="memnuniyet":
                if k==0:
                    json[isimler[i]]=str(val)
            elif isimler[i]=="urunozellikleri":
                if k==0:
                    json[isimler[i]]=[]
                json[isimler[i]]=val[0].decode('utf8')
            elif isimler[i]=='resimler':
                if k==0:
                    json[isimler[i]]=[]
                """    
                json[isimler[i]]={}
                json[isimler[i]]['1500']=[]
                json[isimler[i]]['500']=[]
                json[isimler[i]]['80']=[]
                """
                #if val[1].find('/s/28/1500/')>-1:
                #    json[isimler[i]]['1500'].append(val[1])
                if val[1].find('/500/')>-1:
                    json[isimler[i]].append(val[1])

                #if val[1].find('/s/28/80/')>-1:
                #    json[isimler[i]]['80'].append(val[1])
                    #json[isimler[i]].append(val)
            else:
                json[isimler[i]]=str(val)#decode('utf8'))
    return str(j.dumps(json))


def urunAyrintiWwwN11(text):
    urun=[]
    value={}
    rgxLabel = r"unf-prop-list-title\">(.+)<\/p>"
    rgxData=r"unf-prop-list-prop\">(.+)<\/p>"
    data=re.findall(rgxLabel,text)
    for i,val in enumerate(data):
        #print str(i)+"label"+str(val)
        #urun[val]=[]
        value[i]=val
    data=re.findall(rgxData,text)
    for i,val in enumerate(data):
        #urun[value[i]]=val
        #print "data"+str(val[1])
        dizi={}
        dizi['isim']=value[i]
        dizi['ozellik']=val
        #urun[value[i]]=val[1]
        urun.append(dizi)
    return urun

def urunAyrintiN11(text):
    urun=[]
    value={}
    rgxLabel = r"<span class=\"label\">([A-Za-zığüşöçĞÜŞİÖÇ 0-9,-;!'^+%&/()=?_#]+)<\/span>"
    rgxData=r"<span +(class=\"data\" +| +)>([A-Za-zığüşöçĞÜŞİÖÇ 0-9,-;!'^+%&/()=?_#]+)<\/span>"
    data=re.findall(rgxLabel,text)
    for i,val in enumerate(data):
        #print str(i)+"label"+str(val)
        #urun[val]=[]
        value[i]=val
    data=re.findall(rgxData,text)
    for i,val in enumerate(data):
        dizi={}
        dizi['isim']=value[i]
        dizi['ozellik']=val[1]
        #urun[value[i]]=val[1]
        urun.append(dizi)
        #print "data"+str(val[1])
    return urun


def n11(url,regexList,regexIsim=""):#sadece www olan sayfalarda degisiklik yap.
    html=req2Html(url)
    json={}
    isimler=["isim","fiyat","magazaismi","memnuniyet","resimler","kargo","eskifiyat","yuzdeindirim","ayrinti","kazanc","kategoriid","urunid","stokadet","urungereklilik"]
    for i in isimler:
        json[i]=""
    for i, regex in enumerate(regexList):
        data=re.findall(regex,html)
        for k, val in enumerate(data):
            if isimler[i]=="magazaismi":
                if regexIsim=='www':#regexler karismasin diye
                    json[isimler[i]]=val.decode('utf8')
                else:
                    json[isimler[i]]=val[1].decode('utf8')
            elif isimler[i]=="ayrinti":
                if regexIsim=='www':
                    json[isimler[i]]=val.decode('utf8')
                else:
                    json[isimler[i]]=newLine(val[0].decode('utf8'))
            elif isimler[i]=="fiyat":
                    json[isimler[i]]=val[0].decode('utf8')
            elif isimler[i]=='urungereklilik':
                if regexIsim=='www':
                    json[isimler[i]]=[]
                    json[isimler[i]]=urunAyrintiWwwN11(val)
                else:
                    #json[isimler[i]]=[]
                    json[isimler[i]]=urunAyrintiN11(val[0])
            elif isimler[i]=='resimler':
                if k==0:
                    json[isimler[i]]=[]
                json[isimler[i]].append(val)
            else:
                json[isimler[i]]=val.decode('utf8')
    return str(j.dumps(json))


class Anasayfa(webapp2.RequestHandler):
    def get(self):
        self.response.write("SALI PAZAR ENTEGRASYON")

class RekabetHandler(webapp2.RequestHandler):
    def get(self):
        id = self.request.get('id')
        isim = self.request.get('isim')

        url="https://www.hepsiburada.com/a-p-"+str(id)
        html=req2Html(url)
        regexList=[]
        rgxRekabet = r"merchantName\":\"([A-Za-zığüşöçĞÜŞİÖÇ +_!'#$%&/\(\)=\]\[]+)\",\"merchantPageUrl\":(\"[A-Za-z/-]+\"|null),\"dispatchTime\":[0-9]+,\"priceText\":\"([0-9.,]+)"
        regexList.append(rgxRekabet)

        json={}
        isimler=["magazalar"]
        for i in isimler:
            json[i]=""
        for i, regex in enumerate(regexList):
            data=re.findall(regex,html)
            #print "regex data--------------"
            #print data
            for k, val in enumerate(data):
                if i==0:#fiyat regexlist sırası
                    if k==0:#ilk seferde obje oluşturmak için 
                        json[isimler[0]]=[]
                    dizi={}
                    dizi['isim']=val[0]
                    #print "-----------------------"
                    #print val[2]
                    dizi['fiyat']=float(val[2].replace(".","").replace(",","."))
                    #print "-----------------------"
                    #print dizi
                    json[isimler[0]].append(dizi)

        json1=sorted(json['magazalar'], key=lambda k: k['fiyat'])
        json={}
        json['magazalar']=json1
        self.response.write(j.dumps(json))



class MagazaHandler(webapp2.RequestHandler):
    def get(self):
        isim = self.request.get('isim')
        sayfa = self.request.get('s')
        if sayfa=="":
            sayfa=1
        if isim=="":
            self.response.write('magazaismi giriniz.')
            return
        else:
            if int(sayfa)>1:
                url="https://www.hepsiburada.com/magaza/"+str(isim)+"?sayfa="+str(sayfa)
            else:
                url="https://www.hepsiburada.com/magaza/"+str(isim)
            html=req2Html(url)
            regexList=[]
            regex=r"([/A-Za-z0-9-]+\?magaza=[A-Za-z0-9]+)\" data-sku=\"(.+)\""
            #data=re.findall(regex,html)
            regex2 = r"(class=\"page-[0-9]+)"
            regex3= r"<span class=\"price product-price\">(.+) TL<\/span>"
            rgxIsim = r"<h3 class=\"product-title title\" title=\"(.+)\">"
            regexList.append(regex)
            regexList.append(regex2)
            regexList.append(regex3)
            regexList.append(rgxIsim)
            #pageSize = re.findall(regex2,html)
            json={}
            isimler=["isim","url","sayfasayisi","sayfa","idler","fiyatlar","isimler"]
            for i in isimler:
                json[i]=""
            for i, regex in enumerate(regexList):
                data=re.findall(regex,html)
                #print i
                #print data
                if i==2:
                    json[isimler[5]]=data
                for k, val in enumerate(data):
                    if i==0:
                        if k==0:#tek seferlik dizi oluştur.
                            json[isimler[1]]=[]
                            json[isimler[4]]=[]
                        json[isimler[1]].append(val[0].decode('utf8'))
                        json[isimler[4]].append(val[1].decode('utf8'))
                    if i==1:
                        #sayfa sayısı uzunlugu artı bir
                        json[isimler[2]]=str(int(k)+1)
                    if i==3:
                        if k==0:
                            json[isimler[6]]=[]
                        json[isimler[6]].append(val.replace('&quot','').decode('utf8'))


            json[isimler[3]]=sayfa
            json[isimler[0]]=isim
            self.response.write(j.dumps(json))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        self.response.headers['Content-Type'] = 'application/json'
        if url.find('n11.com')>-1:
            if url.find('urun.n11.com')>-1:
                self.response.write(n11(url,n11RegexLst()))
            if url.find('www.n11.com')>-1:
                self.response.write(n11(url,wwwN11RegexLst(),'www'))
            if url.find('m.n11.com/urun/')>-1:
                url=url.replace('m.n11.com','www.n11.com')
                self.response.write(n11(url,wwwN11RegexLst(),'www'))
            elif url.find('m.n11.com')>-1:
                url=url.replace('m.n11.com','urun.n11.com')
                self.response.write(n11(url,n11RegexLst()))
        elif url.find('hepsiburada.com')>-1:
            self.response.write(hepsiBurada(url))
        else:
            self.response.write("{'hata':'hata mesaji'}")


APP = webapp2.WSGIApplication([
        ('/', Anasayfa),
        (r'/salipazar/', MainHandler),
        (r'/magaza/', MagazaHandler),
        (r'/rekabet/',RekabetHandler)
], debug=True)
