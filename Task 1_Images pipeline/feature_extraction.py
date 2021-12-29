import cv2
import numpy as np
import joblib
from sklearn.cluster import KMeans


def cluster_sift_descriptions(data, NUM_CLUSTERS):
    #Prepare data
    print("Training kmeans")
    #Create model
    kmeans = KMeans(n_clusters = NUM_CLUSTERS, random_state = 0)
    #train model
    sift_descriptors = np.concatenate(data['sift_description'], axis = 0)
    kmeans.fit(sift_descriptors)
    return kmeans

def get_class(animal):
    class_as_number = 0
    if animal == 'Cheetah':
        class_as_number = 1
    if animal == 'Jaguar':
        class_as_number = 2
    if animal == 'Leopard':
        class_as_number = 3
    if animal == 'Lion':
        class_as_number = 4
    if animal == 'Tiger':
        class_as_number = 5
    if class_as_number == 0:
        print('ANIMAL NAME NOT DEFINED!\n')
        print(animal)
    return class_as_number

def calculate_histogram(data, model):
    feature_vector = []
    label_vector = []

    #Make prediction to what class the keypoint belong and make a histogram of that
    idx = 0
    for img in data['sift_description']:
        #Predict and create histogram
        predict_kmeans = model.predict(img)
        hist, bin_edges = np.histogram(predict_kmeans)
        feature_vector.append(hist)

        #Create target vector for classification
        label = get_class(data['label'][idx])
        label_vector.append(label)
        idx = idx + 1

    return feature_vector, label_vector



# -- SIFT --
# https://www.analyticsvidhya.com/blog/2019/10/detailed-guide-powerful-sift-technique-image-matching-python/
def apply_sift(data):
    for img in data['data']:
        img = np.float32(img)
        # Grayscale
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Binarization
        img = cv2.normalize(img, None, 0, 255,
                            cv2.NORM_MINMAX).astype('uint8')

        # Get the sift keypoints and the corresponding descriptors
        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(img, None)
        if 'sift_description' not in data.keys():
            data['sift_description'] = []

        data['sift_description'].append(des)

    return data

if __name__ == '__main__':
    base_name = 'big_cats'
    width = 80
    data = joblib.load(f'{base_name}_{width}x{width}px.pkl')
    data = apply_sift(data)
    # Temporary print loop (to analyze the data)
    # for keypoints in data['sift_keypoints'][:5]:
    #     print('\n')
    #     for d in keypoints:
    #         print(d)
    #         # print(str(d.angle) + ' ' + str(d.class_id) + ' ' + str(d.octave) + ' ' + str(d.pt)  + ' ' +
    #         # str(d.response) + ' ' + str(d.size))