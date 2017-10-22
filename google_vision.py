#!/usr/bin/env python3.6

from google.cloud import vision
import os

client = vision.ImageAnnotatorClient()
os.mkdir('vision')

for i in range(1, 3638):
    image_name = str(i).zfill(4)

    response = client.annotate_image({
        'image': {'source': {'image_uri': 'gs://monetize-bmw-png/{}.png'.format(image_name)}},
        'features': [{'type': vision.enums.Feature.Type.TEXT_DETECTION}],
    })

    with open('vision/{}.txt'.format(image_name), 'w') as out_file:
        out_file.write(response.full_text_annotation.text)

    print(i)
