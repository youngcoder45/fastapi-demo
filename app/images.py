import os

from dotenv import load_dotenv
from imagekitio import ImageKit

load_dotenv()

IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL")

# Note: In imagekitio v5+, ImageKit() no longer accepts `public_key` or `url_endpoint`.
# The URL endpoint is provided to helper methods (e.g., `client.helper.build_url`).
imagekit = ImageKit(private_key=IMAGEKIT_PRIVATE_KEY)
