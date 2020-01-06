def navigateToWaypoint(self, x_in, y_in):  # x_in and y_in are in metres
    y_in = y_in * 100
    x_in = x_in * 100
    x_diff = x_in-self.current_x
    y_diff = y_in-self.current_y
    desired_theta = math.atan(y_diff/x_diff)
    if abs(desired_theta - self.current_theta) < abs(self.current_theta - desired_theta):
        self.turn(desired_theta - self.current_theta)
    else:
        self.turn(self.current_theta - desired_theta)

    tangent_distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
    self.go_straight_cm(tangent_distance)
