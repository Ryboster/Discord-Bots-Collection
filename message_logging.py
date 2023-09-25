from PIL import Image, ImageDraw, ImageFont
import requests
import time
import re
import discord
import emojis

def create_user_message_image(username, avatar_url, message_content, *args):
    attachment_urls = False
    attachments_list = False

    if args:
        print(f'{len(args)} arguments received')
        if 'attachments' in str(args[0]).split('/'):
            attachment_urls = args[0]
            print(args)
    # Calculate image height
    lines = []
    current_line = ""
    draw = ImageDraw.Draw(Image.new('RGB', (400, 400), color='#36393e'))
    font = ImageFont.truetype("arial.ttf", 16)
    word_list = []
    for word in message_content.split():
        if len(word) > 32:
            y = [word[i:i + 32] for i in range(0, len(word), 32)]
            print('y:', y)
            for part_of_word in y:
                word_list.append(part_of_word)
                print(f'part_of_word: {part_of_word}({len(part_of_word)})')
        else:
            word_list.append(word)

    for word in word_list:
        print('word:', word)
        text_size = draw.textsize(current_line + word, font=font)
        if text_size[0] <= 300:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    size_of_lines = 0
    print('lines:', lines)
    temp_list = []
    temp_str = ''
    for line in lines:
        size_of_lines += 16

    print('lines:', lines)
    frame_height = 100 + size_of_lines

    if attachment_urls:
        collective_width = 0
        collective_height = 0
        attachment_position = (10, 100)
        x_position, y_position = attachment_position
        attachments_list = []
        y = 0
        for url in attachment_urls:
            attachment = Image.open(requests.get(url, stream=True).raw)
            attachment_width, attachment_height = attachment.size
            new_attachment_width = 150
            new_attachment_height = int(attachment_height * (new_attachment_width / attachment_width))

            collective_width += new_attachment_width
            resized_image = attachment.resize((new_attachment_width, new_attachment_height), Image.LANCZOS)
            print(f'collective width: {collective_width}')
            print(f"x position: {x_position}")

            if y != 0:
                x_position += collective_width
            else:
                collective_height += new_attachment_height
                collective_width = 0

            if collective_width >= 400 or x_position >= 400:
                print(f'collective width or x position is higher than 400, {y}')
                y_position += new_attachment_height
                collective_height += new_attachment_height
                x_position = 10
                resized_image = attachment.resize((new_attachment_width, new_attachment_height), Image.LANCZOS)
                attachments_list.append((resized_image, (x_position, y_position)))
                # x_position += collective_width
                collective_width = 0
                continue

            attachments_list.append((resized_image, (x_position, y_position)))
            y += 1

        frame_height += collective_height

    frame_width = 400
    print(f'image width: {frame_width}\nimage height: {frame_height}')
    # Create an image
    image = Image.new('RGB', (frame_width, frame_height), color='#36393e')
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    # Choose a font and size
    font = ImageFont.load_default()
    font_size = 16
    font = ImageFont.truetype("arial.ttf", font_size)

    # Set text position
    username_position = (100, 10)
    avatar_position = (10, 10)
    message_position = (100, 40)
    # Load the user's avatar
    avatar = Image.open(requests.get(avatar_url, stream=True).raw)
    avatar = avatar.resize((80, 80))

    # Paste the avatar onto the image
    image.paste(avatar, avatar_position)
    if attachments_list:
        print(attachments_list)
        for picture, position in attachments_list:
            image.paste(picture, position)

    # Write the username to the image
    draw.text(username_position, username, fill='white', font=font)

    message_height = 0
    for line in lines:
        print(line)
        draw.text(message_position, line, fill='white', font=font)
        message_height += font_size
        message_position = (message_position[0], message_position[1] + font_size)
    return image