import numpy as np
import tensorflow as tf
from src.utils import normalize_en, normalize_vi


def load_dataset(path):
    with open(path, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
    print(f"Loaded from {path}: {len(sentences)} sentences")
    return sentences


def preprocess_data(sentences, lang):
    n = len(sentences)
    if lang == 'en':
        for i in range(n):
            sentences[i] = normalize_en(sentences[i])
    elif lang == 'vi':
        for i in range(n):
            sentences[i] = normalize_vi(sentences[i])
    else:
        raise ValueError(f"lang: {lang} not supported")


def filter_long_pairs(source_sentences, target_sentences, size=None, threshold=40):
    train_src = []
    train_tar = []
    max_sentences = len(source_sentences)

    n = 0
    for i in range(max_sentences):
        if len(source_sentences[i].split()) <= threshold:
            train_src.append(source_sentences[i])
            train_tar.append(target_sentences[i])
            n += 1
            if n == size:
                break

    return train_src, train_tar


def make_dataset(source, target, batch_size):
    size = len(source)

    return (
        tf.data.Dataset
        .from_tensor_slices((source, target))
        .shuffle(size)
        .batch(batch_size))
