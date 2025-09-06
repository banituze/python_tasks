# Level 2 - Intermediate Python Tasks

This directory contains three intermediate Python programming tasks that introduce external libraries, web interaction, and data persistence concepts.

## Task 1: To-Do List Application (`todo_list.py`)

A full-featured command-line to-do list manager with persistent JSON storage.

### Features:
- Add, delete, and mark tasks as complete/incomplete
- Task priorities (High, Medium, Low) with visual indicators
- Persistent JSON storage
- Search functionality
- Task filtering (by completion status, priority)
- Detailed statistics and analytics
- Data export/import capabilities
- Task descriptions and timestamps

### How to run:
```bash
python todo_list.py
```

### Main features:
```
 TO-DO LIST APPLICATION
==================================================
1.  Add task
2.  List all tasks
3.  Mark task as completed
4.  Mark task as pending
5.  Delete task
6.  Search tasks
7.  Show statistics
8.  Settings
9.  Exit
==================================================
```

### Example output:
```
 TO-DO LIST
============================================================
PENDING TASKS (3):
----------------------------------------
  [1]  Complete Python project
      Finish all three levels of tasks
  [2]  Buy groceries
      Milk, eggs, bread
  [3]  Call dentist

 COMPLETED TASKS (1):
----------------------------------------
  [4]  Review code

 SUMMARY: 3 pending, 1 completed (4 total)
```

### Data format (tasks.json):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete Python project",
      "description": "Finish all three levels of tasks",
      "completed": false,
      "priority": "high",
      "created_at": "2024-01-15T10:30:00",
      "completed_at": null
    }
  ],
  "next_id": 2,
  "last_saved": "2024-01-15T10:30:00"
}
```

## Task 2: Data Scraper (`data_scraper.py`)

A flexible web scraper that extracts data from websites and saves it to CSV format.

### Prerequisites:
```bash
pip install beautifulsoup4 requests
```

### Features:
- Multiple scraping modes (quotes, news, products, custom)
- Automatic HTML parsing with BeautifulSoup
- CSV output with proper formatting
- Rate limiting to be respectful to servers
- Error handling for network issues
- Support for various website structures

### How to run:
```bash
python data_scraper.py
```

### Scraping options:
```
 Web Scraper - Choose what to scrape:
1.  Quotes (quotes.toscrape.com - demo site)
2.  News headlines (from any news website)
3.  Product information (from e-commerce sites)
4.  Custom scraping
```

### Example usage:
```bash
# Scrape quotes from demo site
 Welcome to the Web Data Scraper!
Enter your choice (1-4): 1

 Scraping quotes from quotes.toscrape.com...
 Fetching: http://quotes.toscrape.com/page/1/
 Successfully fetched and parsed: http://quotes.toscrape.com/page/1/
 Found 10 quotes on page 1
 No more quotes found on page 11
 Scraped 100 quotes total
 Saved 100 items to quotes_20240115_143022.csv
```

### Output CSV format:
```csv
author,page,scraped_at,tags,text
Albert Einstein,1,2024-01-15T14:30:22,change world,Try not to become a person of success but rather try to become a person of value.
J.K. Rowling,1,2024-01-15T14:30:22,abilities choices,It is our choices Harry that show what we truly are far more than our abilities.
```

### Ethical scraping guidelines:
- Always check robots.txt
- Respect rate limits and don't overwhelm servers
- Follow website terms of service
- Only scrape publicly available information

## Task 3: API Integration (`api_integration.py`)

A comprehensive API client that demonstrates interaction with various external APIs.

### Prerequisites:
```bash
pip install requests
```

### Features:
- Weather data fetching (wttr.in)
- Cryptocurrency prices (CoinGecko API)
- Demo data (JSONPlaceholder)
- Joke API integration
- Custom API request tool
- Comprehensive error handling
- Request retries with exponential backoff

### How to run:
```bash
python api_integration.py
```

### Available APIs:
```
 API Integration - Choose an API to interact with:
1.   Weather API (wttr.in)
2.  Cryptocurrency API (CoinGecko)
3.  Demo Posts API (JSONPlaceholder)
4.  Joke API (Official Joke API)
5.  Custom API request
```

### Weather API example:
```
  WEATHER REPORT FOR LONDON
==================================================
  Temperature: 15°C (59°F)
 Feels like: 14°C (57°F)
  Condition: Partly cloudy
 Humidity: 78%
 Wind: 12 km/h WSW

 3-DAY FORECAST:
------------------------------
2024-01-15: 12°C - 18°C, Partly cloudy
2024-01-16: 10°C - 16°C, Light rain
2024-01-17: 14°C - 20°C, Sunny
```

### Cryptocurrency API example:
```
 CRYPTOCURRENCY PRICES (USD)
============================================================
Coin            Price           24h Change      Market Cap     
------------------------------------------------------------
Bitcoin         $43,250.50       +2.45%      $847.2B        
Ethereum        $2,580.75        -1.23%      $310.4B        
Dogecoin        $0.082150        +5.67%      $11.7B         
Litecoin        $72.40           -0.89%      $5.4B          
Cardano         $0.485600        +3.21%      $17.2B         
```

### Custom API requests:
The tool includes a flexible custom API client that allows you to:
- Make GET/POST requests to any endpoint
- Add custom headers and parameters
- Handle different response formats
- View formatted JSON responses

## Getting Started

### Prerequisites:
- Python 3.8 or higher
- Install required packages:
  ```bash
  pip install -r requirements.txt
  ```

### Requirements file content:
```
requests>=2.25.1
beautifulsoup4>=4.9.3
lxml>=4.6.3
```

### Running the tasks:

1. **To-Do List:**
   ```bash
   python todo_list.py
   ```

2. **Data Scraper:**
   ```bash
   # Install dependencies first
   pip install beautifulsoup4 requests
   python data_scraper.py
   ```

3. **API Integration:**
   ```bash
   # Install dependencies first  
   pip install requests
   python api_integration.py
   ```

## Learning Objectives

These intermediate tasks taught me:

### External Libraries:
- **requests**: HTTP requests and API interactions
- **beautifulsoup4**: HTML parsing and web scraping
- **json**: Data serialization and file storage
- **csv**: Structured data export
- **datetime**: Timestamp handling

### Programming Concepts:
- Object-oriented programming with classes
- Data persistence and file formats
- Error handling and network resilience
- Rate limiting and respectful API usage
- Data validation and sanitization

### Web Technologies:
- HTTP methods and status codes
- URL parsing and construction
- HTML parsing and CSS selectors
- REST API principles
- JSON data handling

### Software Design:
- Modular code organization
- Configuration management
- User interface design for CLI applications
- Data export/import functionality
- Comprehensive logging and feedback

## Extension Ideas

### For To-Do List:
- Add due dates and reminders
- Implement categories/projects
- Create web interface
- Add data synchronization
- Implement task templates

### For Data Scraper:
- Add support for JavaScript-rendered pages
- Implement proxy rotation
- Add data validation and cleaning
- Create scraping schedules
- Add database storage

### For API Integration:
- Add authentication handling
- Implement data caching
- Create API response visualization
- Add batch processing
- Implement API monitoring

## Common Issues and Solutions

1. **Network connectivity**: All tools include proper error handling for network issues
2. **Rate limiting**: Scraper includes delays between requests
3. **API key requirements**: Some APIs may require registration
4. **Data format changes**: Scrapers include multiple selectors for robustness
5. **File permissions**: Ensure write permissions for data files

## Security Considerations

- Never hardcode API keys or credentials
- Validate all user inputs
- Use secure HTTP (HTTPS) when available
- Respect website terms of service
- Handle sensitive data appropriately

These intermediate tasks prepared me for the advanced concepts in Level 3, including web frameworks, encryption, and complex algorithms.


