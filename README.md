docker run -d -p 6901:6901 -p 80:80 --name image_searcher google_images_download

docker build -t gpt_scraper .

python3 bing_scraper.py --search 'honeybees on flowers' --limit 3 --download

docker stop image_searcher && docker rm image_searcher
