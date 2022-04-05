from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import undetected_chromedriver as u_chromedriver
import logging
import decimal
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrape_by_url(url):
    driver = __get_page_html(url[1])
    if type(driver) != type(None):
        name = __get_nft_name(driver)
        highest_bid = __get_nft_topbid(driver)
        favourites = __get_favourite_num(driver)
        offers = __get_buying_offers(driver)
        events = __get_events(driver)
        driver.close()
        nft_info = NftInfo(name, favourites, highest_bid)
        instance = NftInstance(url[0], nft_info, events, offers)
        return instance
    return None


def __get_page_html(URL):
    options = u_chromedriver.ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    logging.warning(user_agent)
    options.add_argument("--window-size=1920,1200")
    driver = u_chromedriver.Chrome(options=options)
    driver.get(URL)
    timeout = 10
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR,  "div[class='Rowreact__DivContainer-sc-amt98e-0 emCxyQ EventHistory--row']"))
        WebDriverWait(driver, timeout).until(element_present)


    except TimeoutException:
        logging.warning("timed out")
        try:
            driver.close()
        except WebDriverException:
            logging.warning("cannot close in 20 sec")
            driver.close()
            return None
        return None
    return driver


def __get_favourite_num(driver):
    try:
        fav_button = driver.find_element_by_css_selector("button[class='UnstyledButtonreact__UnstyledButton-sc-ty1bh0-0 btgkrL Blockreact__Block-sc-1xf18x6-0 Countreact__Container-sc-13kp31z-0 cayhdi iMVWtI']")
        fav_num = fav_button.text
        fav_num=[int(word)for word in fav_num.split() if word.isdigit()]
        logging.warning(fav_num[0])
    except (NoSuchElementException, StaleElementReferenceException):
        return 0

    return fav_num[0]


def __get_buying_offers(driver):
    try:
        price_offers_div= driver.find_element_by_css_selector("div[class='Blockreact__Block-sc-1xf18x6-0 jNeTzY']")
        price_offers_table=price_offers_div.find_elements_by_css_selector("li[class='Tablereact__TableRow-sc-120fhmz-1 fwzXIM']")[1:]
        offers=[]
        for li in price_offers_table:
            offer = li.find_element(By.CSS_SELECTOR,"span[class='Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 cKQpdV dUfmNR']").text.replace("$", "").replace(",","")
            if offer != "":
                offers.append(offer)
                logging.warning(offer)
        offers = [decimal.Decimal(offer) for offer in offers if offer != ""]
    except (NoSuchElementException, StaleElementReferenceException):
        logging.warning("no offers")
        return []
    return offers


def __get_span_event_text(div):
    return div.find_element_by_tag_name('span').get_attribute('innerHTML')


def __get_nft_topbid(driver):
    try:

        bid = driver.find_element(By.CLASS_NAME, 'TradeStation--price-container').text.replace(",","").replace("(", "").replace(")", "").replace("$","")
        logging.warning(bid)
        bid = [decimal.Decimal(word) for word in bid.split()]
        logging.warning(bid[0])
        logging.warning(bid[1])
    except (NoSuchElementException, StaleElementReferenceException):
        logging.warning("no top bid")
        return 0
    return bid[1]



def __get_events(driver):
    try:
        divs = driver.find_elements(By.CSS_SELECTOR, "div[class='Rowreact__DivContainer-sc-amt98e-0 emCxyQ EventHistory--row']")
        logging.warning("divs:" + str(len(divs)))
        events =  __get_events_data(divs,driver)
        logging.warning("events: " + str(len(events)))
    except (NoSuchElementException, StaleElementReferenceException):
        logging.warning("no events")
        return []
    return events

#return events lsit of eventData


def __get_nft_name(driver):
    try:
        name = driver.find_elements_by_tag_name('h1')
    except (NoSuchElementException, StaleElementReferenceException):
        logging.warning("name in h2")
        name = driver.find_element_by_tag_name('h2')
        return name.text
    return name[0].text


purchase_type_css_selector= "img[class='Blockreact__Block-sc-1xf18x6-0 Avatarreact__ImgAvatar-sc-sbw25j-1 dGKsYK hzWBaN']"
event_date_xpath=".//div[contains(text(),'pm') or contains(text(),'am')]"
date_span_xpath = ".//span[contains(text(),'ago') ]"
date_href_xpath = ".//a[contains(text(),'ago')]"
event_price_css_selector = "div[class='Row--cell Row--cellIsSpaced EventHistory--price-col']"


def month_to_num(month):
    return {
            'January': "01",
            'February': "02",
            'March': "03",
            'April': "04",
            'May': "05",
            'June': "06",
            'July': "07",
            'August': "08",
            'September': "09",
            'October': "10",
            'November': "11",
            'December': "12"
    }[month]


def convert_12_to_24_clock(time_attributes,split_time):
    if time_attributes[1] == "am" and int(split_time[0]) == 12:
        split_time[0] = "00"
    elif time_attributes[1] == "am" and int(split_time[0]) < 10:
        split_time[0] = "0" + split_time[0]
    elif time_attributes[1] == "pm" and int(split_time[0]) < 12:
        split_time[0] = str(int(split_time[0]) + 12)
    return split_time


def convert_to_datetime(event_date):
    holder = event_date.split(",")
    date = holder[0].split(" ")
    if int(date[1])<10:
        date[1] = "0"+date[1]
    date[0] = month_to_num(date[0])
    date[2] = date[2][2:]
    time_attributes = holder[1].split(" ")[1:]
    split_time = time_attributes[0].split(":")
    split_time = convert_12_to_24_clock(time_attributes,split_time)
    combined_date = date[1]+"/"+date[0]+"/"+date[2]+" "+split_time[0]+":"+split_time[1]+":00"
    date_time_obj=datetime.strptime(combined_date,  '%d/%m/%y %H:%M:%S')
    logging.warning(date_time_obj)
    return date_time_obj


def get_date(row, driver):
    try:
        date_span = row.find_element(By.XPATH, date_span_xpath)
        logging.warning("date span text:" + date_span.text)
        time.sleep(1)
        ActionChains(driver).move_to_element(date_span).perform()
        time.sleep(1)
        event_date = driver.find_element(By.XPATH, event_date_xpath).text
    except NoSuchElementException:
        try:
            date_href = row.find_element(By.XPATH, date_href_xpath)
            logging.warning("date href text:" + date_href.text)
            time.sleep(1)
            ActionChains(driver).move_to_element(date_href).perform()
            time.sleep(1)
            event_date = driver.find_element(By.XPATH, event_date_xpath).text
        except NoSuchElementException:
            logging.warning("a problem in finding elements")
    return convert_to_datetime(event_date)


def __get_events_data(rows, driver):
    events = []
    for row in rows:
        row_divs = row.find_elements_by_tag_name('div')
        event_name = __get_span_event_text(row_divs[0])
        event_date = get_date(row,driver)
        price_info = True
        try:
            event_price = row.find_element(By.CSS_SELECTOR,event_price_css_selector).text.replace(",","")
            purchase_type = row.find_element(By.CSS_SELECTOR,purchase_type_css_selector).get_attribute("alt")
            logging.warning(purchase_type)
            logging.warning(event_price)
        except (StaleElementReferenceException, NoSuchElementException)as e:
            price_info = False
            logging.warning(event_name)
            logging.warning(price_info)

        if not price_info:
            events.append(EventData(event_name, event_date))
        else:
            events.append(EventData(event_name,event_date,event_price,purchase_type))
    return events


class NftInfo:
    def __init__(self, name, favourites, highest_bid):
        self.name = name
        self.favourites = favourites
        self.highest = highest_bid

    def get_name(self):
        return self.name

    def get_favourite(self):
        return self.favourites

    def get_highest_bid(self):
        return self.highest


class NftInstance:
    def __init__(self, id,nft_info, events, offers):
        self.id = id
        self.nft_info = nft_info
        self.events = events
        self.offers = offers

    def get_name(self):
        return self.nft_info.get_name()

    def get_favourites(self):
        return self.nft_info.get_favourite()

    def get_highest(self):
        return self.nft_info.get_highest_bid()

    def get_id(self):
        return self.id


class EventData:
    def __init__(self, *args):
        self.event_name = args[0]
        self.event_date = args[1]
        if len(args) == 2:
            self.has_price = False
        else:
            self.has_price = True
            self.event_price = args[2]
            self.purchase_type = args[3]

    def get_event_name(self):
        return self.event_name

    def get_event_date(self):
        return self.event_date

    def has_price_info(self):
        return self.has_price

    def get_price(self):
        return self.event_price

    def get_purchase_type(self):
        return self.purchase_type
