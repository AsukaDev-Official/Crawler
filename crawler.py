#!/usr/bin/env
#author : Tegar Dev
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

colorama.init()
hijau = colorama.Fore.GREEN
abu = colorama.Fore.LIGHTBLACK_EX
merah = colorama.Fore.RED
reset = colorama.Fore.RESET

internal_urls = set()
external_urls = set()

logo = f"""
       _                         ╭━━━╮         ╭╮
       \`*-.                     ┃╭━╮┃         ┃┃
        )  _`-.                  ┃┃ ╰╋━┳━━┳╮╭╮╭┫┃
       .  : `. .                 ┃┃ ╭┫╭┫╭╮┃╰╯╰╯┃┃
       : _   '  \                ┃╰━╯┃┃┃╭╮┣╮╭╮╭┫╰╮
       ; {merah}*{reset}` _.   `*-._           ╰━━━┻╯╰╯╰╯╰╯╰╯╰━╯
       `-.-'          `-.       
         ;       `       `.          Web Crawler
         :.       .        \    
         . \  .   :   .-'   .     Author : Tegar Dev
         '  `+.;  ;  '      :   
         :  '  |    ;       ;-.  -[AsukaDev Official]-
         ; '   : :`-:     _.`* ;
{hijau}[{merah}404{hijau}]{reset} .*' /  .*' ; .*`- +'  `*' 
      `*-*   `*-*  `*-*'
"""

def benar(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def ambil_semua_link(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue

        href = urljoin(url, href)

        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

        if not benar(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                print(f"{abu}[!] External link: {href}{reset}")
                external_urls.add(href)
            continue
            print(f"{hijau}[*] Internal link: {href}{reset}")
            urls.add(href)
            internal_urls.add(href)
    return urls


total_urls_visited = 0


def crawl(url, max_urls=50):
    global total_urls_visited
    total_urls_visited += 1
    links = ambil_semua_link(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


if __name__ == "__main__":
    print(logo)
    website = input("Enter URL : ")
    crawl(website)
    print("[+] Total External links:", len(external_urls))
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total:", len(external_urls) + len(internal_urls))
