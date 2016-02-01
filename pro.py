import urllib2
from urllib2 import urlopen
import re
import cookielib
import unicodedata
from bs4 import BeautifulSoup

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

def main():
    try:

        name = raw_input("Enter product name: ")
        name = name.replace(' ','+')
                
       
        page = "http://www.cnet.com/search/?query="+name+"+reviews"
        sourceCode = opener.open(page).read()

        soup = BeautifulSoup(sourceCode,"lxml")

        Items = soup.findAll('div', {'class':'type'})
        links = []
        reviews =[]
        comments = []
        p_with_tags = []
        for item in Items:
            if unicodedata.normalize('NFKD', item.contents[0]).encode('ascii','ignore') == "Review":
                links.append(item.find_next_sibling("a"))
                reviews.append(item.find_next_sibling("p").string)

        
        for link in links:

            page1 = "http://www.cnet.com/"+link.get('href')+"user-reviews/"
            sourceCode1 = opener.open(page1).read()
            soup1 = BeautifulSoup(sourceCode1, "lxml")
            comments.append(soup1.findAll('h2', {'class': 'productTitle'}))


            page2 = "http://www.cnet.com/"+link.get('href')
            sourceCode2 = opener.open(page2).read()
            soup = BeautifulSoup(sourceCode2, "lxml")
            p_with_tags.append(soup.findAll('p', {'class':'theGood'}))
            p_with_tags.append(soup.findAll('p', {'class':'theBad'}))
            p_with_tags.append(soup.findAll('p', {'class':'theBottomLine'}))

        for p_with_tag in p_with_tags:
            for line in p_with_tag:
                    reviews.append(line.span.string)
                    

        for comment in comments:
            for line in comment:
                reviews.append(line.string)

        for review in reviews:
            print review
            print "\n-------------------------------------\n"

            
    except Exception, e:
        print str(e)

main()

                    