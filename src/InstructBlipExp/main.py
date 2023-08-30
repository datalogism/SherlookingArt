import math
import os

from transformers import (InstructBlipProcessor,
                          InstructBlipForConditionalGeneration, AutoTokenizer)
import torch
import json
from PIL import Image
from urllib.request import urlopen

import urllib.request
import requests



Image.MAX_IMAGE_PIXELS = None
with open("dict_data.json", 'r') as f:
        data = json.load(f)

qnodes = ['Q4657634',
 'Q3794124',
 'Q1133821',
 'Q920030',
 'Q3642171',
 'Q2734892',
 'Q2900098',
 'Q3948607',
 'Q185255',
 'Q2470123',
 'Q604761',
 'Q28494210',
 'Q644936',
 'Q510799',
 'Q21204853',
 'Q11880391',
 'Q4009226',
 'Q766212',
 'Q6494773',
 'Q3849979',
 'Q3349704',
 'Q2715302',
 'Q3172226',
 'Q1231009',
 'Q3089617',
 'Q3119110',
 'Q2070487',
 'Q29530',
 'Q1988152',
 'Q481454',
 'Q334138',
 'Q2318957',
 'Q4429116',
 'Q683274',
 'Q14127232',
 'Q5659824',
 'Q9372005',
 'Q1167178',
 'Q3842509',
 'Q389198',
 'Q596677',
 'Q5712837',
 'Q493792',
 'Q1103170',
 'Q6163337',
 'Q1913390',
 'Q7973323',
 'Q1213936',
 'Q644106',
 'Q2354033']

print()
properties = ['movement', 'creator']
prompt_dict = {}
prompt_dict['movement'] = ("Which movement would an art historian say that "
                           "this painting belongs to?")
prompt_dict['creator'] = ("An art historian would say that this painting was "
                          "painted by which artist?")
context_list = ['context', 'no_context']
for property in properties:
    p = os.path.join(os.getcwd(),property)
    if not os.path.exists(p):
        os.mkdir(p)
        for con in context_list:
            if not os.path.exists(os.path.join(p,con)):
                os.mkdir(os.path.join(p,con))


#
model = InstructBlipForConditionalGeneration.from_pretrained(
    "Salesforce/instructblip-flan-t5-xl")
processor = InstructBlipProcessor.from_pretrained(
    "Salesforce/instructblip-flan-t5-xl")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# for idx,datapoint in enumerate(data):
#         url = datapoint['pic']
#         img = Image.open(urlopen(url))
for property in properties:
    for c in context_list:
        with (open(os.path.join(os.path.join(os.path.join(os.getcwd(),
                                                        property),c),"res.csv"),
                  'w+') as f):
            for node in qnodes:
                datapoint = data[node]
                url = datapoint['pic']
                img = Image.open(urlopen(url))
                if img.size[0] > 2000:
                        ratio = math.ceil(img.size[0]/2000)
                        img = img.resize((img.size[0]//ratio, img.size[1]//ratio))
                elif img.size[1]>2000:
                        ratio = math.ceil(img.size[1]/2000)
                        img = img.resize((img.size[0] // ratio, img.size[1] // ratio))

                # image = Image.open("ocb.jpg").convert("RGB")
                if c == 'no_context':
                    prompt = (f'{prompt_dict[property]}')
                    inputs = processor(images=img, text=prompt,
                                       return_tensors="pt").to(
                        device)

                    outputs = model.generate(
                        **inputs,
                        do_sample=False,
                        num_beams=5,
                        max_length=100,
                        min_length=1,
                        top_p=0.9,
                        repetition_penalty=1.5,
                        length_penalty=1.0,
                        temperature=1,
                    )
                    generated_text = \
                    processor.batch_decode(outputs, skip_special_tokens=True)[
                        0].strip()
                    print("GENERATED:" + generated_text)
                    actual = datapoint['props'][property]
                    f.write(node + "\t" + prompt + "\t" + generated_text +
                        "\t" + str(actual) + "\n")
                else:
                    prompt = (f'The supplied image, '
                              f'{datapoint["wiki_abs"]}'
                              f'{prompt_dict[property]}')
                    context_shorter = datapoint["wiki_abs"]

                    while True:
                        generated_text = ""
                        try:
                            inputs = processor(images=img, text=prompt,
                                               return_tensors="pt").to(
                                device)

                            outputs = model.generate(
                                **inputs,
                                do_sample=False,
                                num_beams=5,
                                max_length=100,
                                min_length=1,
                                top_p=0.9,
                                repetition_penalty=1.5,
                                length_penalty=1.0,
                                temperature=0,
                            )
                            generated_text = processor.batch_decode(outputs,
                                                                    skip_special_tokens=True)[
                                0].strip()
                            print("GENERATED:" + generated_text)
                            actual = datapoint['props'][property]
                            f.write(
                                node + "\t" + prompt + "\t" + generated_text +
                                "\t" + str(actual) + "\n")
                        except:


                            context_shorter = ".".join(
                                [part for part in context_shorter.split(".") if
                                 part != ""][:-1])
                            prompt = (
                                f'The supplied image, '
                                f'{context_shorter}.'
                                f'.{prompt_dict[property]}')
                        if len(generated_text) > 0:
                            break








