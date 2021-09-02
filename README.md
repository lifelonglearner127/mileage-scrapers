## Installation
In order to run the scraper successfully, we need to use pyvirtualdisplay
```commandline
sudo apt-get install xvfb xserver-xephyr tigervnc-standalone-server xfonts-base
git clone <repository-url>
poetry install
poetry shell
python -m src.aa
```
### How to use Selenium Grid
```commandline
docker-compose up -d
```

Set `use_grid` parameter to `True` to configure remote web drivers.
