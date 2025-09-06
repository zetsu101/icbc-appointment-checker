"""
ICBC Appointment Checker main module.
Handles browser automation and appointment availability checking.
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from config import Config
from notifier import Notifier


class ICBCAppointmentChecker:
    """Main class for checking ICBC appointment availability."""
    
    def __init__(self):
        self.config = Config()
        self.notifier = Notifier()
        self.driver = None
        self.last_checked_appointments = set()
        
    def setup_driver(self) -> bool:
        """Setup Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            
            if self.config.HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Disable images and CSS for faster loading
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-css")
            
            service = Service("/Users/magid/.wdm/drivers/chromedriver/mac64/139.0.7258.154/chromedriver-mac-arm64/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(self.config.BROWSER_TIMEOUT)
            
            print("Chrome WebDriver setup successful")
            return True
            
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            return False
    
    def login_to_icbc(self) -> bool:
        """Login to ICBC website."""
        try:
            print("Attempting to login to ICBC...")
            self.driver.get(self.config.ICBC_LOGIN_URL)
            
            # Wait for login form to load
            wait = WebDriverWait(self.driver, 10)
            time.sleep(3)  # Give page time to load completely
            time.sleep(2)  # Rate limiting - be respectful to ICBC servers
            
            # Find and fill last name field (first text input)
            try:
                last_name_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
                last_name_field.clear()
                last_name_field.send_keys(self.config.ICBC_LAST_NAME)
                print("Filled last name field")
            except Exception as e:
                print(f"Error with last name field: {e}")
                return False
            
            # Find and fill license number field (telephone input)
            try:
                license_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
                license_field.clear()
                license_field.send_keys(self.config.ICBC_LICENSE_NUMBER)
                print("Filled license field")
            except Exception as e:
                print(f"Error with license field: {e}")
                return False
            
            # Find and fill keyword field (password field)
            try:
                keyword_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                keyword_field.clear()
                keyword_field.send_keys(self.config.ICBC_KEYWORD)
                print("Filled keyword field")
            except Exception as e:
                print(f"Error with keyword field: {e}")
                return False
            
            # Check terms and conditions checkbox
            try:
                terms_checkbox = self.driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                if not terms_checkbox.is_selected():
                    # Try clicking the label instead of the checkbox
                    try:
                        label = self.driver.find_element(By.CSS_SELECTOR, "label[for='mat-checkbox-1-input']")
                        label.click()
                    except:
                        terms_checkbox.click()
                    print("Checked terms checkbox")
            except Exception as e:
                print(f"Terms checkbox not found: {e}")
            
            # Submit login form
            try:
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()
                print("Clicked login button")
            except Exception as e:
                print(f"Error clicking login button: {e}")
                return False
            
            # Wait for successful login
            try:
                wait.until(EC.url_contains("dashboard") or EC.url_contains("booking") or EC.url_contains("road-test"))
                print("Successfully logged in to ICBC")
                return True
            except TimeoutException:
                print("Login successful but URL didn't change as expected")
                return True
            
        except TimeoutException:
            print("Timeout during login process")
            return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    
    def navigate_to_booking_page(self) -> bool:
        """Navigate to the road test booking page."""
        try:
            print("Navigating to booking page...")
            self.driver.get(self.config.ICBC_BOOKING_URL)
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            print("Successfully navigated to booking page")
            return True
            
        except Exception as e:
            print(f"Error navigating to booking page: {e}")
            return False
    
    def select_license_type(self) -> bool:
        """Select the appropriate license type (Class 7 N Road Test)."""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Look for Class 7 (N) Road Test radio button
            try:
                license_radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value*='Class 7']")))
                license_radio.click()
                print("Selected Class 7 (N) Road Test")
                return True
            except TimeoutException:
                print("Could not find Class 7 license type - continuing anyway")
                return True
            
        except Exception as e:
            print(f"Error selecting license type: {e}")
            return True
    
    def search_for_locations(self) -> bool:
        """Search for locations based on preferred cities."""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Debug: Print all input elements on the page
            print("Debug: Looking for input elements on the page...")
            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Found {len(all_inputs)} input elements")
            for i, inp in enumerate(all_inputs):
                try:
                    placeholder = inp.get_attribute("placeholder") or "no placeholder"
                    input_type = inp.get_attribute("type") or "no type"
                    name = inp.get_attribute("name") or "no name"
                    print(f"Input {i}: type='{input_type}', placeholder='{placeholder}', name='{name}'")
                except:
                    print(f"Input {i}: could not get attributes")
            
            # Look for location search input field - try multiple selectors
            location_selectors = [
                "input[placeholder*='location']",
                "input[placeholder*='city']", 
                "input[placeholder*='search']",
                "input[placeholder*='Location']",
                "input[placeholder*='City']",
                "input[type='text']",
                "input[aria-label*='location']",
                "input[aria-label*='search']",
                "input[name*='location']",
                "input[name*='city']"
            ]
            
            location_input = None
            for selector in location_selectors:
                try:
                    location_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f"Found location input using selector: {selector}")
                    break
                except:
                    continue
            
            if not location_input:
                print("Could not find location search input - continuing anyway")
                return True
            
            # Try each preferred city
            for city in self.config.get_preferred_test_centers():
                try:
                    location_input.clear()
                    location_input.send_keys(city)
                    print(f"Typed '{city}' in location field")
                    time.sleep(3)  # Wait for suggestions to appear
                    
                    # Look for dropdown suggestions or autocomplete
                    suggestion_selectors = [
                        f"li:contains('{city}')",
                        f"div:contains('{city}')",
                        f"span:contains('{city}')",
                        f"option:contains('{city}')",
                        ".suggestion-item",
                        ".dropdown-item", 
                        ".autocomplete-item",
                        ".location-suggestion",
                        "[role='option']"
                    ]
                    
                    suggestion_found = False
                    for suggestion_selector in suggestion_selectors:
                        try:
                            suggestions = self.driver.find_elements(By.CSS_SELECTOR, suggestion_selector)
                            if suggestions:
                                suggestions[0].click()
                                print(f"Selected suggestion for '{city}'")
                                time.sleep(2)
                                suggestion_found = True
                                return True
                        except:
                            continue
                    
                    if not suggestion_found:
                        # Try pressing Enter or Tab to submit
                        location_input.send_keys(Keys.RETURN)
                        print(f"Pressed Enter after typing '{city}'")
                        time.sleep(2)
                    
                except Exception as e:
                    print(f"Error searching for '{city}': {e}")
                    continue
            
            print("No location suggestions found for any preferred city")
            return True
            
        except Exception as e:
            print(f"Error searching for locations: {e}")
            return True
    
    def select_test_center(self) -> bool:
        """Select a test center from the list of available locations."""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Look for test center selection buttons
            try:
                # Wait for location list to load
                time.sleep(3)
                
                # Look for location selection buttons (blue circular buttons with arrows)
                location_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[class*='location'], button[class*='select'], .location-item button")
                
                if location_buttons:
                    # Click the first available location
                    location_buttons[0].click()
                    print("Selected first available test center")
                    time.sleep(2)
                    return True
                else:
                    print("No test center selection buttons found - continuing anyway")
                    return True
                    
            except Exception as e:
                print(f"Error selecting test center: {e}")
                return True
            
        except Exception as e:
            print(f"Error in select_test_center: {e}")
            return True
    
    def check_availability(self) -> List[Dict[str, Any]]:
        """Check for available appointments."""
        try:
            print("Checking appointment availability...")
            
            # Wait for appointment slots to load
            wait = WebDriverWait(self.driver, 15)
            time.sleep(3)  # Give page time to load
            
            available_appointments = []
            
            # Look for appointment time buttons with more specific selectors
            time_slot_selectors = [
                "button:contains('AM')",
                "button:contains('PM')",
                "button:contains('Morning')",
                "button:contains('Afternoon')",
                "button:contains('Evening')",
                "button:contains('Available')",
                "button[class*='time']",
                "button[class*='appointment']",
                ".time-slot",
                ".appointment-slot",
                ".available-slot",
                "input[type='radio']",
                "label:contains('Available')",
                "[data-time]",
                ".slot-button",
                ".appointment-button",
                "button[style*='purple']",  # Purple buttons from your screenshot
                "button[style*='background']"
            ]
            
            time_buttons = []
            for selector in time_slot_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if buttons:
                        time_buttons.extend(buttons)
                        print(f"Found {len(buttons)} time slots using selector: {selector}")
                except:
                    continue
            
            if time_buttons:
                print(f"Found {len(time_buttons)} total appointment time slots")
                
                for button in time_buttons:
                    try:
                        # Extract appointment data from button
                        appointment_data = self._extract_appointment_data_from_button(button)
                        if appointment_data and self._is_appointment_suitable(appointment_data):
                            available_appointments.append(appointment_data)
                    except Exception as e:
                        print(f"Error extracting appointment data: {e}")
                        continue
            else:
                print("No appointment time slots found")
                
            print(f"Found {len(available_appointments)} suitable appointments")
            return available_appointments
            
        except Exception as e:
            print(f"Error checking availability: {e}")
            return []
    
    def _extract_appointment_data_from_button(self, button) -> Optional[Dict[str, Any]]:
        """Extract appointment data from a time slot button."""
        try:
            appointment_data = {
                'date': None,
                'time': None,
                'location': None,
                'license_type': 'Class 7 (N)'
            }
            
            # Get the button text (should contain time like "8:35 AM")
            button_text = button.text.strip()
            if button_text and any(word in button_text.lower() for word in ['am', 'pm']):
                appointment_data['time'] = button_text
            
            # Try to find the date from the page context
            try:
                # Look for date headers or context
                date_elements = self.driver.find_elements(By.CSS_SELECTOR, "h3, .date-header, [class*='date']")
                for element in date_elements:
                    text = element.text.strip()
                    if any(word in text.lower() for word in ['january', 'february', 'march', 'april', 'may', 'june', 
                                                           'july', 'august', 'september', 'october', 'november', 'december']):
                        appointment_data['date'] = text
                        break
            except:
                pass
            
            # Try to find location from page context
            try:
                location_elements = self.driver.find_elements(By.CSS_SELECTOR, "h2, .location-name, [class*='location']")
                for element in location_elements:
                    text = element.text.strip()
                    if any(center.lower() in text.lower() for center in self.config.get_preferred_test_centers()):
                        appointment_data['location'] = text
                        break
            except:
                pass
            
            return appointment_data if appointment_data['time'] else None
            
        except Exception as e:
            print(f"Error extracting appointment data from button: {e}")
            return None
    
    def _is_appointment_suitable(self, appointment_data: Dict[str, Any]) -> bool:
        """Check if appointment meets user preferences."""
        try:
            # Check if appointment is at a preferred test center
            if appointment_data.get('location'):
                location = appointment_data['location'].lower()
                preferred_centers = [center.lower() for center in self.config.get_preferred_test_centers()]
                
                if not any(center in location for center in preferred_centers):
                    return False
            
            # Check if appointment date is acceptable
            if appointment_data.get('date'):
                try:
                    # Parse date format like "Thursday, January 22nd, 2026"
                    date_text = appointment_data['date']
                    # Extract just the date part for parsing
                    import re
                    date_match = re.search(r'(\w+), (\w+) (\d+), (\d+)', date_text)
                    if date_match:
                        month_name = date_match.group(2)
                        day = date_match.group(3)
                        year = date_match.group(4)
                        
                        # Convert month name to number
                        month_map = {
                            'january': '01', 'february': '02', 'march': '03', 'april': '04',
                            'may': '05', 'june': '06', 'july': '07', 'august': '08',
                            'september': '09', 'october': '10', 'november': '11', 'december': '12'
                        }
                        month_num = month_map.get(month_name.lower(), '01')
                        
                        appointment_date = datetime.strptime(f"{year}-{month_num}-{day.zfill(2)}", '%Y-%m-%d')
                        earliest_acceptable = self.config.get_earliest_acceptable_date()
                        
                        if appointment_date < earliest_acceptable:
                            return False
                except ValueError:
                    # If date parsing fails, assume it's acceptable
                    pass
            
            return True
            
        except Exception as e:
            print(f"Error checking appointment suitability: {e}")
            return False
    
    def check_for_new_appointments(self) -> bool:
        """Main method to check for new appointments and send notifications."""
        try:
            if not self.setup_driver():
                return False
            
            if not self.login_to_icbc():
                return False
            
            if not self.navigate_to_booking_page():
                return False
            
            if not self.select_license_type():
                return False
            
            if not self.search_for_locations():
                return False
            
            if not self.select_test_center():
                return False
            
            available_appointments = self.check_availability()
            
            # Check for new appointments
            new_appointments = []
            for appointment in available_appointments:
                appointment_key = f"{appointment.get('date')}-{appointment.get('time')}-{appointment.get('location')}"
                if appointment_key not in self.last_checked_appointments:
                    new_appointments.append(appointment)
                    self.last_checked_appointments.add(appointment_key)
            
            # Send notifications for new appointments
            if new_appointments:
                print(f"Found {len(new_appointments)} new appointments!")
                for appointment in new_appointments:
                    self.notifier.send_notification(appointment)
                return True
            else:
                print("No new appointments found")
                return False
            
        except Exception as e:
            print(f"Error during appointment check: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
    
    def run_continuous_check(self):
        """Run continuous appointment checking with specified interval."""
        print(f"Starting continuous appointment checking every {self.config.CHECK_INTERVAL_MINUTES} minutes")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n--- Checking appointments at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
                self.check_for_new_appointments()
                
                # Wait for next check
                time.sleep(self.config.CHECK_INTERVAL_MINUTES * 60)
                
        except KeyboardInterrupt:
            print("\nStopping appointment checker...")
        except Exception as e:
            print(f"Error in continuous check: {e}")
