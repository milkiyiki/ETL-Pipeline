def transform_products(products):
    transformed = []

    for product in products:
        try:
            price_usd = float(product['Price'].replace('$', '').strip())
            price_idr = price_usd * 16000
        except (ValueError, AttributeError, KeyError):
            price_idr = None

        try:
            rating = float(product['Rating'].split()[0])
        except (ValueError, AttributeError, KeyError):
            rating = None

        colors = ''.join(filter(str.isdigit, product.get('Colors', '')))
        size = product.get('Size', '').replace("Size: ", "").strip()
        gender = product.get('Gender', '').replace("Gender: ", "").strip()
        title = product.get('Title', '').strip()
        timestamp = product.get('Timestamp', '')

        # Masukkan hanya jika price dan rating valid
        if price_idr is not None and rating is not None:
            transformed.append({
                "Title": title,
                "Price": price_idr,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "Timestamp": timestamp
            })

    # Hilangkan duplikat berdasarkan Title
    seen = set()
    unique_products = []
    for p in transformed:
        if p['Title'] not in seen:
            seen.add(p['Title'])
            unique_products.append(p)

    return unique_products