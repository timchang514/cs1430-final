from skimage import color, feature, transform, io, img_as_float

# Fix crash on OSX
# import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

import numpy as np
import scipy
import cv2
import scipy.cluster.hierarchy as hcluster

# returns an array of images, each image being a square in the playing area of the board
# these images will be passed into the CNN for classification
def get_board_squares(img, corners):
    # the dimensions 1816 x 1816 were chosen such that each square in the board will be of dimension 227 x 227 for the CNN
    new_corners = np.array([[0, 0], [0, 1816], [1816, 1816], [1816, 0]], dtype='float32')

    # four point transform to crop the board image to get just the playing area
    M = cv2.getPerspectiveTransform(corners, new_corners)
    warped = cv2.warpPerspective(img, M, (1816, 1816))
    # plt.imshow(img)
    # plt.scatter(corners[:,0], corners[:, 1], c="r")
    # plt.show()


    # divide the cropped image to get the individual squares of the board
    squares = divide_board(warped, int(1816/8))

    return squares

# takes in an image of a board (taken from video feed of the game) and finds the corners
# of the playing area
def find_corners(img):
    # img = cv2.resize(img, (313, 418))
    # img = cv2.resize(img, (720, 1280))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # get the edges of the image
    edges = detect_edges(img)

    # get the lines of the board
    lines = cv2.HoughLines(edges, 1, np.pi/180, 90)
    lines = np.reshape(lines, (len(lines), 2))

    # filter to get only roughly vertical and horizontal lines
    horizontal = []
    vertical = []

    for r, t in lines:
        if t < 0.1 or t > np.pi - 0.1:
            vertical.append([r, t])
        elif t < (np.pi / 2) + 0.1 and t > (np.pi / 2) - 0.1:
            horizontal.append([r, t])

    # find where the horizontal and vertical lines intersect
    intersections = find_intersections(horizontal, vertical)

    # run agglomerative clustering in case we detected some bad lines
    thresh = 5
    dists = scipy.spatial.distance.pdist(intersections)
    linkage_matrix = hcluster.single(dists)
    flat_clusters = hcluster.fcluster(linkage_matrix, thresh, criterion="distance")
    clusters = {}
    # calculate the cluster centers
    for i, c_ind in enumerate(flat_clusters):
        if c_ind in clusters:
            clusters[c_ind].append(intersections[i])
        else:
            clusters[c_ind] = [intersections[i]]

    centers = []
    for points in clusters.values():
        center = [np.mean(np.array(points)[:,0]), np.mean(np.array(points)[:,1])]
        centers.append(center)

    centers = np.array(centers)
    # plt.imshow(img)
    # plt.scatter(centers[:,0], centers[:,1], c="r")
    # plt.show()
    # once we have the clustered intersection points, find the corners of the playing area
    # return these corners
    corners = get_playing_area_corners(img, centers)

    return corners


def detect_edges(img):
    m = np.median(img)
    lower = int(max(0,(1.0 - 0.33) * m))
    upper = int(min(255, (1.0 + 0.33) * m))
    edges = cv2.Canny(img, lower, upper)
    return edges

def find_intersections(horizontal, vertical):
    intersections = []
    for r1, t1 in horizontal:
        for r2, t2 in vertical:
            b = [r1, r2]
            A = [[np.cos(t1), np.sin(t1)], [np.cos(t2), np.sin(t2)]]
            X = np.linalg.solve(A, b)
            intersections.append(X)

    return np.array(intersections)

def get_closest_point(a, B):
    dists = scipy.spatial.distance.cdist([a], B)
    return B[np.argmin(dists)]

def get_second_closest_point(a, B):
    dists = scipy.spatial.distance.cdist([a], B)
    return B[np.argsort(dists)[0, 1]]

def get_playing_area_corners(im, points):
    n, m = im.shape
    image_center = [m / 2, n / 2]

    # get the point on the board closest to image center
    # if the camera is properly positioned, this will be the center of the board
    board_center = get_closest_point(image_center, points)

    # find the gridpoint adjacent to the board to calculate the size of the
    # squares of the board in pixels
    board_center_adjacent = get_second_closest_point(board_center, points)
    dist = scipy.spatial.distance.euclidean(board_center, board_center_adjacent)

    # find the points closest to where the corners of the board should be
    # according to the location of the board center and the gridsize
    corner1 = get_closest_point([board_center[0] - 4*dist, board_center[1] - 4*dist], points)
    corner2 = get_closest_point([board_center[0] - 4*dist, board_center[1] + 4*dist], points)
    corner3 = get_closest_point([board_center[0] + 4*dist, board_center[1] + 4*dist], points)
    corner4 = get_closest_point([board_center[0] + 4*dist, board_center[1] - 4*dist], points)
    corners = np.array([corner1, corner2, corner3, corner4], dtype='float32')

    return corners

def divide_board(board_image, side_length):
    squares = []
    for i in range(8):
        for j in range(8):
            squares.append(board_image[i * side_length : (i + 1) * side_length, i * side_length : (i + 1) * side_length])

    return squares
