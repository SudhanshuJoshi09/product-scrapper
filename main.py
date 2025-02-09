# from fastapi import FastAPI
# from contollers.scraper import scrape_router
# from contollers.users import user_router
#
#
# app = FastAPI()
# app.include_router(user_router)
# app.include_router(scrape_router)

from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, EmailStr
import redis
import json
import datetime
import requests
from bs4 import BeautifulSoup
import os
import time
from threading import Thread
from models import User, ScrapingRecord, Scheduler, Base

DATABASE_URL = "sqlite:///./scraper.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
redis_client = redis.Redis(host='localhost', port=6379,
                           db=0, decode_responses=True)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str


class ScrapeRequest(BaseModel):
    page_count: int = None
    proxy: str = None

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Services


class ScrapingService:
    def get_cached_or_file_data(self, page_number: int):
        cache_key = f"scraped_page_{page_number}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        filename = f"scraped_page_{page_number}.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return json.load(file)
        return None

    def scrape_page(self, page_number: int, proxy: str = None):
        url = f"https://dentalstall.com/shop/page/{page_number}/"
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(response.text, "html.parser")

        products = []
        for li in soup.find_all("li"):
            title_tag = li.find("h2", class_="woo-loop-product__title")
            price_tag = li.find("span", class_="woocommerce-Price-amount")
            image_tag = li.find("div", class_="mf-product-thumbnail").find(
                "img") if li.find("div", class_="mf-product-thumbnail") else None

            title = title_tag.get_text(strip=True) if title_tag else ""
            price = price_tag.get_text(strip=True) if price_tag else ""
            image_url = image_tag["src"] if image_tag else ""

            if title and price and image_url:
                products.append(
                    {"title": title, "price": price, "image_url": image_url})

        return products if response.status_code == 200 else None

    def scrape(self, req: ScrapeRequest, db: Session):
        product_list = []
        page_number = 1

        while req.page_count is None or page_number <= req.page_count:
            cached_data = self.get_cached_or_file_data(page_number)
            if cached_data:
                product_list.extend(cached_data)
            else:
                curr_product_list = self.scrape_page(page_number, req.proxy)
                if not curr_product_list:
                    record = ScrapingRecord(
                        page_number=page_number, status="failed")
                    db.add(record)
                    db.commit()
                    self.schedule_retry(db, record.id)
                    break
                product_list.extend(curr_product_list)

                # Store in database
                record = ScrapingRecord(
                    page_number=page_number, status="completed")
                db.add(record)
                db.commit()

                # Store in file
                with open(f"scraped_page_{page_number}.json", "w") as file:
                    json.dump(curr_product_list, file)

                # Store in cache
                redis_client.set(
                    f"scraped_page_{page_number}", json.dumps(curr_product_list))

            page_number += 1

        return {"products": product_list}

    def schedule_retry(self, db: Session, scraping_record_id: int):
        retry_entry = Scheduler(scraping_record=scraping_record_id,
                                execution_time=datetime.datetime.utcnow() + datetime.timedelta(minutes=5))
        db.add(retry_entry)
        db.commit()

# Background Scheduler


def process_failed_requests():
    while True:
        db = SessionLocal()
        failed_jobs = db.query(Scheduler).filter(
            Scheduler.status == "scheduled").all()
        for job in failed_jobs:
            record = db.query(ScrapingRecord).filter(
                ScrapingRecord.id == job.scraping_record).first()
            if record and record.status == "failed":
                service = ScrapingService()
                service.scrape(ScrapeRequest(page_count=1), db)
                record.status = "completed"
                job.status = "completed"
                db.commit()
        db.close()
        time.sleep(300)  # Runs every 5 minutes


Thread(target=process_failed_requests, daemon=True).start()

# FastAPI App Setup
app = FastAPI()


@app.post("/scrape")
def scrape_data(request: ScrapeRequest, db: Session = Depends(get_db)):
    service = ScrapingService()
    result = service.scrape(request, db)
    return result


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email,
                    password_hash=user.password_hash)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}
