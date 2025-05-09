import requests


def create_payment(amount, description):
    headers = {
        'Authorization': f'Basic {YOO_KASSA_API_KEY}',
        'Content-Type': 'application/json',
    }

    payment_data = {
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://yourwebsite.com/return"  # URL для возврата после оплаты
        },
        "description": description,
        "capture": True,
    }

    response = requests.post(YOO_KASSA_API_URL, json=payment_data, headers=headers)
    return response.json()
