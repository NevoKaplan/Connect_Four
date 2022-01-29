import constants


class Place:
    # one square
    def __init__(self, row, col):
        # each square has a row/col position.
        self.row = row
        self.col = col
        self.left, self.top = self.left_top_coordinates_of_box()
        self.image = ''
        self.image_pre = ''
        self.color = ''

    def left_top_coordinates_of_box(self):
        # Convert board coordinates to pixel coordinates
        left = self.col * (constants.BOX_SIZE_X + constants.GAP_SIZE_X) + constants.X_MARGIN + 32
        top = self.row * (constants.BOX_SIZE_Y + constants.GAP_SIZE_Y) + constants.Y_MARGIN + 93
        return left, top