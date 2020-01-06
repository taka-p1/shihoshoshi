from datetime import datetime
import math
from selenium import webdriver
import pandas as pd
import numpy as np
import logging

logging.basicConfig(filename='shihoshoshi.log', level=logging.INFO)
logger = logging.getLogger(__name__)

class Robot(object):

    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(driver_path)

    def calc_pages(self, url):
        logger.info({
            'action':'access to url',
            'url':url,
            'status':'run'
        })
        self.driver.get(url)
        logger.info({
            'action':'access to url',
            'url':url,
            'status':'success'
        })
        search_button =self.driver.find_element_by_xpath(
            '//*[@id="member"]/div[2]/div/ul/li[1]/input'
        )
        search_button.click()
        logger.info({
            'action':'click search button',
            'status':'success'
        })
        count_str = str(self.driver.find_element_by_xpath('//*[@id="search_hit"]/span').text)
        num_of_members = int(count_str.replace(',',''))
        num_of_pages = math.ceil(num_of_members/20)
        return num_of_pages

    def make_shihoshoshi_df(self, base_url):
        df_list = []
        pages = self.calc_pages(base_url)
        for count in range(pages):
            pageID = count + 1
            url = self.driver.current_url+f'&pageID={pageID}'
            logger.info({
                'action':'get table value',
                'status':'run',
                'url':url
            })
            dfs = pd.read_html(url, header=0)
            logger.info({
                'action':'get table value',
                'status':'success',
                'url':url
            })
            df_list.append(dfs[0])
        df = pd.concat(df_list)
        df.dropna(how='all', inplace=True)
        df = df.assign(No = df.No.astype(np.int64))
        return df


    def export_file(self, df, filename):
        now = datetime.now()
        filename = f'{filename}_{now:%Y%m%d}.csv'
        df = df.assign(No = df.No.astype(np.int64))
        logger.info({
            'action':'export csv',
            'status':'run',
            'filename':filename
        })
        df.to_csv(filename, index=False)
        logger.info({
            'action':'export csv',
            'status':'success',
            'filename':filename
        })

if __name__ == "__main__":
    Robot(None)
