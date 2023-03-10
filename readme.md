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

# Change user agent from settings of the project folder

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
