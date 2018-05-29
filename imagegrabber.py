import bs4
import requests
import uuid
import os
import argparse
from multiprocessing.dummy import  Pool as ThreadPool

uri= None
tldn = None
imagepath = None
urls = []



def download_images(each_link):
    try:
        print("Downloading: ",each_link)
        pget = requests.get(each_link)
        pget.raise_for_status()
        if each_link.endswith("jpeg" or "jpg"):
            extension = "jpeg"
        elif each_link.endswith("png"):
            extension = "png"
        elif each_link.endswith("gif"):
            extension = "gif"
        else:
            extension = "jpeg"

        imagefile = open(os.path.join(imagepath, "%s.%s"% (uuid.uuid4().hex,extension)), 'wb')
        for chunk in pget.iter_content(10000):
            imagefile.write(chunk)
        imagefile.close()
    except Exception as e:
        print(e)


def main():
    if not os.path.exists(imagepath):
        os.mkdir(imagepath)

    res = requests.get(uri)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    for link in soup.find_all('img'):
        link = str(link).lstrip('<img src=\"').rstrip("/>\"")
        link = link.replace("t_",'')
        link = url + link
        urls.append(link)
    pool = ThreadPool(4)
    pool.map(download_images,urls)
    pool.close()
    pool.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("URL",help="Top level URL you want to scrape images from")
    parser.add_argument("URI",help="The URI you want to scrape iamges form")
    parser.add_argument("local_path",help="The location on disk you want to save images to")
    args = parser.parse_args()
    url = args.URL
    uri = args.URI
    imagepath = args.local_path
    main()
