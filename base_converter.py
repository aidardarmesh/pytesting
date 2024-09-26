def to_base_64(num):
    if num == 0:
        return '0'

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-."
    base = 64
    result = []

    while num > 0:
        remainder = num % base
        result.append(alphabet[remainder])
        num //= base

    return ''.join(result[::-1])  # Reverse the list to get the correct order


# Example usage
number = 123456
base_64_result = to_base_64(number)
print(base_64_result.zfill(6))
