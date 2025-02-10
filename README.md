# Product Scraper

A simple web scraper built using FastAPI that allows users to scrape product data.
[https://whimsical.com/scraper-UpxADUJS7LnjbcBeMEn7H](Link to design)

## Setup Instructions

Follow these steps to set up and run the scraper:

1. **Set up and run Redis:**
   ```bash
   redis-server
   ```

2. **Set up a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   fastapi dev main.py
   ```

## API Usage

The scraper provides a single API endpoint to initiate a scraping operation.

### Endpoint: `/scrape`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body Parameters:**
  - `page_count` (optional, integer): Number of pages to scrape.
  - `proxy` (optional, string): Proxy URL to use for scraping.

### Example Request
```bash
curl --location 'http://127.0.0.1:8000/scrape' \
--header 'Content-Type: application/json' \
--data '{
  "page_count": 12
}'
```

## License
This project is licensed under the MIT License.


# Product Scraper

A simple web scraper built using FastAPI that allows users to scrape product data with optional parameters for proxy usage and page count.

## Setup Instructions

Follow these steps to set up and run the scraper:

1. **Set up and run Redis:**
   ```bash
      redis-server
         ```

         2. **Set up a virtual environment and activate it:**
            ```bash
               python -m venv venv
                  source venv/bin/activate  # On macOS/Linux
                     venv\Scripts\activate  # On Windows
                        ```

                        3. **Install dependencies:**
                           ```bash
                              pip install -r requirements.txt
                                 ```

                                 4. **Start the FastAPI server:**
                                    ```bash
                                       fastapi dev main.py
                                          ```

## API Usage

The scraper provides a single API endpoint to initiate a scraping operation.

### Endpoint: `/scrape`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - **Body Parameters:**
    - `page_count` (optional, integer): Number of pages to scrape.
      - `proxy` (optional, string): Proxy URL to use for scraping.

### Example Request
```bash
curl --location 'http://127.0.0.1:8000/scrape' \
--header 'Content-Type: application/json' \
--data '{
      "page_count": 12
}'
```

## License
This project is licensed under the MIT License.


