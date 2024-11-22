import json
import os
import random
from scipy.spatial import distance
import cv2
import numpy as np


def orb_similarity_by_distance(imageA, imageB):
    orb = cv2.ORB_create()
    kpA, desA = orb.detectAndCompute(imageA, None)
    kpB, desB = orb.detectAndCompute(imageB, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desA, desB)
    matches = sorted(matches, key=lambda x: x.distance)
    total_distance = sum(match.distance for match in matches)
    max_distance = 255
    similarity = 1 - (total_distance / (len(matches) * max_distance))

    return similarity


def sift_encoding(img_path, vector_size=30):
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints = sift.detect(gray_img, None)
    keypoints = sorted(keypoints, key=lambda x: -x.response)
    img_kps = keypoints[:vector_size]
    kps, des = sift.compute(gray_img, img_kps)
    vector = des.flatten()
    vector_len = vector_size * 128
    if vector.size < vector_len:
        vector = np.concatenate(vector, np.zeros(vector_len - vector.size))
    return vector.reshape(-1, 128 * vector_size)


def sift_similarity_by_distance(imageA, imageB):
    vectorA = sift_encoding(imageA)
    vectorB = sift_encoding(imageB)
    sim = distance.cdist(vectorA, vectorB, 'cosine')
    return sim


def get_similarity_imagePathList(DataSetName, image_path, top_n=1):
    directory_path = f'example/{DataSetName}/img/'
    label_path = f"example/{DataSetName}/context.json"

    with open(label_path, 'r', encoding='utf-8') as f:
        label = json.load(f)

    target_img = cv2.imread(image_path)
    similarity_scores = []
    for imgName in label:
        img = cv2.imread(directory_path + imgName)
        try:
            similarity = orb_similarity_by_distance(img, target_img)
        except:
            continue
        similarity_scores.append((directory_path + imgName, similarity))
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    similar_images = [path for path, _ in similarity_scores[:top_n]]

    if len(similar_images) == 0:
        all_images = [os.path.join(directory_path, img) for img in os.listdir(directory_path) if
                      img.endswith(('.jpg', '.png', '.jpeg'))]
        similar_images = random.sample(all_images, min(top_n, len(all_images)))

    return similar_images
