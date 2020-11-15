# PQual - Automating Qualitative evaluation of webpages

## Introduction

The increasing complexity of web pages has brought a number of solutions to offer simpler or lighter versions of these pages the qualitative evaluation of newversions is commonly carried outrelying on user studies in addition to associated costsrunning user studies might be extremely challenging due to health, travel and financial constraints. Moreover, user studies are prone to subjectivity which makes it difficult to compare theresults of different studies. pQual is a computer vision tool that helps to compare two web pages visually and gives a standardized score. This includes a three-step process:
1. Actionable tag identification
2. Individual component extraction, and
3. Component matching

For the technical details of the tool refer to the [published demo paper](https://dl.acm.org/doi/abs/10.1145/3379350.3416163) at ACM UIST 2020

## Installing the tool

### Installing Python Modules
PQual relies on `Selenium`, `Open CV`, `Beautiful Soup`, `NumPy`,`Scikit-Image`,

Install these by pip using the following command if you haven't already

```cmd
pip3 install -r requirements.txt
```

### Browser requirements
After downloading this repository:
- Make sure that you have `Mozilla Firefox` installed on your machine.
- Download the [Gecko Driver](https://github.com/mozilla/geckodriver/releases) and place it in `./drivers/`

### (Optional) Setting up Firefox Profiles

This step is only required if you want to compare two versions of the same webpage on different proxies.

**Proxy A** *is the base page that will be compared to*
**Proxy B** *is the page that will be compared to Proxy B for changes*

1. Open Firefox and enter `about:profiles` in the URL bar
2. Go to the option 'CREATE A NEW PROFILE' and name this Proxy A
3. After creating the new profile, launch firefox in the new profile
4. enter `about:preferences` in the URL bar and scroll down to "NETWORK SETTINGS"
5. Change proxy access to "MANUAL PROXY SELECTION" and add the desired HTTP Proxy and Port
6. Repeat this for another Profile and Proxy and call this Proxy B
7. find and save the path for these profiles. Generally the path is `/Users/NAME/Library/Application Support/Firefox/Profiles/`

## Using the tool
The pQual has modes to  the following cases:
- Adding proxies of the same website using firefox profiles and comparing the two proxy versions of the same webpage.
- Comparing websites on 2 different URLs
- Running component Analysis on 2 different screenshots

### Mode A: Using Proxies
⚠️  For this mode, the last step of setting up is required.
In this mode pQual will perform actions over all the tags in the website using *Proxy A* and evaluate which tags render change and calculate changes based on the screenshots obtained for *Proxy A*. the same website will be opened using *Proxy B* and the previously recorded actions will be emulated on the *Proxy B* browser.

```python
import pqual

pqual.PROXY_A = "/Users/waleed/Library/Application Support/Firefox/Profiles/7r4j2f81.Proxy_A"
pqual.PROXY_B = "/Users/waleed/Library/Application Support/Firefox/Profiles/98cha76a.Proxy_B"
WEBSITE = "http://google.com/"

pqual.compare(WEBSITE,mode="proxy")
```

### Mode B: Using 2 versions of the webpage without proxy
This mode does not require you to install firefox profiles. In this mode pQual will perform actions over all the tags in the **the Source Website** and evaluate which tags render change and calculate changes based on the screenshots obtained for **the Source Website**. On **Compared Website** the previously recorded actions will be emulated and a score will be calculated based on the area matched.

```python
import pqual

WEBSITE_SRC = "http://website.com/blog-1"
WEBSITE_CMP = "http://website.com/blog-2"

pqual.compare(WEBSITE_SRC,WEBSITE_CMP,mode="no_proxy")
```

### Mode C: Using 2 screenshots
This mode will not perform actions on tags in the website. Instead, it will compare two screenshots and return the score based on the area in **Source Screenshot** retained in the **Compared Screenshot**

```python
import pqual

SCREENSHOT_SRC = "screenshots/1.png"
SCREENSHOT_CMP = "screenshots/2.png"

pqual.compare(SCREENSHOT_SRC,SCREENSHOT_CMP,mode="screenshot")
```
