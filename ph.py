import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base = "https://www.producthunt.com/"

headers= {
    'content-type': 'application/json',
    'x-requested-with': 'XMLHttpRequest'
   }

url = 'https://www.producthunt.com'
data = requests.get(url,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

def page_title():
    # Snag Page Title
    pagetitle = soup.title.string
    print('\n Title: \n ',pagetitle.strip(), '\n Initialized from current page:','\n',url ,'\n')

product_images = []
product_links = []
product_data = []

target_layout = soup.find("main", attrs={"class": "layoutMain"})
target_layout_prod = target_layout.find("div", attrs={"data-test": "homepage-section-0"})

def target():
    for target_product in target_layout_prod:
        target_product_data = target_layout_prod.find("div", attrs={"class": "styles_item__Sn_12"})

        # get link text    
        target_product_info = target_product_data.findAll('a')        
        for product_info in target_product_info:
            if product_info:
                product_data.append(product_info.text)   
        # get images
        target_product_images = target_product_data.findAll('img')
        for imglink in target_product_images:
            if imglink.has_attr('src'):
                relative = imglink['src']
                alt_tag = imglink['alt']
                item_name = urljoin(base, relative)
                item_name = item_name.split('png')[0] + 'png'
                product_images.append(item_name)
                product_images.append(alt_tag)        
        # get links
        target_product_links = target_product_data.findAll('a')
        for link in target_product_links:
            if link.has_attr('href'):
                relative = link['href']
                item_name = urljoin(base, relative)
                product_links.append(item_name)              

        # clears empty strings within the list
        while("" in product_data):
            product_data.remove("")
                
        pd = 'product name/details: '
        pil = 'product image links/tags: '
        pl = 'product links: '
        print(pd, set(product_data))
        print(pil, set(product_images))
        print(pl, set(product_links))        
        
        product_name = set(product_data) & set(product_images)
        print(pd.replace('/details',''), product_name)
try:
    page_title()
    target()
except IndexError:
    pass


# OUTPUT
# ---------------------------------------------
#  Title:
#   Product Hunt – The best new products in tech.
#  Initialized from current page:
#  https://www.producthunt.com

# product name/details:  {'SaaS Library', 'Discover 100+ unique SaaS ideas that can be built with AI'}
# product image links/tags:  {'SaaS Library', 'https://ph-files.imgix.net/a2ee02f9-3d24-4593-bca3-5a7b0a243b86.png'}
# product links:  {'https://www.producthunt.com/r/p/374860', 'https://www.producthunt.com/posts/saas-library'}
# product name:  {'SaaS Library'}
# ---------------------------------------------
