docker run -d -p 80:80 --name image_searcher saitamatechno/google_images_download:v1.0

docker build -t google_images_download .

python3 bing_scraper.py --search 'honeybees on flowers' --limit 3 --download

docker stop image_searcher && docker rm image_searcher
