"""
Minimum inference code
"""
import os
import numpy as np
from imageio import imread, imwrite
import tensorflow as tf
from generator import Generator
from logger import get_logger


# NOTE: TF warnings are too noisy without this
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel(40)


def main(m_path, img_path, out_dir, light=False):
    logger = get_logger("inference")
    logger.info(f"generating image from {img_path}")
    try:
        g = Generator(light=light)
        g.load_weights(m_path)
        img = np.expand_dims(imread(img_path), 0).astype(np.float32) / 127.5 - 1
        out = ((g(img).numpy().squeeze() + 1) * 127.5).astype(np.uint8)
    except ValueError:
        logger.error("Failed to load specified weight.")
        logger.error("If you trained your model with --light, "
                     "consider adding --light when executing this script; otherwise, "
                     "do not add --light when executing this script.")
        exit(1)
    if out_dir != "" and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    if out_dir == "":
        out_dir = "."
    out_path = os.path.join(out_dir, os.path.split(img_path)[1])
    imwrite(out_path, out)
    logger.info(f"generated image saved to {out_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--m_path", type=str, default=os.path.join("models", "generator"))
    parser.add_argument("--img_path", type=str,
                        default=os.path.join("input_images", "temple.jpg"))
    parser.add_argument("--out_dir", type=str, default='out')
    parser.add_argument("--light", action='store_true')
    args = parser.parse_args()
    main(args.m_path, args.img_path, args.out_dir, args.light)
