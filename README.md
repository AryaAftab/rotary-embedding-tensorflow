## Rotary Embeddings - Tensorflow

A standalone library for adding <a href="https://arxiv.org/abs/2104.09864">rotary embeddings</a> to transformers in Tesnorflow, following its success as <a href="https://blog.eleuther.ai/rotary-embeddings/">relative positional encoding</a>. Specifically it will make rotating information into any axis of a tensor easy and efficient, whether they be fixed positional or learned. This library will give you state of the art results for positional embedding, at little costs.

My gut also tells me there is something <a href="https://www.nature.com/articles/s41593-021-00821-9">more</a> to rotations that can be exploited in artificial neural networks.

## Note
An implemented version of Pytorch is available in this <a href="https://github.com/lucidrains/rotary-embedding-torch">repository</a>.

This version is written by converting to the version of Pytorch. 

The three functions of rearrange, irearrange and repeat have been written due to the incompatibility of the einops library with tensorflow 2.x.
## Install

```bash
$ pip install rotary-embedding-tensorflow
```

## Usage

```python
import tensorflow as tf
from rotary_embedding_tensorflow import apply_rotary_emb, RotaryEmbedding

# instantiate the positional embedding in your transformer and pass to all your attention layers

pos_emb = RotaryEmbedding(dim = 32)

# generate the rotations

freqs = pos_emb(tf.range(1024), cache_key = 1024) # cache with a key that is the sequence length, so that it does not need to recompute

# mock queries and keys

q = tf.random.normal((1, 1024, 64)) # queries - (batch, seq len, dimension of head)
k = tf.random.normal((1, 1024, 64)) # keys

# apply the rotations to your queries and keys after the heads have been split out, but prior to the dot product and subsequent softmax (attention)

freqs = freqs[None, ...] # expand dimension for batch dimension
q = apply_rotary_emb(freqs, q)
k = apply_rotary_emb(freqs, k)

# then do your attention with your queries (q) and keys (k)
```

If you do all the steps above correctly, you should see a dramatic improvement during training

## Axial Rotary Embeddings

For easy use of 2d axial relative positional embedding, ie. vision transformers

```python
import tensorflow as tf
from rotary_embedding_tensorflow import apply_rotary_emb, RotaryEmbedding, broadcat

pos_emb = RotaryEmbedding(
    dim = 32,
    freqs_for = 'pixel'
)

# queries and keys for frequencies to be rotated into

q = tf.random.normal((1, 256, 256, 64))
k = tf.random.normal((1, 256, 256, 64))

# get frequencies for each axial
# -1 to 1 has been shown to be a good choice for images and audio

freqs_h = pos_emb(tf.linspace(-1, 1, num = 256), cache_key = 256)
freqs_w = pos_emb(tf.linspace(-1, 1, num = 256), cache_key = 256)

# concat the frequencies along each axial
# broadcat function makes this easy without a bunch of expands

freqs = broadcat((freqs_h[None, :, None, :], freqs_w[None, None, :, :]), dim = -1)

# rotate in frequencies

q = apply_rotary_emb(freqs, q)
k = apply_rotary_emb(freqs, k)
```

## Learned Rotations

For injecting learned rotations into a network. Experiments pending

Update: doesn't seem to do anything -_-, will keep trying...

```python
import tensorflow as tf
from tensorflow.keras import layers
from rotary_embedding_tensorflow import apply_learned_rotations

x = tf.random.normal((1, 1024, 512))

# you can only rotate in (dim // 2) values
# ex. for 512, you can only rotate in 256 values

# say you have two sets of learned rotations of 128 values each

rots1 = layers.Dense(128)(x)
rots2 = layers.Dense(128)(x)

# you rotate in 256 (128 x 2) at first

x = apply_learned_rotations(rots1, x, start_index = 0)

# then you start at index 256 and rotate in the last (128 x 2)

x = apply_learned_rotations(rots2, x, start_index = 256)

# you could also concat the rotations together and pass it in all at once

rots = tf.concat((rots1, rots2), axis = -1)

x = apply_learned_rotations(rots, x)
```

## Citations

```bibtex
@misc{su2021roformer,
    title   = {RoFormer: Enhanced Transformer with Rotary Position Embedding}, 
    author  = {Jianlin Su and Yu Lu and Shengfeng Pan and Bo Wen and Yunfeng Liu},
    year    = {2021},
    eprint  = {2104.09864},
    archivePrefix = {arXiv},
    primaryClass = {cs.CL}
}

@misc{rotary-embedding-torch,
    title   = {Rotary Embeddings - Pytorch}, 
    author  = {Phil Wang (lucidrains)},
    year    = {2021},
    url  = {https://github.com/lucidrains/rotary-embedding-torch},
    publisher = {Github},
}
```
