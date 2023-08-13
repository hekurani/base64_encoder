from base64_encoder import Base64

message = "Hello world!"
image_file = 'image.png'
video_file = 'video.mp4'

b64 = Base64(message, 'string')

encoded_output = b64.encode()
print("Encoded output: " + encoded_output)

b64.decode(encoded_output)
