def check_price(file_path, new_price, baseline_price=584.0):
    try:
        with open(file_path, 'r') as f:
            old_price = float(f.read().strip())
    except FileNotFoundError:
        old_price = baseline_price
    except ValueError:
        old_price = baseline_price

    if new_price != old_price:
        with open(file_path, 'w') as f:
            f.write(str(new_price))
        return True
    else:
        return False