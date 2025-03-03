import tweepy
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
from typing import List, Dict

class TrendService:
    def __init__(self, twitter_bearer_token: str):
        self.twitter_client = tweepy.Client(bearer_token=twitter_bearer_token)
        self.ai_accounts = [
            "choi.openai",
            "AndrewYNg",
            "ylecun",
            "sama",
            "jeffdean"
        ]
        
    def get_latest_ai_trends(self) -> Dict:
        """Get latest AI trends from Twitter and tech news sites"""
        trends = {
            "twitter_updates": self._get_twitter_updates(),
            "tech_news": self._get_tech_news(),
            "last_updated": datetime.now().isoformat()
        }
        return trends
        
    def _get_twitter_updates(self) -> List[Dict]:
        """Fetch latest tweets from AI thought leaders"""
        tweets = []
        for account in self.ai_accounts:
            try:
                user = self.twitter_client.get_user(username=account)
                if user.data:
                    recent_tweets = self.twitter_client.get_users_tweets(
                        user.data.id, 
                        max_results=5,
                        tweet_fields=['created_at', 'public_metrics']
                    )
                    if recent_tweets.data:
                        for tweet in recent_tweets.data:
                            tweets.append({
                                "author": account,
                                "text": tweet.text,
                                "created_at": tweet.created_at.isoformat(),
                                "metrics": tweet.public_metrics
                            })
            except Exception as e:
                print(f"Error fetching tweets for {account}: {str(e)}")
                continue
        
        return sorted(tweets, key=lambda x: x["created_at"], reverse=True)
        
    def _get_tech_news(self) -> List[Dict]:
        """Scrape latest AI news from tech websites"""
        news = []
        
        # TechCrunch AI section
        try:
            response = requests.get("https://techcrunch.com/category/artificial-intelligence/")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all('article', class_='post-block')
                for article in articles[:5]:
                    title = article.find('h2')
                    link = article.find('a')
                    if title and link:
                        news.append({
                            "source": "TechCrunch",
                            "title": title.text.strip(),
                            "url": link['href'],
                            "timestamp": datetime.now().isoformat()
                        })
        except Exception as e:
            print(f"Error scraping TechCrunch: {str(e)}")
            
        return news
