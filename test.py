import pqual

WEBSITE_SRC = "en.unesco.org"
WEBSITE_CMP = "en.unesco.org"

## using proxy mode
pqual.PROXY_A = "/Users/waleed/Library/Application Support/Firefox/Profiles/7r4j2f81.Proxy_A"
pqual.PROXY_B = "/Users/waleed/Library/Application Support/Firefox/Profiles/98cha76a.Proxy_B"
pqual.compare(WEBSITE_SRC,mode="proxy")

## using no_proxy mode
pqual.compare(WEBSITE_SRC,WEBSITE_CMP,mode="no_proxy")

## comparing screenshots
pqual.compare("one.png","two.png",mode="screenshot")
pqual.compare("original.png","reduced.png",mode="screenshot")
