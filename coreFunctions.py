from skimage.measure import compare_ssim as ssim
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import cv2, skimage,os,time
import numpy as np
from matplotlib import pyplot as plt
import random
import os, shutil

######### PREFERENCE VARIABLES

PROXY_A = ""
PROXY_B = ""
generateReport = False
ACTIVE_SESSION_IDs = []


###################################
###                             ###
###       Index Functions       ###
###                             ###
###################################

def compareWithProxy(WEBSITE,PROXY_A,PROXY_B):

    print("Website:\t\t\t{}\nSource Proxy Profile:\t\t{}\nComparison Proxy Profile:\t{}\n".format(WEBSITE,PROXY_A,PROXY_B))

    scores = []

    print ("SRC stated")
    SRC_SESSION, importantTags = evaluateSrcPage(WEBSITE,PROXY=True)
    print ("CMP started")
    CMP_SESSION, errorLog = evaluateCmpPage(WEBSITE,importantTags,PROXY=True)

    print ("Component Analysis Started")
    scores = componentAnalysis_multipleTags(WEBSITE,importantTags,SRC_SESSION,CMP_SESSION)

    score = sum(scores) / len(scores)

    clearFolders()

    print (f"PQual Score: {score}")
    return score

def compareWithNoProxy(WEBSITE_SRC,WEBSITE_CMP):
    print("Source Website:\t\t{}\nComparison Website:\t{}".format(WEBSITE_SRC,WEBSITE_CMP))

    scores = []

    print ("SRC stated")
    SRC_SESSION, importantTags = evaluateSrcPage(WEBSITE_SRC)
    print ("CMP started")
    CMP_SESSION, errorLog = evaluateCmpPage(WEBSITE_CMP,importantTags)

    print ("Component Analysis Started")
    scores = componentAnalysis_multipleTags(WEBSITE_SRC,importantTags,SRC_SESSION,CMP_SESSION)

    score = sum(scores) / len(scores)

    clearFolders()

    print (f"PQual Score: {score}")
    return score


def compareWithScreenshots(SCREENSHOT_SRC,SCREENSHOT_CMP):
    print("Source screenshot:\t{}\nComparison screenshot:\t{}".format(SCREENSHOT_SRC,SCREENSHOT_CMP))

    score = compareImages (SCREENSHOT_SRC,SCREENSHOT_CMP)
    print (f"PQual Score: {score}")

    return score

###############################################
###                                         ###
###         Browser Action Functions        ###
###                                         ###
###############################################

def evaluateSrcPage (WEBSITE,PROXY=False):
    sessionID = getSessionID()

    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.set_headless()
    if PROXY:
        print("Using Proxy A")
        fireFoxProf = webdriver.FirefoxProfile(PROXY_A)

    driver = webdriver.Firefox(executable_path="drivers/geckodriver",firefox_options=firefoxOptions)

    matrix = []
    TAGS = []

    driver.get("https://{}/".format(WEBSITE))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,0);")
    total_height = driver.execute_script("return document.body.scrollHeight")
    if total_height < 1080: total_height = 1080
    driver.set_window_size(1920, total_height)
    driver.save_screenshot("screenshots/{}-{}-SRC.png".format(str(sessionID),WEBSITE))

    soup = bs(driver.page_source.encode("utf-8"),"lxml")

    for tag in ["nav","li","ul","div","p","span","h1","h2","h3","h4","h5","h6","p","button"]:
        tags = soup.findAll (tag)
        for t in tags:
            if t.get("id")!=None:
                if type(t.get("id")) == type([]):
                    for name in t.get("id"):
                        appendable = {"type":"id","tag":tag,"name":name}
                        if not appendable in matrix: matrix.append(appendable)

                else:
                    appendable = {"type":"id","tag":tag,"name":t.get("id")}
                    if not appendable in matrix: matrix.append(appendable)

            if t.get("class")!=None:
                if type(t.get("class")) == type([]):
                    for name in t.get("class"):
                        appendable = {"type":"class","tag":tag,"name":name}
                        if not appendable in matrix: matrix.append(appendable)

                else:
                    appendable = {"type":"class","tag":tag,"name":t.get("class")}
                    if not appendable in matrix: matrix.append(appendable)


    print ("Number of unique ID/classes found: ",len (matrix))

    # print ("hovering over tags and taking screenshots now")

    org = cv2.imread("screenshots/{}-{}-SRC.png".format(str(sessionID),WEBSITE))

    for m in matrix:

        try:
            elem = driver.find_element_by_xpath("//{}[@{}=\'{}\']".format(m["tag"],m["type"],m["name"]))
            # hover over that element
            actions = ActionChains(driver)
            # driver.execute_script("arguments[0].scrollIntoView();", elem)
            actions.move_to_element(elem)
            actions.perform()

            path = "screenshots/{}-{}-{}-{}-{}.png".format(str(sessionID),WEBSITE,m["tag"],m["type"],m["name"])
            driver.save_screenshot(path)

            new = cv2.imread(path)
            diff = skimage.metrics.structural_similarity(org,new, multichannel=True)
            # print ("Simmilarity Index", diff)

            tolerance = 0.99

            if diff <= tolerance:
                TAGS.append ({"tag":m["tag"],"type":m["type"],"name":m["name"],"Score":diff, "Comparable":True})

            else:
                TAGS.append ({"tag":m["tag"],"type":m["type"],"name":m["name"],"Score":diff, "Comparable":False})

        except:
            # print ("Error locating {} {} {}".format(m["tag"],m["type"],m["name"]))
            TAGS.append ({"tag":m["tag"],"type":m["type"],"name":m["name"],"Score":0, "Comparable":False})

    driver.close()

    IMP_TAGS = []

    for t in TAGS:
        if t["Comparable"]==True:
            IMP_TAGS.append(t)

    print("Number of Comparable tags: ", len(IMP_TAGS))

    return sessionID, IMP_TAGS

def evaluateCmpPage (WEBSITE,impTAGS,PROXY=False):
    sessionID = getSessionID()
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.set_headless()
    if PROXY:
        print("Using Proxy B")
        fireFoxProf = webdriver.FirefoxProfile(PROXY_B)

    driver = webdriver.Firefox(executable_path="drivers/geckodriver",firefox_options=firefoxOptions)

    driver.get("https://{}/".format(WEBSITE))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0,0);")
    total_height = driver.execute_script("return document.body.scrollHeight")
    if total_height < 1080: total_height = 1080
    driver.set_window_size(1920, total_height)

    driver.save_screenshot("screenshots/{}-{}-CMP.png".format(str(sessionID),WEBSITE))

    errorLog = []

    # print ("hovering over tags and taking screenshots now")

    for m in impTAGS:
        try:
            elem = driver.find_element_by_xpath("//{}[@{}=\'{}\']".format(m["tag"],m["type"],m["name"]))
            # hover over that element
            actions = ActionChains(driver)
            # driver.execute_script("arguments[0].scrollIntoView();", elem)
            actions.move_to_element(elem)
            actions.perform()

            path = "screenshots/{}-{}-{}-{}-{}.png".format(str(sessionID),WEBSITE,m["tag"],m["type"],m["name"])
            driver.save_screenshot(path)

        except:
            # print ("Error locating {} {} {}".format(m["tag"],m["type"],m["name"]))
            errorLog.append ({"tag":m["tag"],"type":m["type"],"name":m["name"],"Error":"Not found"})

    driver.close()
    return sessionID, errorLog


###############################################
###                                         ###
###        Component Analysis Funcs         ###
###                                         ###
###############################################

def componentAnalysis_multipleTags(WEBSITE,TAGS,SRC_SESSION,CMP_SESSION):

    scores = []
    errorLog = []

    for tag in TAGS:
        try:
            srcPath = "screenshots/{}-{}-{}-{}-{}.png".format(str(SRC_SESSION),WEBSITE,tag["tag"],tag["type"],tag["name"])
            cmpPath = "screenshots/{}-{}-{}-{}-{}.png".format(str(CMP_SESSION),WEBSITE,tag["tag"],tag["type"],tag["name"])

            score = compareImages (srcPath,cmpPath)
        except:
            errorLog.append(tag)

    return scores

def subtractImages(SRC_PATH, SRC_IMAGE,components):
    base = SRC_IMAGE

    for c in components:
        subject = c["component"]
        topX, topY =  c["position"]
        try:
            base[topX:topX+subject.shape[0],topY:topY+subject.shape[1],:] -= subject
            # print(np.unique(base[topX:topX+subject.shape[0],topY:topY+subject.shape[1],:].flatten()))
        except:
            print ("err")

    cv2.imwrite("reports/" + SRC_PATH.split("/")[-1], base)

def compareImages(SRC_PATH, CMP_PATH):

    totalScore = 0

    # print('reading')
    SRC_IMAGE = cv2.imread(SRC_PATH)
    CMP_IMAGE = cv2.imread(CMP_PATH)

    # print('thresholding')
    SRC_th = binaryThresholding(cv2.imread(SRC_PATH,0))

    # print('breaking SRC into components')
    area,components = breakIntoComponents(SRC_th, SRC_IMAGE)

    # print(f'broken into {len(components)} components')

    totalComponentArea = 0

    found = []
    notFound = []

    for cmp in components:
        c = cmp["component"]
        totalComponentArea +=  c.shape[0]*c.shape[1]
        matchFound = find_image(CMP_IMAGE,c) #returns tuple of x,y if found
        if matchFound:
            totalScore += c.shape[0]*c.shape[1]
            found.append({"position":matchFound,"component":c})
        else:
            croppedFromOriginalPos = CMP_IMAGE[cmp["loc"][1]:cmp["loc"][1]+c.shape[0],cmp["loc"][0]:cmp["loc"][0]+c.shape[1],:]
            print(c.shape,croppedFromOriginalPos.shape)
            try:
                totalScore += c.shape[0]*c.shape[1]* ssim(c,croppedFromOriginalPos,multichannel=True)
                notFound.append({"position":cmp["loc"][::-1],"component":c})
            except:
                ("dim error")


    if generateReport:
        subtractImages (SRC_PATH,CMP_IMAGE,found+notFound)


    return totalScore/totalComponentArea

def binaryThresholding(img):
    img = cv2.medianBlur(img,5)
    th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    return th

def normalise(website,background=None, imagePath=None,):
    # change background to black(0)
    # transorm the rest of the pixels to
    # monotone for easier comparison later
    if website!=None:
        background = website["background"]
        img = website["screenshot"]
    else:
        img = cv2.imread("screenshots/"+imagePath)

    black = 0
    white = 255
    k = 0
    l = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if list(img[i][j]) == background:
                img[i][j] = black
                l+=1
            else:
                img[i][j] = white
                k+=1
    print ("Normalise ratio: ", k,l)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def breakIntoComponents(img, originalImage):

    img = cv2.bitwise_not(img)
    cv2.imwrite("screenshots/1.png" , img)

    totalArea = 0
    nChannels = 3 #RGB
    maskArray = []
    kernalConst = 12
    kernalHolds = False
    maxComponents = img.shape[0]//6

    while not kernalHolds:
        # dilate components: this will join the nearby components for them to be grouped
        img_dil = cv2.dilate (img,np.ones((kernalConst,kernalConst)))

        cv2.imwrite("screenshots/2.png" , img_dil)

        labels, markers = cv2.connectedComponents(img_dil.astype(np.uint8),connectivity=8)

        img0_mask = skimage.measure.label(markers, background = 0).flatten()

        if labels < maxComponents//6:
            kernalConst -= 1
            #print(f"updating kernalConst to {kernalConst}")
        elif labels > maxComponents:
            kernalConst += 1
            #print(f"updating kernalConst to {kernalConst}")
        else:
            kernalHolds=True

    for i in range (1,labels,1):
        component = np.where(img0_mask==i)[0]

        # totalComponentArea += saveComponent(imgOrg,component,markers.shape,i,save_dir)

        sizeForFlatten = markers.shape[0]*markers.shape[1]

        originalImage_flat = originalImage.flatten().reshape(sizeForFlatten , nChannels)

        mask = np.zeros(sizeForFlatten * nChannels).reshape(sizeForFlatten , nChannels)
        for c in component:
            mask[c] = originalImage_flat[c]

        # mask = cv2.erode(mask, np.ones((50, 50)))

        mask = mask.reshape(markers.shape[0],markers.shape[1],nChannels)

        mask, loc = crop(mask,originalImage)

        componentArea = mask.shape[0]*mask.shape[1]

        # discard small components
        if componentArea > 100:
            totalArea += componentArea
            maskArray.append({"component":mask,"loc":loc})

    for i in range(len(maskArray)):
        cv2.imwrite("screenshots/component_" + str(i) + ".png" , maskArray[i]["component"])

    return totalArea,maskArray

def breakIntoComponents2 (simplifiedWebsite,tag,normalisedScreenshot):
    img0_norm = normalisedScreenshot
    imgOrg = cv2.imread ("screenshots/{}-{}-{}-{}-{}.png".format(simplifiedWebsite["proxy"],simplifiedWebsite["Name"],tag["tag"],tag["type"],tag["name"]))

    save_dir = "screenshots/components/{}-{}-{}-{}-{}-{}".format(simplifiedWebsite["proxy"],simplifiedWebsite["Name"],tag["tag"],tag["type"],tag["name"],"component")

    # dilate components: this will join the nearby components for them to be grouped
    img0_dil = cv2.dilate (img0_norm,np.ones((12,12)))

    labels, markers = cv2.connectedComponents(img0_dil.astype(np.uint8),connectivity=8)

    img0_mask = skimage.measure.label(markers, background = 0).flatten()

    totalComponentArea = 0

    for i in range (1,labels,1):
        component = np.where(img0_mask==i)[0]
        totalComponentArea += saveComponent(imgOrg,component,markers.shape,i,save_dir)

    return labels,totalComponentArea

def crop(mask,imgOrg):
    cv2.imwrite ('temp.png', mask)
    img = cv2.imread('temp.png')
    os.remove('temp.png')

    # print (img.shape,img1.shape)
    # img = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)

    x,y,w,h = cv2.boundingRect(thresh)

    crop = imgOrg[y:y+h,x:x+w]
    loc = [x,y]

    # cv2.imwrite("1.jpg",imgOrg)
    return crop,loc

def trim_recursive_crop(img_norm,img_org):
    if img_norm.shape[0] == 0:
        return np.zeros((0,0,3))

      # crop top
    if not np.sum(img_norm[0]):
        return trim_recursive_crop(img_norm[1:],img_org[1:])
      # crop bottom
    elif not np.sum(img_norm[-1]):
        return trim_recursive_crop(img_norm[:-1],img_org[:-1])
      # crop left
    elif not np.sum(img_norm[:, 0]):
        return trim_recursive_crop(img_norm[:, 1:],img_org[:, 1:])
        # crop right
    elif not np.sum(img_norm[:, -1]):
        return trim_recursive_crop(img_norm[:, :-1],img_org[:, 1:])

    return img_org

def saveComponent (imgOrg,comp,shape,label,save_dir):
    nChannels = 3 #RGB

    sizeForFlatten = shape[0]*shape[1]
    originalImage = imgOrg.flatten().reshape(sizeForFlatten , nChannels)

    mask = np.zeros(sizeForFlatten * nChannels).reshape(sizeForFlatten , nChannels)
    for c in comp:
        mask[c] = originalImage[c]

    # mask = cv2.erode(mask, np.ones((50, 50)))

    mask = mask.reshape(shape[0],shape[1],nChannels)
    mask = crop(mask,imgOrg)

    componentArea = mask.shape[0]*mask.shape[1]
    # print(componentArea)

    if len(mask.flatten()) < 20:
        print ("component too small")
    else:
        cv2.imwrite(save_dir + "-" + str(label) + ".png" , mask)

    return componentArea

def find_image(im, tpl):
    tpl = tpl[1:-1,1:-1,:]
    im = np.atleast_3d(im)
    tpl = np.atleast_3d(tpl)
    H, W, D = im.shape[:3]
    h, w = tpl.shape[:2]

    # Integral image and template sum per channel
    sat = im.cumsum(1).cumsum(0)
    tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])

    # Calculate lookup table for all the possible windows
    iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:]
    lookup = iD - iB - iC + iA

    # Possible matches
    possible_match = np.where(np.logical_and.reduce([lookup[..., i] == tplsum[i] for i in range(D)]))

    # Find exact match
    for y, x in zip(*possible_match):
        if np.all(im[y+1:y+h+1, x+1:x+w+1] == tpl):
            return (y, x)

    return False
    raise Exception("Image not found")


###############################################
###                                         ###
###             Misc. Functions             ###
###                                         ###
###############################################

def reset():
    clearFolders()
    resetPreferences()

    # reset preferences

def clearFolders():
    folder = 'screenshots'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def resetPreferences():
    global PROXY_A,PROXY_B,generateReport
    PROXY_A = ""
    PROXY_B = ""
    generateReport = False


# def generateReport(scores,errorLog):
#     pass

def getSessionID():
    r = random.randint(100000000,999999999)

    while r in ACTIVE_SESSION_IDs:
        r = random.randint(100000000,999999999)

    ACTIVE_SESSION_IDs.append(r)
    return r
