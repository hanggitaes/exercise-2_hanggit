import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class BookCartTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--disable-gpu")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get("https://bookcart.azurewebsites.net/")
        cls.driver.maximize_window()
    
    def test_register(self):
        """Test user registration with valid data."""
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Register").click()
        driver.find_element(By.ID, "firstName").send_keys("John")
        driver.find_element(By.ID, "lastName").send_keys("Doe")
        driver.find_element(By.ID, "username").send_keys("johndoe123")
        driver.find_element(By.ID, "password").send_keys("SecurePass123")
        driver.find_element(By.ID, "confirmPassword").send_keys("SecurePass123")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]").click()
        
        # Assertion to check registration success message
        success_message = driver.find_element(By.CLASS_NAME, "success-message").text
        self.assertIn("Registration successful", success_message)
    
    def test_login(self):
        """Test login with valid credentials."""
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Login").click()
        driver.find_element(By.ID, "username").send_keys("johndoe123")
        driver.find_element(By.ID, "password").send_keys("SecurePass123")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        
        # Assertion to check login success
        welcome_text = driver.find_element(By.CLASS_NAME, "welcome-message").text
        self.assertIn("Welcome", welcome_text)
    
    def test_add_to_cart_and_checkout(self):
        """Test adding an item to the shopping cart and proceeding to checkout."""
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Books").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Cart')]").click()
        driver.find_element(By.LINK_TEXT, "Cart").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Checkout')]").click()
        
        # Assertion to check checkout success message
        checkout_message = driver.find_element(By.CLASS_NAME, "checkout-success").text
        self.assertIn("Order placed successfully", checkout_message)
    
    def test_filter_by_category(self):
        """Test filtering products by category."""
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Categories").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fiction')]").click()
        
        # Assertion to check if the correct category is displayed
        category_header = driver.find_element(By.CLASS_NAME, "category-title").text
        self.assertIn("Fiction", category_header)
    
    def test_filter_by_price(self):
        """Test filtering products by price range."""
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Books").click()
        price_filter = driver.find_element(By.ID, "price-slider")
        price_filter.send_keys(Keys.ARROW_RIGHT * 5)
        
        # Assertion to check if products are filtered correctly
        filtered_products = driver.find_elements(By.CLASS_NAME, "product-item")
        self.assertGreater(len(filtered_products), 0)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()