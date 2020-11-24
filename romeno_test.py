import requests, json, time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


website = "en.unesco.org"


driver = webdriver.Firefox(executable_path="drivers/geckodriver")
driver.get("https://{}/".format(website))
URL = "https://ui-research-romeno.glitch.me/run?api_key=nyuaddauyn&url=https%3A%2F%2F{}&filtered=false&screenHeight=700&screenWidth=1000".format(website)


###########################################
####                                   ####
####    clicking listeners by xpath    ####
####                                   ####
###########################################


# print ("Requesting xpaths from the API....")
response = requests.get(URL)
# print ("Recieved")
#
# xpaths = []

xpaths = ['/html[@class="js"]/body[@class="html front not-logged-in one-sidebar sidebar-second page-frontpage i18n-en"]', '/html[@class="js"]/body[@class="html front not-logged-in one-sidebar sidebar-second page-frontpage i18n-en"]', '/html[@class="js"]/body[@class="html front not-logged-in one-sidebar sidebar-second page-frontpage i18n-en"]', 'id("google-cse-results-searchbox-form")', 'id("edit-query")', 'id("edit-query")', 'id("gs_id50")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gsc-i-id1")', 'id("gs_st50")/a[@class="gsst_a"]', 'id("gs_st50")/a[@class="gsst_a"]', 'id("gs_st50")/a[@class="gsst_a"]', 'id("gs_st50")/a[@class="gsst_a"]', 'id("___gcse_0")/div[@class="gsc-control-searchbox-only gsc-control-searchbox-only-en"]/form[@class="gsc-search-box gsc-search-box-tools"]/table[@class="gsc-search-box"]/tbody[1]/tr[1]/td[@class="gsc-search-button"]/button[@class="gsc-search-button gsc-search-button-v2"]', 'id("___gcse_0")/div[@class="gsc-control-searchbox-only gsc-control-searchbox-only-en"]/form[@class="gsc-search-box gsc-search-box-tools"]/table[@class="gsc-search-box"]/tbody[1]/tr[1]/td[@class="gsc-clear-button"]/div[@class="gsc-clear-button"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="first expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="first expanded dropdown"]', 'id("info")', 'id("info")', 'id("info")', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("folder")', 'id("folder")', 'id("folder")', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("globe")', 'id("globe")', 'id("globe")', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]/ul[@class="dropdown-menu"]/li[@class="leaf"]/a[1]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]/ul[@class="dropdown-menu"]/li[@class="leaf"]/a[1]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("handshake")', 'id("handshake")', 'id("handshake")', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="expanded dropdown"]', 'id("hand")', 'id("hand")', 'id("hand")', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]/a[@class="dropdown-toggle"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]/a[@class="dropdown-toggle"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]/a[@class="dropdown-toggle"]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]/ul[@class="dropdown-menu"]/li[@class="leaf"]/a[1]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]/ul[@class="dropdown-menu"]/li[@class="leaf"]/a[1]', 'id("main-navbar")/nav[1]/ul[@class="menu nav navbar-nav"]/li[@class="last expanded dropdown"]/ul[@class="dropdown-menu"]/li[@class="leaf"]/a[1]', 'id("share-respect")', 'id("views_slideshow_pager_field_item_top_news-front_infocus_block_1_0")', 'id("views_slideshow_pager_field_item_top_news-front_infocus_block_1_1")', 'id("views_slideshow_pager_field_item_top_news-front_infocus_block_1_2")', 'id("views_slideshow_pager_field_item_top_news-front_infocus_block_1_3")', 'id("views_slideshow_cycle_teaser_section_news-front_infocus_block_1")', 'id("views_slideshow_cycle_teaser_section_news-front_infocus_block_1")', 'id("styles-0-0")/img[@class="img-responsive"]', 'id("1")', 'id("2")', 'id("3")', 'id("myCarousel")', 'id("myCarousel")', 'id("myCarousel")', 'id("myCarousel")/div[@class="carousel-inner"]/div[@class="item active"]/div[@class="row"]/div[@class="col-sm-3"]/div[@class="views-field views-field-title"]/span[@class="field-content title"]/a[1]', 'id("myCarousel")/div[@class="carousel-inner"]/div[@class="item active left"]/div[@class="row"]/div[@class="col-sm-3"]/div[@class="views-field views-field-field-media-image"]/div[@class="field-content media"]/a[1]', 'id("myCarousel")/div[@class="carousel-inner"]/div[@class="item"]/div[@class="row"]/div[@class="col-sm-3"]/div[@class="views-field views-field-title"]/span[@class="field-content title"]/a[1]', 'id("myCarousel")/div[@class="carousel-inner"]/div[@class="item"]/div[@class="row"]/div[@class="col-sm-3"]/div[@class="views-field views-field-field-media-image"]/div[@class="field-content media"]/a[1]', 'id("myCarousel")/a[@class="left carousel-control"]', 'id("myCarousel")/a[@class="right carousel-control"]', 'id("cboxOverlay")', 'id("cboxPrevious")', 'id("cboxNext")']
#
# for listener in response.json()["listeners"]:
#     xp = (listener["xpathInfo"])
#     xpaths.append(xp)

# print (xpaths)


for xp in xpaths:
    a = input("enter for the next xPath")

    print (driver.current_url)

    while driver.current_url != "https://{}/".format(website):
        driver.get("https://{}/".format(website))
        time.sleep(2)

    print ("XPATH:\t", xp)

    try:
        element = driver.find_elements_by_xpath(xp)[0]
    except:
        print (f"{xp} not found on page")

    try:
        element.click()
    except:
        print (f"{xp} couldn't be clicked")

###########################################
####                                   ####
####    sending keys to searchboxes    ####
####                                   ####
###########################################

textBoxes = driver.find_elements_by_xpath("//input[@type=\'text\']")

for t in textBoxes:
    try:
        t.send_keys("123")
        send_keys(u'\ue007')

    except:
        pass

driver.close()
