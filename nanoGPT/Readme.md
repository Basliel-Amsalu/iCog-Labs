# nanoGPT

nanoGPT is a minimalistic implementation of GPT (Generative Pre-trained Transformer) trained on amharic news dataset. This project aims to provide a simple and clear understanding of how GPT models work.

## Features
- Basic implementation of GPT architecture
- Easy to understand and exten

# Steps involved in this project
- preprocessing an Amharic news data to get the proper format of the needed data
- tokenizing the data (it is tokenized in a character level vocabulary since this a character level transformet that predicts the next character using the precedding characters)
- embedding the tokens
- training a neural network
- implementing self attention (taken from the attention is all you need paper to give the model a sense of space in addition to token which means letting the character token communicate what it has, where it is, what it wants and what it will communicate.)
- adding MLP.
- generating an output and writing it to a file to see the final product of the the transformer.

## Usage
To get started with nanoGPT, clone the repository: then

```bash
cd nanoGPT
python gpt.py
```

