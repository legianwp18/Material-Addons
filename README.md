# Material-Addons

## Material Addons Documentation API

* GET Request
```python
import requests

url = "http://127.0.0.1:8069/api/v1/get_product_material"

payload = {}
headers = {
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("GET", url, data=payload, headers=headers)
```

* POST Request
```python
import requests

url = "http://127.0.0.1:8069/api/v1/post_product_material"

payload = {
    'name': 'm4',
    'material_code': 'MC24',
    'material_type': 'Fabric',
    'material_buy_price': 200,
    'supplier_id': 14,
    'company_id': 1
}
headers = {
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers)
```

* PUT Request
```python
import requests

url = "http://127.0.0.1:8069/api/v1/put_product_material/4"

payload = {
    'material_buy_price': 500
}
headers = {
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("PUT", url, data=payload, headers=headers)
```

* DELETE Request
```python
import requests

url = "http://127.0.0.1:8069/api/v1/delete_product_material/4"

payload = {
    'material_buy_price': 500
}
headers = {
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("DELETE", url, data=payload, headers=headers)
```