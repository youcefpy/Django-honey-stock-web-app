import requests

BASE_URL = "https://aseel.ecomanager.dz/api/shop/v1/"
TOKEN = 'pRYrqd5XDIurdoNSw7rBiJ8vv8meKocZzsP6Uk4wR480KOnlFaNap5Bb6IbsAXEIm2NtOckJuLctfU5Z'
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

def GET_request(endpoint, params={}):
    response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
    if response.status_code != 200:
        print(f"GET Error: {response.json()}")
        return None
    return response.json()

def POST_request(endpoint, data={}):
    response = requests.post(BASE_URL + endpoint, headers=headers, json=data)
    if response.status_code != 200:
        print(f"POST Error: {response.json()}")
        return None
    return response.json()

# Implement PUT_request function
def PUT_request(endpoint, data={}):
    response = requests.put(BASE_URL + endpoint, headers=headers, json=data)
    if response.status_code != 200:
        print(f"PUT Error: {response.json()}")
        return None
    return response.json()

def get_product_by_sku(sku_code):
    products = GET_request("products")
    if not products:
        return None
    
    for product in products:
        if product.get("reference") == sku_code:
            return product
    return None


def increment_quantity_in_ecomanager(sku, increment_value):
    product = get_product_by_sku(sku.code)
    
    if not product:
        return

    updated_quantity = int(product["quantity"]) + increment_value
    payload = {"quantity": updated_quantity}
    
    # Use PUT_request to update the product
    update_response = PUT_request(f"/products/{sku.code}", data=payload)
    if not update_response:
        print(f"Failed to update product with SKU {sku.code}")
