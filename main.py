import cv2

# Function to get image properties
def define_image_properties(image_path):
    image = cv2.imread(image_path)
    return image, image.shape[0], image.shape[1]


# Function to convert a text message into binary format
def text_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)


# Function to convert binary data to text
def binary_to_text(binary_data):
    chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(byte, 2)) for byte in chars])


# Function to encode the message into the image
def encode_text_in_image(image_path, message, output_image_path):
    image, rows, columns = define_image_properties(image_path)
    binary_message = text_to_binary(message) + '1111111111111110'  # Add a delimiter to end the message
    binary_index = 0

    for row in range(rows):
        for col in range(columns):
            for color in range(3):  # Iterate over each color channel (B, G, R)
                if binary_index < len(binary_message):
                    # Replace LSB with message bit
                    image[row, col][color] = int(bin(image[row, col][color])[:-1] + binary_message[binary_index], 2)
                    binary_index += 1

    cv2.imwrite(output_image_path, image)
    print("Message encoded and saved to", output_image_path)


# Function to decode the message from the image
def decode_text_from_image(image_path):
    image, rows, columns = define_image_properties(image_path)
    binary_data = ""

    for row in range(rows):
        for col in range(columns):
            for color in range(3):
                binary_data += (bin(image[row, col][color])[-1])  # Extract the LSB

    # Split by the delimiter '1111111111111110' to stop
    message_bits = binary_data.split('1111111111111110')[0]
    return binary_to_text(message_bits)


# Example usage
if __name__ == "__main__":
    file = open("fun.txt", 'r')
    poem = file.read()
    encode_text_in_image("./test.png", poem, "encoded_image2.png")
    decoded_message = decode_text_from_image("encoded_image2.png")
    print("Decoded Message:", decoded_message)