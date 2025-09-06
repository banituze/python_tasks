#!/usr/bin/env python3
"""
Level 2 Task 3: API Integration
A Python script that interacts with external APIs to fetch and display data.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

class APIClient:
    def __init__(self):
        """Initialize the API client"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Python-API-Client/1.0'
        })
        self.timeout = 10
        self.max_retries = 3
    
    def make_request(self, url: str, method: str = 'GET', params: Dict = None, 
                    headers: Dict = None, data: Dict = None) -> Optional[Dict]:
        """Make HTTP request with error handling and retries"""
        if headers:
            self.session.headers.update(headers)
        
        for attempt in range(self.max_retries):
            try:
                print(f" Making {method} request to: {url}")
                
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, timeout=self.timeout)
                elif method.upper() == 'POST':
                    response = self.session.post(url, params=params, json=data, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                
                try:
                    data = response.json()
                    print(f" Request successful (Status: {response.status_code})")
                    return data
                except json.JSONDecodeError:
                    print(" Response is not valid JSON, returning text")
                    return {"text": response.text, "status_code": response.status_code}
                
            except requests.exceptions.RequestException as e:
                print(f" Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return None
        
        return None

class WeatherAPI:
    def __init__(self):
        """Initialize Weather API client"""
        self.client = APIClient()
        self.base_url = "https://wttr.in"
    
    def get_weather(self, location: str, format_type: str = "json") -> Optional[Dict]:
        """Get weather information for a location"""
        url = f"{self.base_url}/{location}"
        params = {"format": format_type} if format_type != "json" else {}
        
        if format_type == "json":
            url += "?format=j1"
        
        return self.client.make_request(url, params=params)
    
    def display_weather(self, weather_data: Dict, location: str):
        """Display weather information in a user-friendly format"""
        if not weather_data:
            print(" No weather data to display")
            return
        
        print(f"\n  WEATHER REPORT FOR {location.upper()}")
        print("=" * 50)
        
        try:
            current = weather_data.get('current_condition', [{}])[0]
            
            temp_c = current.get('temp_C', 'N/A')
            temp_f = current.get('temp_F', 'N/A')
            feels_like_c = current.get('FeelsLikeC', 'N/A')
            feels_like_f = current.get('FeelsLikeF', 'N/A')
            humidity = current.get('humidity', 'N/A')
            description = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
            wind_speed = current.get('windspeedKmph', 'N/A')
            wind_dir = current.get('winddir16Point', 'N/A')
            
            print(f"  Temperature: {temp_c}°C ({temp_f}°F)")
            print(f" Feels like: {feels_like_c}°C ({feels_like_f}°F)")
            print(f"  Condition: {description}")
            print(f" Humidity: {humidity}%")
            print(f" Wind: {wind_speed} km/h {wind_dir}")
            
            # Display forecast if available
            weather = weather_data.get('weather', [])
            if weather:
                print(f"\n 3-DAY FORECAST:")
                print("-" * 30)
                
                for day in weather[:3]:
                    date = day.get('date', 'N/A')
                    max_temp = day.get('maxtempC', 'N/A')
                    min_temp = day.get('mintempC', 'N/A')
                    
                    hourly = day.get('hourly', [{}])
                    if hourly:
                        desc = hourly[0].get('weatherDesc', [{}])[0].get('value', 'N/A')
                    else:
                        desc = 'N/A'
                    
                    print(f"{date}: {min_temp}°C - {max_temp}°C, {desc}")
            
        except (KeyError, IndexError) as e:
            print(f" Error parsing weather data: {e}")
            print("Raw data available:")
            print(json.dumps(weather_data, indent=2))

class CryptocurrencyAPI:
    def __init__(self):
        """Initialize Cryptocurrency API client"""
        self.client = APIClient()
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_coin_prices(self, coins: List[str] = None, vs_currency: str = "usd") -> Optional[Dict]:
        """Get cryptocurrency prices"""
        if not coins:
            coins = ["bitcoin", "ethereum", "dogecoin", "litecoin", "cardano"]
        
        coins_str = ",".join(coins)
        url = f"{self.base_url}/simple/price"
        params = {
            "ids": coins_str,
            "vs_currencies": vs_currency,
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        
        return self.client.make_request(url, params=params)
    
    def get_trending_coins(self) -> Optional[Dict]:
        """Get trending cryptocurrencies"""
        url = f"{self.base_url}/search/trending"
        return self.client.make_request(url)
    
    def display_prices(self, price_data: Dict, vs_currency: str = "usd"):
        """Display cryptocurrency prices"""
        if not price_data:
            print(" No price data to display")
            return
        
        currency_symbol = {"usd": "$", "eur": "€", "gbp": "£"}.get(vs_currency, vs_currency.upper())
        
        print(f"\n CRYPTOCURRENCY PRICES ({vs_currency.upper()})")
        print("=" * 60)
        print(f"{'Coin':<15} {'Price':<15} {'24h Change':<15} {'Market Cap':<15}")
        print("-" * 60)
        
        for coin, data in price_data.items():
            price = data.get(vs_currency, 0)
            change_24h = data.get(f"{vs_currency}_24h_change", 0)
            market_cap = data.get(f"{vs_currency}_market_cap", 0)
            
            # Format price
            if price < 1:
                price_str = f"{currency_symbol}{price:.6f}"
            elif price < 100:
                price_str = f"{currency_symbol}{price:.2f}"
            else:
                price_str = f"{currency_symbol}{price:,.2f}"
            
            # Format change with color indicators
            if change_24h > 0:
                change_str = f" +{change_24h:.2f}%"
            else:
                change_str = f" {change_24h:.2f}%"
            
            # Format market cap
            if market_cap > 1e9:
                cap_str = f"{currency_symbol}{market_cap/1e9:.1f}B"
            elif market_cap > 1e6:
                cap_str = f"{currency_symbol}{market_cap/1e6:.1f}M"
            else:
                cap_str = f"{currency_symbol}{market_cap:,.0f}"
            
            print(f"{coin.capitalize():<15} {price_str:<15} {change_str:<15} {cap_str:<15}")
    
    def display_trending(self, trending_data: Dict):
        """Display trending cryptocurrencies"""
        if not trending_data:
            print(" No trending data to display")
            return
        
        coins = trending_data.get('coins', [])
        if not coins:
            print(" No trending coins found")
            return
        
        print(f"\n TRENDING CRYPTOCURRENCIES")
        print("=" * 50)
        
        for i, coin_data in enumerate(coins, 1):
            coin = coin_data.get('item', {})
            name = coin.get('name', 'N/A')
            symbol = coin.get('symbol', 'N/A')
            market_cap_rank = coin.get('market_cap_rank', 'N/A')
            
            print(f"{i:2d}. {name} ({symbol.upper()}) - Rank #{market_cap_rank}")

class NewsAPI:
    def __init__(self):
        """Initialize News API client"""
        self.client = APIClient()
        # Using a free news API that doesn't require API key
        self.base_url = "https://jsonplaceholder.typicode.com/posts"  # Demo API
        # Alternative: "https://newsapi.org/v2" (requires API key)
    
    def get_demo_posts(self) -> Optional[List[Dict]]:
        """Get demo posts (since we don't have a real news API key)"""
        return self.client.make_request(self.base_url)
    
    def display_posts(self, posts_data: List[Dict]):
        """Display posts/articles"""
        if not posts_data:
            print(" No posts to display")
            return
        
        print(f"\n LATEST POSTS")
        print("=" * 60)
        
        for i, post in enumerate(posts_data[:10], 1):  # Show first 10
            title = post.get('title', 'N/A')
            body = post.get('body', 'N/A')
            user_id = post.get('userId', 'N/A')
            
            print(f"\n{i:2d}. {title.title()}")
            print(f"    Author ID: {user_id}")
            print(f"    {body[:100]}...")

class JokeAPI:
    def __init__(self):
        """Initialize Joke API client"""
        self.client = APIClient()
        self.base_url = "https://official-joke-api.appspot.com"
    
    def get_random_joke(self) -> Optional[Dict]:
        """Get a random joke"""
        url = f"{self.base_url}/random_joke"
        return self.client.make_request(url)
    
    def get_jokes_by_category(self, category: str, count: int = 5) -> Optional[List[Dict]]:
        """Get jokes by category"""
        url = f"{self.base_url}/jokes/{category}/ten"
        data = self.client.make_request(url)
        
        if data and isinstance(data, list):
            return data[:count]
        return None
    
    def display_joke(self, joke_data: Dict):
        """Display a single joke"""
        if not joke_data:
            print(" No joke to display")
            return
        
        setup = joke_data.get('setup', '')
        punchline = joke_data.get('punchline', '')
        joke_type = joke_data.get('type', 'general')
        
        print(f"\n JOKE ({joke_type.upper()})")
        print("=" * 40)
        print(f"{setup}")
        print(f" {punchline}")

def get_api_choice():
    """Get user choice for API to use"""
    print("\n API Integration - Choose an API to interact with:")
    print("1.   Weather API (wttr.in)")
    print("2.  Cryptocurrency API (CoinGecko)")
    print("3.  Demo Posts API (JSONPlaceholder)")
    print("4.  Joke API (Official Joke API)")
    print("5.  Custom API request")
    
    while True:
        choice = input("Enter your choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

def main():
    """Main function"""
    print(" Welcome to the API Integration Demo!")
    print("This tool demonstrates how to interact with various external APIs.")
    
    choice = get_api_choice()
    
    try:
        if choice == '1':
            # Weather API
            weather_api = WeatherAPI()
            location = input("\n  Enter city name (or 'London' for demo): ").strip() or "London"
            
            weather_data = weather_api.get_weather(location)
            if weather_data:
                weather_api.display_weather(weather_data, location)
            else:
                print(" Failed to fetch weather data")
        
        elif choice == '2':
            # Cryptocurrency API
            crypto_api = CryptocurrencyAPI()
            
            print("\nChoose option:")
            print("1. Get prices for popular coins")
            print("2. Get trending coins")
            print("3. Get prices for specific coins")
            
            crypto_choice = input("Enter choice (1-3): ").strip()
            
            if crypto_choice == '1':
                price_data = crypto_api.get_coin_prices()
                if price_data:
                    crypto_api.display_prices(price_data)
            
            elif crypto_choice == '2':
                trending_data = crypto_api.get_trending_coins()
                if trending_data:
                    crypto_api.display_trending(trending_data)
            
            elif crypto_choice == '3':
                coins_input = input("Enter coin names (comma-separated, e.g., 'bitcoin,ethereum'): ").strip()
                if coins_input:
                    coins = [coin.strip() for coin in coins_input.split(',')]
                    price_data = crypto_api.get_coin_prices(coins)
                    if price_data:
                        crypto_api.display_prices(price_data)
        
        elif choice == '3':
            # Demo Posts API
            news_api = NewsAPI()
            posts_data = news_api.get_demo_posts()
            if posts_data:
                news_api.display_posts(posts_data)
        
        elif choice == '4':
            # Joke API
            joke_api = JokeAPI()
            
            print("\nChoose option:")
            print("1. Random joke")
            print("2. Jokes by category")
            
            joke_choice = input("Enter choice (1-2): ").strip()
            
            if joke_choice == '1':
                joke_data = joke_api.get_random_joke()
                if joke_data:
                    joke_api.display_joke(joke_data)
            
            elif joke_choice == '2':
                categories = ["general", "programming", "dad", "knock-knock"]
                print(f"Available categories: {', '.join(categories)}")
                category = input("Enter category: ").strip().lower()
                
                if category in categories:
                    jokes_data = joke_api.get_jokes_by_category(category, 3)
                    if jokes_data:
                        for joke in jokes_data:
                            joke_api.display_joke(joke)
                            print()
                else:
                    print(" Invalid category")
        
        elif choice == '5':
            # Custom API request
            client = APIClient()
            
            print("\n Custom API Request")
            url = input("Enter API URL: ").strip()
            
            if not url:
                print(" URL is required")
                return
            
            method = input("Enter HTTP method (GET/POST) [GET]: ").strip().upper() or "GET"
            
            params = {}
            params_input = input("Enter query parameters (key=value,key2=value2) [optional]: ").strip()
            if params_input:
                try:
                    for param in params_input.split(','):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            params[key.strip()] = value.strip()
                except Exception as e:
                    print(f" Error parsing parameters: {e}")
            
            # Add headers if needed
            headers = {}
            if input("Do you need to add custom headers? (y/n): ").lower().startswith('y'):
                headers_input = input("Enter headers (key=value,key2=value2): ").strip()
                try:
                    for header in headers_input.split(','):
                        if '=' in header:
                            key, value = header.split('=', 1)
                            headers[key.strip()] = value.strip()
                except Exception as e:
                    print(f" Error parsing headers: {e}")
            
            print(f"\n Making {method} request to {url}")
            if params:
                print(f"Parameters: {params}")
            if headers:
                print(f"Headers: {headers}")
            
            response_data = client.make_request(url, method, params, headers)
            
            if response_data:
                print("\n RESPONSE:")
                print("=" * 50)
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
            else:
                print(" Failed to get response")
    
    except KeyboardInterrupt:
        print("\n\n API session interrupted by user")
    except Exception as e:
        print(f" An unexpected error occurred: {e}")
    
    print("\n API integration session completed!")

if __name__ == "__main__":
    main()


