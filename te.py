import gzip
import base64

# Original data
data = "https://9jarocks.net/videodownload/wura-season-2-id284328.html"

# Compress the data using gzip
compressed_data = gzip.compress(data.encode())

# Encode the compressed data using base64
encoded_data = base64.b64encode(compressed_data).decode()

# Decode the compressed data using base64 and then decompress using gzip
decoded_compressed_data = gzip.decompress(base64.b64decode(encoded_data)).decode()

print("Original data size:", len(data))
print("Encoded data size:", len(encoded_data))
print("Compressed data:", len(compressed_data))
print("Decoded compressed data:", decoded_compressed_data)
