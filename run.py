"""importing all important libraries"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request
import time
import sys
import os
import getpass

"""instagram login"""
class instagramLog:
    def __init__(self):
        self.scroll_script = """function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        async function scroller() {
            var divTag = document.getElementsByClassName('isgrP');
            var d = divTag[0];
            var newHeight = 0;
            while (true){
                newHeight += 50;
                d.scrollTo(0, newHeight);
                await sleep(100);
                if (newHeight >= d.scrollHeight){
                    break;
                }
            }
        }
        scroller()"""
        self.options = Options()
        self.options.headless = True
        self.browser = webdriver.Chrome("chromedriver", chrome_options=self.options)
        self.browser.maximize_window()
        self.browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(1)

    """function to login on instagram"""
    def login (self, user, passw):
        wait = WebDriverWait(self.browser,120)
        username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        username.send_keys(user)
        password = self.browser.find_element_by_name("password")
        password.send_keys(passw)

        """enter login button"""
        loginbtn = self.browser.find_elements_by_tag_name("button")
        loginbtn[1].click()

    """function to download images from user account"""
    def download_photos(self,url,username):
        self.browser.get(url)
        images_list=[]
        oh = self.browser.execute_script("return document.body.scrollHeight")
        while True:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            soup=BeautifulSoup(self.browser.page_source,"html.parser")
            img=soup.find_all("img")
            for i in img:
                    try:
                        img_link=i.attrs['src']
                        images_list.append(img_link)
                    except:
                        pass

            time.sleep(3)

            """new height calculation"""
            nh = self.browser.execute_script("return document.body.scrollHeight")
            if nh == oh:
                break
            else:
                oh = nh


        img_unique_list=list(set(images_list))
        total_images=len(img_unique_list)
        if  total_images == 0 :
                   print("SORRY!!!! The given username account is not found :(")
                   self.browser.close()
                   sys.exit()
        work_dir=os.getcwd()
        path1=work_dir+"/"+'{}'.format("images")
        check=os.path.isdir(path1)
        if check==False:
            os.mkdir(path1)
        path2=path1+"/"+'{}'.format(username)
        try:
            os.mkdir(path2)
            os.chdir(path2)
            print("images will be download in {} folder".format(path2))
        except:
            os.chdir(path1)
            print("directory creation failed")
            print("images will store in {} folder".format(path1))

        print("Downolading start....")
        for j in range(total_images):
                   img_name=str(j)+'.jpg'
                   download=urllib.request.urlretrieve(img_unique_list[j],img_name)
                   print("{}".format(img_name))
        print("Process is successfully completed....")


"""main function"""
if __name__=="__main__":
    print("*************Login to your Instagram account*****************")
    uname = input("Enter username: ")
    try:
        password = getpass.getpass(prompt="Enter password : ")
    except Exception as e:
        print("Error:",e)
    insta = instagramLog()
    insta.login(uname, password)

    option=int(input("\n1.username\n2.hashtag\nEnter option:"))

    if option == 1:
               tag=input("\nEnter username: ")
               url="https://www.instagram.com/{}/".format(tag)
    elif option == 2:
               tag=input("\nEnter hashtag with #: ")
               tag=tag[1:]
               url="https://www.instagram.com/explore/tags/{}".format(tag)
    insta.download_photos(url,tag)
