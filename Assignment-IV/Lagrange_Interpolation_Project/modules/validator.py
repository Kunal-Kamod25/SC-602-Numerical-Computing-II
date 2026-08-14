# validator.py
#
# Why this file exists:
# Before we do any interpolation, we should always check that the
# data given by the user actually makes sense. For example, we
# cannot have two points with the same x value (that would break
# the Lagrange formula because we divide by (xi - xj)).
#
# So this file just keeps all the "checking" logic in one place
# instead of scattering if-checks everywhere in the main program.


class Validator:
    """
    Simple class that holds validation methods.
    All methods here either pass silently (data is fine) or
    raise a ValueError with a clear message.
    """

    def check_minimum_points(self, x_list):
        # We need at least 2 points to draw a line, so anything
        # less than that does not make sense for interpolation.
        if len(x_list) < 2:
            raise ValueError("Need at least 2 data points to do interpolation.")

    def check_duplicate_x(self, x_list):
        # Using a set to quickly find duplicates.
        # If the set is smaller than the list, it means some
        # x values were repeated.
        unique_values = set(x_list)
        if len(unique_values) != len(x_list):
            raise ValueError("Duplicate x values found. All x values must be different.")

    def check_equal_length(self, x_list, y_list):
        # x and y arrays must have same length otherwise which y
        # belongs to which x is not clear.
        if len(x_list) != len(y_list):
            raise ValueError("Number of x values and y values do not match.")

    def check_not_empty(self, data_list):
        if len(data_list) == 0:
            raise ValueError("Input data is empty.")

    def check_point_in_reasonable_range(self, point, x_list):
        # This is not a hard error, just a soft warning check.
        # Interpolation technically works outside the range too
        # (that is called extrapolation) but the answer becomes
        # less trustworthy, so we just print a warning, we do not
        # stop the program.
        min_x = min(x_list)
        max_x = max(x_list)
        if point < min_x or point > max_x:
            print("Warning: The point you gave is outside the given data range.")
            print("This means we are extrapolating, result may not be accurate.")

    def check_large_dataset_warning(self, x_list):
        # This is not an error, just information for the user.
        #
        # In theory the Lagrange formula works for any number of
        # points. But in practice, when we calculate it directly
        # (the "naive" way, like we do in this project), the
        # numerator and denominator are made by multiplying many
        # numbers together. If there are too many points, these
        # products become extremely large (or extremely small),
        # bigger than what a normal float can store. This is
        # called "overflow" and it makes the answer come out as
        # "nan" (not a number).
        #
        # From our testing, this project starts giving unreliable
        # results somewhere around 100-200 points. So we just warn
        # the user here, we do not stop the program, since the
        # program can still be used for smaller/medium datasets
        # without any issue.
        if len(x_list) > 100:
            print("Warning: Large dataset detected.")
            print("The direct (naive) Lagrange formula used in this project")
            print("can become numerically unstable for very large datasets")
            print("(the numbers involved get too big for the computer to store")
            print("accurately). Results for very large datasets may show as 'nan'.")
            print("See README.md -> Future Improvements for more on this.")

    def validate_all(self, x_list, y_list, points_list):
        # Runs every check together, so main code just calls
        # this one method instead of calling each check one by one.
        # points_list can have one or more points to estimate.
        self.check_not_empty(x_list)
        self.check_equal_length(x_list, y_list)
        self.check_minimum_points(x_list)
        self.check_duplicate_x(x_list)
        self.check_large_dataset_warning(x_list)

        for point in points_list:
            self.check_point_in_reasonable_range(point, x_list)
