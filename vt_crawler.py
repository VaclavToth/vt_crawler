# by Vašek Toth on Aug 27 2022

# We need just the necessary libraries
import time
import sys
import requests

# Default values - play with them, if you want more proper testing
DEFAULT_START_PAGE = "https://seznam.cz"
DEFAULT_TIMEOUT = 0.5
DEFAULT_MAX_PAGES = 10
MAX_TIMEOUT = 2
MAX_PAGES_LIMIT = 50
SHOW_OTHERS = False

# I also need a list for found URLs/links (difference described below)
url_list = []
links_list = []
cleaned_links_list = []
other_links_list = []
crawled_urls = []

# Main function
def crawler():

    # Function for response of URL
    def load_page(url):
        try:
            response = requests.get(url)
            return response.ok
        except ValueError:
            return "fail"

    # Function - If last character is slash then create a URL without it
    def get_rid_of_slash(string):
        if string[-1] == "/":
            string = string[:-1]

    # IF no argument is specified, write a info
    if len(sys.argv) == 1:
        print(
            "Welcome to VT crawler. If you want to proceed, you need to pass first agrument"
        )
        print("That could be any URL or you can just type 'test'")
        print("Also second (optional) parameter is TIMEOUT ")
        print(
            f"default {DEFAULT_TIMEOUT}s between iteration of webpages, {MAX_TIMEOUT}s max"
        )
        print("and third (optional) is maximum pages crawled")
        print(f"(default {DEFAULT_MAX_PAGES}, max {MAX_PAGES_LIMIT})")
        sys.exit()

    # Only required input is the first webpage I would like to crawl or user can just type "test"
    if sys.argv[1] == "test":
        start_page = DEFAULT_START_PAGE
    else:
        input_page = sys.argv[1]
        start_url_response = load_page(input_page)
        if start_url_response:
            if start_url_response == "fail":
                # Maybe user just forgot to pass http
                input_page = "http://" + input_page
                start_url_response = load_page(input_page)
                if start_url_response is not True:
                    print(f"Looks like that '{input_page}' is not a proper URL :-/")
                    sys.exit()
        else:
            print(f"Looks like that {input_page} does not work :-/")
            sys.exit()

        start_page = input_page

    # Second optional arguments is timeout
    if len(sys.argv) > 2:
        try:
            timeout = float(sys.argv[2])
            timeout = min(timeout, MAX_TIMEOUT)

        except ValueError:
            print("Timeout argument is not a number")
            sys.exit()
    else:
        timeout = DEFAULT_TIMEOUT

    # Third is iteration limit for crawling pages
    if len(sys.argv) > 3:
        try:
            max_pages = int(sys.argv[3])
            max_pages = min(max_pages, max_pages)

        except ValueError:
            print("Max webpages argument is not a whole number")
            sys.exit()
    else:
        max_pages = DEFAULT_MAX_PAGES

    # Lets add start page to url_list for crawling, so it is simplier to do a loop
    url_list.append(start_page)

    print(
        f"Crawling started on page {start_page} with {timeout}s minimal timeout between requests"
    )
    print(f"and will iterate up to {max_pages} webpages")
    print("")

    # Main loop for every url that I want to crawl
    for i in range(0, max_pages):

        if len(url_list) == 0:
            break

        get_rid_of_slash(url_list[0])

        current_url = url_list[0]
        url_list.pop(0)

        if current_url in crawled_urls:
            continue

        get_rid_of_slash(current_url)
        crawled_urls.append(current_url)

        # I need to see HTML content of the page
        crawling_page_resposnse = requests.get(current_url)

        start = time.time()

        # It is possible that page was redirected, in this case we want all page it went through
        if crawling_page_resposnse.history:
            for resp in crawling_page_resposnse.history:
                if resp.url not in crawled_urls:
                    crawled_urls.append(resp.url)

        # proceed only if page loaded succesfully
        if not crawling_page_resposnse.ok:
            continue

        crawling_page = crawling_page_resposnse.content

        # Now I need to parse the webpage, so I can recognize a links.
        # The most straightforward method for this would be a Beautiful Soup library
        # but for this simple case lets use native Python

        # So I need the whole webpage as the string
        crawling_str = str(crawling_page)

        while len(crawling_str) > 0:
            # I need to find first a <a tag
            a_tag_index = 0
            a_tag_index = crawling_str.find("<a ")

            # If there is not any, lets end the loop
            if a_tag_index == -1:
                break

            # Whatever was before this tag, I don't need anymore
            crawling_str = crawling_str[a_tag_index:]

            # Letr find a link in href atr.
            href_index = crawling_str.find('href="')

            # Now lets start with actual Link. I also want to get rid of quatation marks
            crawling_str = crawling_str[href_index + len('href="'):]

            # The atribute always ends with quatation marks
            end_href_index = crawling_str.find('"')

            # And now we have parsed our link (always in lcase)
            parsed_link = crawling_str[:end_href_index].lower()
            # But I only want a unique ones
            if parsed_link not in links_list:
                links_list.append(parsed_link)

            # and we can work with the rest of code and repeat the loop
            crawling_str = crawling_str[end_href_index:]

        # Now we have a lots of unique content of "href" atributes of <a> tags
        # But not all of them are usable and even less of them are URLs

        # First lets get rid of things that are not a proper link
        for link in links_list:
            # hastag as its a class selector
            if "#" not in link:
                # js reset page
                if "javascript:void(0)" not in link:
                    # html reset page
                    if not link == "/":
                        # if there are any html tag - failed parsing of href atr
                        if ("<" or ">") not in link:
                            cleaned_links_list.append(link)

        # URLs in our case - webpages can only be in two formats: "http://" or "https://"
        # other URLs such as FTPs are useless right now
        for link in cleaned_links_list:
            if "http://" in link or "https://" in link:
                url_list.append(link)
            else:
                # We don't want to other links be foregotten
                # because they can be used for local onsite crawling
                other_links_list.append(link)

        # If it took less time than timeout, wait for the rest of time
        print(f"{i+1}. '{current_url}' just has been crawled")
        end = time.time()
        p_time = end - start
        if p_time < timeout:
            time.sleep(timeout - p_time)


crawler()
print("")
if SHOW_OTHERS:
    print("Other links that are not URLs:")
    print(other_links_list)
    print("")
print("URLs that has NOT been Crawled:")
print(url_list)
print("")
print("URLs thats HAS been crawled:")
print(crawled_urls)
