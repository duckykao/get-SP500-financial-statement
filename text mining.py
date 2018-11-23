import requests as req
from bs4 import BeautifulSoup
import os
import pdfkit
import xlrd



# 你需要去下載 BeautifulSoup 跟 pdfkit (pdfkit 比較難下載)

"""
companies = {}
companies_path = "C:\\Users\\user\\Downloads\\SP500_non_fin_firms_2003.xlsx" 

open_excel = xlrd.open_workbook(companies_path)
com_name = open_excel.sheet_by_index(0)
for index in range(len(com_name.col(8))):
    companies[index] = com_name.cell_value(index,8)

del companies[0]
"""  
def DOWNLOAD_PDF(company_name):
    
    URL = "https://www.sec.gov"
    url = URL + "/cgi-bin/browse-edgar?action=getcompany&CIK=%s&type=10-K&dateb=&owner=exclude&count=20" % (company_name) 
    
    res = req.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    article = soup.select("td a")
    #print(article)

    path = {}
    num = 0

    for i in article:                  #讀取歷年10-K網站連結
        #print(URL + i.get('href'))
        path[num] = i.get('href')
        num = num + 1

    for r in range(len(path)):
        k = path[r].split("/")
        #print(k)
        if k[1] == 'cgi-bin':          #刪除裡面為 Interactive的連結 
            del path[r]
        else:
            path[r] = URL + path[r]

    path_10_K = {}   #每一個10-K 網站連結
    path_num = 0
    for t in path:
        #print(path[t])
        res2 = req.get(path[t])
        soup2 = BeautifulSoup(res2.text, "html.parser")
        article2 = soup2.select("td a")
        for ii in article2:
            path_10_K[path_num] = URL + ii.get('href')   #讀取10-k
            #print(path_10_K[path_num])
            path_num = path_num + 1
            break

    save_path = os.path.join("D:\\EDGAR\\",company_name+"\\")  # "D:\\EDGAR\\" 改成你想要的儲存的路徑
    if not os.path.exists(save_path):    # 查看此公司的資料夾是否存在 
        os.makedirs(save_path)           #沒有就建造一個
        
    print("============== Start Saving ================")
    
    for html_dir in range(len(path_10_K)-2):
        name = path_10_K[html_dir].split("/")[-1].split('.')[0]
        pdfkit.from_url(path_10_K[html_dir],save_path+name+'.pdf')   #將html轉成PDF
        print(html_dir)
        
    print("Done")


"""
for com in companies:
    
    DOWNLOAD_PDF(companies[com])
"""
DOWNLOAD_PDF("0001637459")






