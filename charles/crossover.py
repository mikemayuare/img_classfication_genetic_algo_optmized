from random import randint, sample, uniform, random


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1) - 2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def pmx(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(p1)), 2)
    # xo_points = [3,6]
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * len(x)
        # offspring2
        o[xo_points[0] : xo_points[1]] = x[xo_points[0] : xo_points[1]]
        z = set(y[xo_points[0] : xo_points[1]]) - set(x[xo_points[0] : xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] is not None:
                temp = index
                index = y.index(x[temp])
            o[index] = i

        # numbers that doesn't exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return o1, o2


def arithmetic_xo(p1, p2):
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    alpha = uniform(0, 1)
    o1 = [None] * len(p1)
    o2 = [None] * len(p1)
    for i in range(len(p1)):
        o1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        o2[i] = p2[i] * alpha + (1 - alpha) * p1[i]
    return o1, o2


def blx_alpha_xo(p1, p2, alpha=0.1):
    size = len(p1)

    o1 = [None] * size
    o2 = [None] * size

    for i in range(size):
        # Determine the lower and upper bounds for the blending range
        min_val = min(p1[i], p2[i])
        max_val = max(p1[i], p2[i])

        # Calculate the range of the blending region
        range_val = max_val - min_val

        # Calculate the lower and upper bounds of the offspring
        low = min_val - alpha * range_val
        high = max_val + alpha * range_val

        # Generate a random value within the blending range
        o1[i] = uniform(low, high)
        o2[i] = uniform(low, high)

    return o1, o2


def simplex_xo(p1, p2):
    # Construct the simplex
    simplex = [p1, p2]
    size = len(p1)

    # Add a random point within the line segment connecting p1 and p2
    random_point = []
    for i in range(size):
        alpha = uniform(0, 1)
        random_coordinate = p1[i] + alpha * (p2[i] - p1[i])
        random_point.append(random_coordinate)
    simplex.append(random_point)

    # Generate offspring
    o1 = []
    o2 = []
    for i in range(size):
        coordinates = [
            vertex[i] for vertex in simplex
        ]  # Get the coordinates of the vertices along the i-th dimension
        min_coordinate = min(coordinates)
        max_coordinate = max(coordinates)

        # Randomly select a point within the range defined by the min and max coordinates
        offspring_coordinate = uniform(min_coordinate, max_coordinate)
        o1.append(offspring_coordinate)

        # Generate a second offspring by taking the average of the parent genes
        avg_coordinate = sum(coordinates) / len(coordinates)
        o2.append(avg_coordinate)

    return o1, o2


def sbx_xo(p1, p2, eta=20):
    # Assuming p1 and p2 are lists of non-negative real numbers representing genes
    # eta is the distribution index parameter

    size = len(p1)
    o1 = []
    o2 = []

    for i in range(size):
        # Perform SBX crossover for each gene

        u = random()  # Random value between 0 and 1
        if u <= 0.5:
            beta = (2 * u) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))

        # Calculate the minimum value for the offspring gene
        min_value = min(p1[i], p2[i])

        # Calculate the maximum value for the offspring gene
        max_value = max(p1[i], p2[i])

        # Generate the offspring gene within the range [min_value, max_value]
        child = 0.5 * ((1 - beta) * min_value + (1 + beta) * max_value)

        # Ensure the offspring gene is non-negative
        child = max(0, child)

        o1.append(child)

        # Generate a second offspring by taking the average of the parent genes
        avg_coordinate = sum([p1[i], p2[i]]) / 2
        o2.append(avg_coordinate)

    return o1, o2


if __name__ == "__main__":
    # p1, p2 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10], [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    p1, p2 = [0.1, 0.15, 0.3], [0.3, 0.1, 0.2]
    o1, o2 = arithmetic_xo(p1, p2)
    print(o1, o2)


def uniform_crossover(p1, p2):
    """
    Performs uniform crossover on two parents.

    Args:
        p1: The first parent.
        p2: The second parent.

    Returns:
        The two children created by modified uniform crossover.
    """

    crossover_point1 = randint(0, len(p1) - 1)
    crossover_point2 = randint(crossover_point1 + 1, len(p1))

    o1 = (
        p1[:crossover_point1]
        + p2[crossover_point1:crossover_point2]
        + p1[crossover_point2:]
    )
    o2 = (
        p2[:crossover_point1]
        + p1[crossover_point1:crossover_point2]
        + p2[crossover_point2:]
    )

    return o1, o2
