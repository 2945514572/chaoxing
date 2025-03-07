import re
import requests

def getText(url):
    try:
        kv = {'user-agent': 'Mozilla/5.0',
              'cookie': '_m_h5_tk=2c21cc81621dc79ac44897dc915feeea_1691599805662; _m_h5_tk_enc=04435c12192c1aadb3b8764f9016eb58; t=48b2e347d5bb40db94c9464c66a81fff; _tb_token_=5b9659ef5e7ae; _samesite_flag_=true; cookie2=1bf4797578cd24659ffe664904e59fda; cna=ejeKHHtlpCoCASeQn14Pdsg9; xlly_s=1; sgcookie=E100%2BUJvVKKP5X8mHRNzxi2N6zXcQBDPkxR14LK4GKnuk6IS90vpttXT45OW7GXNeecJJc1y9dIIGKQq61VulJW3Dzbr5knbXeJDx53TMAdTqav64fMKLT6ykIXpI4U%2B7i%2Fu; unb=2201427454458; uc1=pas=0&cookie21=VFC%2FuZ9ainBZ&existShop=false&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie14=Uoe9bF%2FE%2B0hibA%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&nk2=F5RMECpHcMLuGV4%3D&vt3=F8dCsGd5wyAcxWLWbxc%3D&id2=UUphy%2FZ4hEXS1oCEGg%3D%3D; csg=1703e32d; lgc=tb995051899; cancelledSubSites=empty; cookie17=UUphy%2FZ4hEXS1oCEGg%3D%3D; dnk=tb995051899; skt=024b5995ad5d9742; existShop=MTY5MTU5MjIxMg%3D%3D; uc4=nk4=0%40FY4HVZjyOueZo3Ld4Isu90XqXbYE5w%3D%3D&id4=0%40U2grEJGHt4gsB8FGNp8GJiurTrbCstVY; tracknick=tb995051899; _cc_=V32FPkk%2Fhw%3D%3D; _l_g_=Ug%3D%3D; sg=98b; _nk_=tb995051899; cookie1=VADZ6bwueiXOBR8bDBoqc70v59E9eeVoiWtM%2FqHncSI%3D; JSESSIONID=B257FA02E73F51AC4C534C7AA2B7F27B; l=fBTfQR4VN0f5e-PSBO5Cnurza77OuIdb8sPzaNbMiIEGa6ghTngG3NC6nlN27dtjgTfD6etrGJos3depJ74g7xGjL77kRs5mpup9-dIpQp5..; isg=BHZ2mUS2DhKGhPr2tAK9AFLOx6x4l7rRcIToNOBe99l4Ixe9SCep4v2RO_9Pi7Lp; tfstk=d9ow3OmULhKa_1uTLzZqLHUwdWrTmudWbmNbnxD0C5Vg1x200XcXB5MD6jo4tx36BrOO3OnEais66FHc0oZDNQtWVAH_DoA5KOAUXurzWB9CO3MtBoFrHXAWV-PWQMI93v8ReQz9vYPnbEg3KROJzWIcmcxY775QOJeIYJUaZy2PQgfYKoenDV5cuP2LL79eL2p0RJ1..'}

        r=requests.get(url,headers=kv,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        # print(r.text[:500])
        return r.text

    except:
        return ""

def paresrPage(ilt,html):
    try:
        plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt=re.findall(r'\"raw_title"\:\".*?\"',html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price,title])


    except:
        print("")

def printGoodsList(ilt):
    tplt="{:4}\t{:8}\t{:16}"
    print(tplt.format("序号","价格","商品名称"))
    count=0
    for g in ilt:
        count =count+1
        print(tplt.format(count,g[0],g[1]))
    # print(ilt)



def main():
    goods='手机'
    depth=3
    start_url='https://s.taobao.com/search?q='+goods
    infoList=[]

    for i in range (depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=getText(url)
            paresrPage(infoList,html)
        except:
            continue
    printGoodsList(infoList)
    # print(html[:500])
    # print(plt)
main()