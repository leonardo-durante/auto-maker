import praw
import requests
import os
import shutil
import logging
import sys
import random
import time
import argparse
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

class RedditBot:
    """
    A class to interact with Reddit API and download images from subreddits
    """
    
    def __init__(self):
        """Initialize the Reddit API connection using credentials from environment variables"""
        try:
            # Get the credentials from environment variables
            client_id = os.getenv('ID')
            client_secret = os.getenv('SECRET')
            user_agent = os.getenv('AGENT')
            
            # Check if credentials are available
            if not client_id or not client_secret or not user_agent:
                raise ValueError("Missing Reddit API credentials. Please check your .env file.")
            
            # Initialize the Reddit API connection
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
            )
            
            logging.info("Connected to Reddit API successfully")
            
        except praw.exceptions.PRAWException as e:
            logging.error(f"Reddit API connection error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error initializing RedditBot: {str(e)}")
            raise