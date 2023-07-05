import json
import requests
import pandas as pd
import ast
import re

df = pd.read_csv("Q3_HK_queries.csv", header=None)

items_list = []

url_hk = "https://deliveroo.hk/en/restaurants/hong-kong/times-square?geohash=wecnwr8u4q79&collection={}"

queries = []
vendornames = []
vendorurls = []

for index, row in df.iterrows():
    print ("now extracting row {}...".format(index))
    
    query = row[0]

    url = url_hk.format(query)

    resp = requests.get(url)
    
    data = re.search(r'{"results":{(.*?)"fulfillmentMethods"', resp.text)
    data = data.group(0).split(',"fulfillmentMethods"',1)[0]
    data = data+"}" # complete dictionary
    results = json.loads(data)

    res_len = len(results["results"]["data"][0]["blocks"])-1

    for i in range(0,res_len-1):

        resto = results["results"]["data"][0]["blocks"][i]["target"]

        if resto is not None and "restaurant" in resto:

            restaurant = resto["restaurant"]

            vendor_name = restaurant["name"]
            vendor_url = "https://deliveroo.hk/en" + restaurant["links"]["self"]["href"]

        else:

            vendor_name = "-"
            vendor_url = "-"

        vendornames.append(vendor_name)
        vendorurls.append(vendor_url)
        
        top_10_vendornames = vendornames[:10]
        top_10_vendorurls = vendorurls[:10]
        results_len = len(top_10_vendornames)

        ### Convert to lists ###
        queries.append(query)
        
# save as single file
deliveroo_resto = pd.DataFrame({
'query': queries,
'restaurant_names': vendornames,
'vendor_urls': vendorurls})
deliveroo_resto.to_csv("deliveroo_res.csv", index=False)