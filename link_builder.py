from abc import ABC, abstractmethod, abstractproperty
import string, random
from datetime import datetime, time, date

#Product
class Url():
    def __init__(self):
        self.real_link = "real_link"
        self.ip_addy = "ip_addy"
        self.ad_type = "ad_type"
        self.token = "token"
        self.date = "date"
        self.hour = "hour"
      
#Abstract Builder Class
class UrlBuilder(ABC):
    @abstractmethod
    def get_real_link(self,real_link):
        pass
    @abstractmethod
    def get_ip_addy(self,ip_addy):
        pass
    @abstractmethod
    def get_ad_type(self):
        pass
    @abstractmethod
    def get_date(self):
        pass
    @abstractmethod
    def generate_token(self):
        pass
    @abstractmethod
    def return_data(self):
        pass
#Builder Concrete Classes
class AdUrlBuilder(UrlBuilder):
    def __init__(self):
        self.link = Url()
    def get_real_link(self,real_link):
        self.link.real_link = real_link
    def get_ad_type(self):
        self.link.ad_type = "True"
    def get_ip_addy(self,ip_addy):
        self.link.ip_addy = ip_addy
    def get_date(self):
        self.date = str(date.today())
    def get_hour(self):
        now = datetime.now()
        self.hour = str(time(now.hour,now.minute,now.second))
    def generate_token(self):
        strings = string.ascii_lowercase + string.ascii_uppercase
        token = ""
        for x in range(7):
            token += random.choice(strings)
        self.link.token = token
    def return_data(self):
       return self.link
class WithoutAdUrlBuilder(UrlBuilder):
    def __init__(self):
        self.link = Url()
    def get_real_link(self,real_link):
        self.link.real_link = real_link
    def get_ad_type(self):
        self.link.ad_type = "False"
    def get_date(self):
        self.date = str(date.today())
    def get_hour(self):
        now = datetime.now()
        self.hour = str(time(now.hour,now.minute,now.second))
    def get_ip_addy(self,ip_addy):
        self.link.ip_addy = ip_addy
    def generate_token(self):
        strings = string.ascii_lowercase + string.ascii_uppercase
        token = ""
        for x in range(7):
            token += random.choice(strings)
        self.link.token = token
    def return_data(self):
        return self.link