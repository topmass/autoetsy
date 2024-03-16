EXAMPLES TO USE FOR REFERENCE OF PROPER api STRUCTURE:

text to image
import requests
import json

# Vincent diagram example
host = "http://127.0.0.1:8888"

def text2img(params: dict) -> dict:
    """
    Vincentian picture
    """
    result = requests.post(url=f"{host}/v1/generation/text-to-image",
                           data=json.dumps(params),
                           headers={"Content-Type": "application/json"})
    return result.json()

result =text2img(
        {"prompt": "1girl sitting on the ground",
         "async_process": True}
    )
print(result)
upscale or vary
import requests
import json


# upscale or vary v1 Interface example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()

def upscale_vary(image, params: dict) -> dict:
    """
    Upscale or Vary
    """
    response = requests.post(url=f"{host}/v1/generation/image-upscale-vary",
                        data=params,
                        files={"input_image": image})
    return response.json()

result =upscale_vary(image=image,
                     params={
                         "uov_method": "Upscale (2x)",
                         "async_process": True
                     })
print(json.dumps(result, indent=4, ensure_ascii=False))
import requests
import json
import base64


# upscale or vary v2 Interface example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()

def upscale_vary(params: dict) -> dict:
    """
    Upscale or Vary
    """
    response = requests.post(url=f"{host}/v2/generation/image-upscale-vary",
                        data=json.dumps(params),
                        headers={"Content-Type": "application/json"},
                        timeout=300)
    return response.json()

result =upscale_vary(params={
                         "input_image": base64.b64encode(image).decode('utf-8'),
                         "uov_method": "Upscale (2x)",
                         "async_process": True
                     })
print(json.dumps(result, indent=4, ensure_ascii=False))
inpaint or outpaint
import requests
import json

# Partial redraw v1 interface example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()

def inpaint_outpaint(params: dict, input_image: bytes, input_mask: bytes = None) -> dict:
    """
    Partial redraw v1 interface example
    """
    response = requests.post(url=f"{host}/v1/generation/image-inpaint-outpaint",
                        data=params,
                        files={"input_image": input_image,
                               "input_mask": input_mask})
    return response.json()


# Image extension example
result = inpaint_outpaint(params={
                            "outpaint_selections": "Left,Right",
                            "async_process": True},
                          input_image=image,
                          input_mask=None)
print(json.dumps(result, indent=4, ensure_ascii=False))
#Partial redraw example
source = open("./imgs/s.jpg", "rb").read()
mask = open("./imgs/m.png", "rb").read()
result = inpaint_outpaint(params={
                            "prompt": "a cat",
                            "async_process": True},
                          input_image=source,
                          input_mask=mask)
print(json.dumps(result, indent=4, ensure_ascii=False))
import requests
import json
import base64


# Partial redraw v2 interface example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()

def inpaint_outpaint(params: dict) -> dict:
    """
    Partial redraw v2 interface example
    """
    response = requests.post(url=f"{host}/v2/generation/image-inpaint-outpaint",
                        data=json.dumps(params),
                        headers={"Content-Type": "application/json"})
    return response.json()

# Image extension example
result = inpaint_outpaint(params={
                            "input_image": base64.b64encode(image).decode('utf-8'),
                            "input_mask": None,
                            "outpaint_selections": ["Left", "Right"],
                            "async_process": True})
print(json.dumps(result, indent=4, ensure_ascii=False))
# Partial redraw example
source = open("./imgs/s.jpg", "rb").read()
mask = open("./imgs/m.png", "rb").read()
result = inpaint_outpaint(params={
                            "prompt": "a cat",
                            "input_image": base64.b64encode(source).decode('utf-8'),
                            "input_mask": base64.b64encode(mask).decode('utf-8'),
                            "async_process": True})
print(json.dumps(result, indent=4, ensure_ascii=False))
image prompts
import requests
import json


# image_prompt v1 Interface example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()
source = open("./imgs/s.jpg", "rb").read()
mask = open("./imgs/m.png", "rb").read()

def image_prompt(params: dict,
                 input_image: bytes=None,
                 input_mask: bytes=None,
                 cn_img1: bytes=None,
                 cn_img2: bytes=None,
                 cn_img3: bytes=None,
                 cn_img4: bytes=None,) -> dict:
    """
    image prompt
    """
    response = requests.post(url=f"{host}/v1/generation/image-prompt",
                             data=params,
                             files={
                                 "input_image": input_image,
                                 "input_mask": input_mask,
                                 "cn_img1": cn_img1,
                                 "cn_img2": cn_img2,
                                 "cn_img3": cn_img3,
                                 "cn_img4": cn_img4,
                              })
    return response.json()

# image extension
params = {
    "outpaint_selections": ["Left", "Right"],
    "image_prompts": [] # Required parameters, can be an empty list
}
result = image_prompt(params=params, input_iamge=image)
print(json.dumps(result, indent=4, ensure_ascii=False))
# partial redraw

params = {
    "prompt": "1girl sitting on the chair",
    "image_prompts": [], # Required parameters, can be an empty list
    "async_process": True
}
result = image_prompt(params=params, input_iamge=source, input_mask=mask)
print(json.dumps(result, indent=4, ensure_ascii=False))
# image prompt

params = {
    "prompt": "1girl sitting on the chair",
    "image_prompts": [
        {
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        },{
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        }]
    }
result = image_prompt(params=params, cn_img1=image, cn_img2=source)
print(json.dumps(result, indent=4, ensure_ascii=False))
import requests
import json
import base64

# image_prompt v2 Interface example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()
source = open("./imgs/s.jpg", "rb").read()
mask = open("./imgs/m.png", "rb").read()

def image_prompt(params: dict) -> dict:
    """
    image prompt
    """
    response = requests.post(url=f"{host}/v2/generation/image-prompt",
                             data=json.dumps(params),
                             headers={"Content-Type": "application/json"})
    return response.json()

# image extension
params = {
    "input_image": base64.b64encode(image).decode('utf-8'),
    "outpaint_selections": ["Left", "Right"],
    "image_prompts": [] # Required parameters, can be an empty list
}
result = image_prompt(params)
print(json.dumps(result, indent=4, ensure_ascii=False))
# partial redraw

params = {
    "prompt": "1girl sitting on the chair",
    "input_image": base64.b64encode(source).decode('utf-8'),
    "input_mask": base64.b64encode(mask).decode('utf-8'),
    "image_prompts": [], # Required parameters, can be an empty list
    "async_process": True
}
result = image_prompt(params)
print(json.dumps(result, indent=4, ensure_ascii=False))
# image prompt

params = {
    "prompt": "1girl sitting on the chair",
    "image_prompts": [
        {
            "cn_img": base64.b64encode(source).decode('utf-8'),
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        },{
            "cn_img": base64.b64encode(image).decode('utf-8'),
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        }]
    }
result = image_prompt(params)
print(json.dumps(result, indent=4, ensure_ascii=False))
text to image with imageprompt
import requests
import json
import base64

# text to image with imageprompt Example
host = "http://127.0.0.1:8888"
image = open("./imgs/bear.jpg", "rb").read()
source = open("./imgs/s.jpg", "rb").read()
def image_prompt(params: dict) -> dict:
    """
    image prompt
    """
    response = requests.post(url=f"{host}/v2/generation/text-to-image-with-ip",
                             data=json.dumps(params),
                             headers={"Content-Type": "application/json"})
    return response.json()

params = {
    "prompt": "A bear",
    "image_prompts": [
        {
            "cn_img": base64.b64encode(source).decode('utf-8'),
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        },{
            "cn_img": base64.b64encode(image).decode('utf-8'),
            "cn_stop": 0.6,
            "cn_weight": 0.6,
            "cn_type": "ImagePrompt"
        }
    ]
}
result = image_prompt(params)
print(json.dumps(result, indent=4, ensure_ascii=False))
describe
import requests

image = open("./imgs/bear.jpg", "rb").read()
def describe_image(image: bytes,
                   params: dict = {"type": "Photo"}) -> dict:
    """
    describe-image
    """
    response = requests.post(url="http://127.0.0.1:8888/v1/tools/describe-image",
                        params=params,
                        files={
                            "image": image
                        },
                        timeout=30)
    return response.json()

describe_image(image=image)