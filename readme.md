# System requirements

    vscode build tool [download the installer and then run this command at cmd on that location, silent installer]
    vs_buildtools.exe --norestart --passive --downloadThenInstall --includeRecommended --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.MSBuildTools

    vcredistx64 [same ...]
    VC_redist.x64.exe  /q /norestart

    Scrapy
    pip install Scrapy

### Create python virtual environment

    python -m venv project_name

### Activate the virtual environment

    cd project_name/Script

#### run at this location

    Git bash
    . active

# Create a Scrapy project

    mkdir src
    cd src
    scrapy startproject project_name

## Generate Spider

    to view spider type
    scrapy genspider -l

    basic type
    scrapy genspider site_name site_url
    for crawl type
    scrapy genspider -t crawl site_name site_url

#### run spider [there will be a file created like site_name.py]

    go at the top of the project location then -->
    scrapy crawl site_name or spider_name
    if an output file
    scrapy crawl audible -o [add custome location if you want like ./..../]file_name.json or .csv

## Change user agent from settings of the project folder

    DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    or use this as custom way

    basic
    add this above parse func and remove start_urls from parse func

    def start_requests(self):
        scrapy.Request(url=link_you_want, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})

    if you use parse func in a loop you also need to add the headers to the parse from where you are calling for loop, not at the top parse func

    crawl
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X', headers={'user-agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths=(
            "//ul[@class=\"scripts-list\"]/a")), callback="parse_item", follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=(
            "(//a[@rel=\"next\"])[1]")), process_request='set_user_agent'),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return

# SQL

    <!-- To open database -->
    .OPEN database_name.db

    <!-- Create Table -->
    CREATE TABLE table_name(
        id INT,
        name TEXT,
    );

    <!-- Show Schema -->
    after opening the database #1
    .schema table_name

    <!-- Show table -->
    SELECT * from table_name

# Splash

    pip install scrapy-splash

Taken from ["https://github.com/scrapy-plugins/scrapy-splash"]

1. Add the Splash server address to settings.py of your Scrapy project like this:

   SPLASH_URL = 'http://localhost:8050/'

2. Enable the Splash middleware by adding it to DOWNLOADER_MIDDLEWARES in your settings.py file and changing HttpCompressionMiddleware priority:

   DOWNLOADER_MIDDLEWARES = {
   'scrapy_splash.SplashCookiesMiddleware': 723,
   'scrapy_splash.SplashMiddleware': 725,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
   }

3. Enable SplashDeduplicateArgsMiddleware by adding it to SPIDER_MIDDLEWARES in your settings.py:

   SPIDER_MIDDLEWARES = {
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
   }

4. Set a custom DUPEFILTER_CLASS:

   DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

#### Check with Scrapy

    <!-- Check it is connected or not use scrapy shell -->
    scrapy shell
    fetch('http://localhost:8050')

    <!-- check with url -->
    fetch('http://localhost:8050/render.html?url=https...')

# Aquarium

It's like a cluster of splashes [3]
liks: ["https://github.com/TeamHG-Memex/aquarium"]

1. Install [in linux] --> cd Documents
   pip install cookiecutter
2. Then generate a folder with config files:
   cookiecutter gh:TeamHG-Memex/aquarium
3. launch aquarium at the ./aquriam location
   docker-compose up

# Docker

#### to install splash

    docker pull scrapinghub/splash

    for linux // don't know which one, try all of them 🤣🤣
    sudo service docker start
    systemctl enable docker
    systemctl start docker
    sudo dockerd

    <!-- to stop it -->
    sudo systemctl stop docker && sudo systemctl stop docker.socket

    <!-- to check all container -->
    docker container ls

    <!-- run splash on a browser -->

    docker run -it -p 8050:8050 scrapinghub/splash

    <!-- for high memory usage restart it self -->
    docker run -it --restart always -p 8050:8050 scrapinghub/splash
