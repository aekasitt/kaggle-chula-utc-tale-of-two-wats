#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2019-2020 All rights reserved.
# FILENAME:  scrape.py
# VERSION: 	 1.0
# CREATED: 	 2020-05-19 14:53
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
import asyncio
from argparse import ArgumentParser
from io import BytesIO
from os import path, makedirs
from pathlib import Path
from time import sleep
### Third-Party Packages ###
import requests
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
### Local Modules ###
from helpers.logger import Logger
from helpers.pickler import Pickler

def scrollToEnd(wd:webdriver, loops:int=1, interval:int=1):
  try:
    for _ in range(loops):
      wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
      sleep(interval)
  except JavascriptException:
    pass

def persist_image(target_folder:str, url:str, img_name:str, logger:Logger):
  try:
    image_content = requests.get(url).content
    image_file = BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    file_path = path.join(target_folder, f'{img_name}.png')
    with open(file_path, 'wb') as f:
      image.save(f, 'PNG', quality=100)
    logger.infoSuccess(f'SUCCESS - saved {url} - as {file_path}')
  except Exception as e:
    logger.infoDanger(f'ERROR - Cound now download {url} - {e}')

def scrape():
  ### Parse Arguments ###
  parser = ArgumentParser(description='Kaggle Competition Image Scraper by @aekasitt')
  parser.add_argument('search_term', type=str, \
      help='The search term to query using Google Images')
  parser.add_argument('target_folder', type=str, \
      help='Define the target folder to save the images queried to.')
  parser.add_argument('--amount', '-n', type=int, \
      help='The amount of images to fetch', default=200)
  args = parser.parse_args()
  ### Initiate Logger Instance ###
  logger = Logger.get_instance('scraper')
  logger.info(args)
  target_folder = path.join(args.target_folder)
  name_idx = 0
  if not path.exists(target_folder):
    makedirs(target_folder)
  else:
    images_saved = Path(target_folder).glob('*.png')
    name_idx = len(list(images_saved)) + 1
    del images_saved
  wd = webdriver.Firefox(executable_path='./geckodriver')
  search_url = 'https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img'.format(q=args.search_term)
  wd.get(search_url)
  image_count = 0
  img_urls = set()
  results_start = 0
  interval_between_interactions = 1 # second
  while image_count < args.amount:
    scrollToEnd(wd)
    thumbnail_results = wd.find_elements_by_css_selector('img.rg_i')
    number_results = len(thumbnail_results)
    logger.info(f'Found: {number_results} search results. Extracting links from {results_start} to {number_results}')
    for img in thumbnail_results[results_start:number_results]:
      try:
        img.click()
        sleep(interval_between_interactions)
      except Exception:
        continue
      actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
      for actual_image in actual_images:
        if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
          img_urls.add(actual_image.get_attribute('src'))
      image_count = len(img_urls)
      
      if len(img_urls) >= args.amount:
        logger.info(f'Found {image_count} image links, done!')
        break
      else:
        pass # TODO
      results_start = len(thumbnail_results)
  wd.quit()
  for img_url in img_urls:
    img_name = f'{args.search_term.split(" ")[-1]}{name_idx}'
    print(f'Search-Term: {args.search_term}')
    print(f'Image-Name: {img_name}')
    persist_image(args.target_folder, img_url, img_name, logger)
    name_idx += 1
  Logger.release_instance()

if __name__ == '__main__':
  scrape()