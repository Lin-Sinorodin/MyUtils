class ColabUtils:

    @staticmethod
    def on_colab():
        """Check if the code is running on Google Colab. Source: https://stackoverflow.com/a/53586419"""
        import sys
        return 'google.colab' in sys.modules

    @staticmethod
    def selenium_webdriver():
        """Selenium webdriver, works on Colab. Based on: https://github.com/korakot/kora/blob/master/kora/selenium.py"""
        import os
        os.system('apt update')
        os.system('apt install chromium-chromedriver')
        os.system('pip install selenium')

        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        return webdriver.Chrome('chromedriver', options=options)
