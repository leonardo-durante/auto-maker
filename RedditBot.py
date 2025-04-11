import praw
import requests
import os
import logging
from dotenv import load_dotenv
from PIL import Image

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

    def get_images(self, sub_name='memes', limit=10, feed_type='hot'):
        """
        Scrapes Reddit for memes and saves them in a folder
        
        Args:
            sub_name (str): The subreddit name to scrape images from
            limit (int): Maximum number of posts to fetch
            feed_type (str): Type of feed to fetch ('hot', 'new', 'top', 'rising')
            
        Returns:
            bool: True if images were downloaded successfully, False otherwise
        """
        try:
            # Create directory for images if it doesn't exist
            if os.path.exists('images'):
                logging.info("Images directory already exists, cleaning it up first")
                for file in os.listdir('images'):
                    if file.endswith('.jpg'):
                        os.remove(os.path.join('images', file))
            else:
                os.makedirs('images')
                logging.info("Created images directory")
            
            # Get subreddit instance
            sub = self.reddit.subreddit(sub_name)
            
            # Counter for naming images and tracking successful downloads
            n = 1
            downloaded_count = 0
            
            # Iterate through posts in the subreddit based on feed_type
            logging.info(f"Fetching {feed_type} posts from r/{sub_name}...")
            
            # Select feed based on feed_type
            if feed_type == 'new':
                posts = sub.new(limit=limit)
            elif feed_type == 'top':
                posts = sub.top(limit=limit)
            elif feed_type == 'rising':
                posts = sub.rising(limit=limit)
            else:  # Default to 'hot'
                posts = sub.hot(limit=limit)
                
            for post in posts:
                url = post.url
                
                # Download images (JPG, PNG, JPEG)
                if url.endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        # Download the image
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()  # Raise exception for HTTP errors
                        
                        # Extract extension and save the image
                        extension = url.split('.')[-1]
                        image_path = f'images/img{n}.{extension}'
                        
                        with open(image_path, 'wb') as handler:
                            handler.write(response.content)
                            logging.info(f"Downloaded image {n}: {url}")
                            n += 1
                            downloaded_count += 1
                            
                        # If the image is not a jpg but we need jpg for video creation, convert it
                        if extension != 'jpg':
                            img = Image.open(image_path)
                            img = img.convert('RGB')  # Convert to RGB to ensure compatibility
                            jpg_path = f'images/img{n-1}.jpg'
                            img.save(jpg_path)
                            logging.info(f"Converted {extension} to jpg: {jpg_path}")
                            # Remove the original non-jpg file
                            os.remove(image_path)
                            
                    except requests.exceptions.RequestException as e:
                        logging.warning(f"Failed to download image from {url}: {str(e)}")
            
            # Check if we were able to download any images
            if downloaded_count == 0:
                logging.warning(f"No images found in the first {limit} posts of r/{sub_name}")
                # Create a placeholder image to avoid errors in video creation
                placeholder_path = 'images/placeholder.jpg'
                try:
                    # Create a simple colored placeholder image
                    placeholder = Image.new('RGB', (800, 600), color=(33, 33, 33))
                    # Add text to the image
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(placeholder)
                    # Try to use a default font
                    try:
                        font = ImageFont.truetype("arial.ttf", 40)
                    except:
                        font = ImageFont.load_default()
                    
                    text = f"No images found in r/{sub_name}"
                    text_width = draw.textlength(text, font=font)
                    draw.text(((800-text_width)/2, 280), text, fill=(255, 255, 255), font=font)
                    
                    # Save the placeholder
                    placeholder.save(placeholder_path)
                    logging.info(f"Created placeholder image: {placeholder_path}")
                    return True
                except Exception as e:
                    logging.error(f"Failed to create placeholder image: {str(e)}")
                    return False
                
            logging.info(f"Successfully downloaded {downloaded_count} images from r/{sub_name}")
            return True
            
        except praw.exceptions.PRAWException as e:
            logging.error(f"Reddit API error: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Error downloading images: {str(e)}")
            return False