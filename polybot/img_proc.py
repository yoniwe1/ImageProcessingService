import random
from pathlib import Path
from matplotlib.image import imread, imsave


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j - 1] - row[j]))

            self.data[i] = res

    def rotate(self):

        # rotate = transpose + reverse lines

        m = len(self.data)
        n = len(self.data[0])

        transposed = list(zip(*self.data))
        rotated = [[0 for x in range(m)] for y in range(n)]

        for i in range(len(transposed)):
            new_transposed = list(transposed[i])
            new_transposed.reverse()
            rotated[i] = new_transposed

        self.data = rotated

    def salt_n_pepper(self):

        for i in range(len(self.data)):

            for j in range(len(self.data[0])):

                random_number = random.random()

                if random_number < 0.2:
                    self.data[i][j] = 255

                elif random_number > 0.8:
                    self.data[i][j] = 0

    def concat(self, other, direction='horizontal'):

        height_original = len(self.data)
        width_original = len(self.data[0])
        height_other = len(other.data)
        width_other = len(other.data[0])

        if height_original != height_other or width_original != width_other:
            raise RuntimeError("Matrix sizes do not match!")

        result = []

        if direction == "horizontal":

            for i in range(height_original):
                row_result = self.data[i] + other.data[i]
                result.append(row_result)

        elif direction == "vertical":

            result.extend(self.data)
            result.extend(other.data)

        else:

            raise RuntimeError("No valid specification of direction is given!")

        self.data = result

    def segment(self):

        for i in range(len(self.data)):

            for j in range(len(self.data[0])):

                if self.data[i][j] > 100:
                    self.data[i][j] = 255

                else:
                    self.data[i][j] = 0


if __name__ == '__main__':
    my_img = Img("/home/jonathan/Pictures/beatles.jpg")
    my_img.segment()
    my_img.save_img()
