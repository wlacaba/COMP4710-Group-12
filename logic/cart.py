"""
PURPOSE
Build the CART tree here.

AUTHOR
Min Gyu Park
"""

import csv
from random import shuffle


class _SplittingCriterion:
    """
    Records the position of splitting attribute in
    the header list (column number) and its splitting value.
    """

    def __init__(self, attr_col_num, value):
        self.attr_col_num = attr_col_num
        self.value = value

    def match(self, row):
        # Check if row's attribute value matches with
        # 'this' attribute's value
        return self.value == row[self.attr_col_num]

    def __str__(self):
        # Format in a readable way
        # eg. Is 'company' == 'Disney'?
        condition = '=='
        return "{0} {1} {2}".format(header[self.attr_col_num], condition, self.value)


class _Leaf:
    """
    A Leaf node that holds the frequency of the class values
    """

    def __init__(self, rows):
        self.predictions = _count_class_values(rows)


class _SplittingNode:
    """
    A node containing the splitting criterion and its child nodes
    """

    def __init__(self, split_crit, true_branch, false_branch):
        self.split_crit = split_crit
        self.true_branch = true_branch
        self.false_branch = false_branch


def _get_unique_values(rows, attr_num):
    """
    Find the unique values of a column in the rows
    """
    return set([row[attr_num] for row in rows])


def _count_class_values(rows):
    """
    Count how many times each class label occurs in a dataset
    """
    counter = {}  # save it as label -> count
    for row in rows:
        class_label = row[revenue_pos]  # class label at the last column
        if class_label not in counter:
            counter[class_label] = 0
        counter[class_label] += 1

    return counter


def _partition(rows, split_crit):
    """
    Partition a dataset into true/false rows based on the
    splitting criterion
    """
    true_rows, false_rows = [], []  # to hold the partitions

    # Loop through the DataFrame
    for row in rows:
        if split_crit.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)

    return true_rows, false_rows


def _gini(rows):
    """
    Calculate the Gini Impurity of the rows.
    """
    # Count the unique class values and their frequency in rows
    class_values = _count_class_values(rows)

    gini_impurity = 1
    # for each class value
    for class_val in class_values:
        prob = class_values[class_val] / float(len(rows))  # Get its probability ( frequency / total size )
        gini_impurity -= prob ** 2  # Gini = 1 - (sum of prob^2)
    return gini_impurity


def _info_gain(left, right, current_uncertainty):
    """
    Calculate uncertainty given the uncertainty of current node
    and its child nodes
    """
    prob = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - prob * _gini(left) - (1 - prob) * _gini(right)


def _get_best_split(rows):
    """
    Get the best split by iterating over every attribute
    and its value and calculating its information gain
    """
    best_gain = 0  # to hold the best gain to split
    best_split_crit = None  # to hold the best splitting criterion
    current_uncertainty = _gini(rows)
    size = len(header)  # number of columns

    # for each attribute
    for col_num in range(size):
        # Get unique values in the column
        if header[col_num] == 'revenue' or header[col_num] == 'title':
            continue
        else:
            unique_values = _get_unique_values(rows, col_num)

        # for each value
        for val in unique_values:
            # Try to split the dataset to find the best info gain
            split_crit = _SplittingCriterion(col_num, val)
            true_rows, false_rows = _partition(rows, split_crit)

            # Skip if either partition is empty
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the info gain
            gain = _info_gain(true_rows, false_rows, current_uncertainty)

            # Save the best gain and its splitting criterion
            if gain > best_gain:
                best_gain, best_split_crit = gain, split_crit

    return best_gain, best_split_crit


def _build_tree(rows):
    """
    Build a tree using recursion

        Base case: Information Gain = 0 (Class labels are equal)
                   Return Leaf

        Else...
        Split the rows using the best splitting criterion
    """
    # Get the best gain and splitting criterion
    gain, split_crit = _get_best_split(rows)

    # Base case
    if gain == 0:
        return _Leaf(rows)

    # Else... split rows
    true_rows, false_rows = _partition(rows, split_crit)

    # Build tree from true and false branches
    true_branch = _build_tree(true_rows)
    false_branch = _build_tree(false_rows)

    # Return the node containing its child nodes and the splitting criterion
    return _SplittingNode(split_crit, true_branch, false_branch)


def classify(row, node):
    """
    Classify a row given a splitting node
    """
    # Base case - has reached a Leaf node
    if isinstance(node, _Leaf):
        return node.predictions

    # Follow a branch based on results of match
    if node.split_crit.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def predict(leaf):
    """
    Based on its class values, predict the class label it belongs
    by finding the maximum among the class values
    """
    return max(leaf.keys(), key=(lambda key: leaf[key]))


def split_dataset(dataset, train_ratio):
    """
    Split the data into training and testing dataset
    """
    size = len(dataset)  # size of dataset

    # Shuffle the dataset randomly
    shuffle(dataset)

    # Split the data
    train_data = dataset[:int(train_ratio * size)]
    test_data = dataset[int(train_ratio * size):]

    return train_data, test_data


def _get_accuracy(tree, test):
    """
    Find out how many predictions are correct given a tree
    and test data
    """
    size = len(test)
    correct = 0.0

    # Write the results
    with open('results.csv', 'w', newline='\n', encoding='utf-8') as resultFile:
        writer = csv.writer(resultFile, delimiter=',')
        header_row = []
        for r in header:
            header_row.append(r)
        header_row.append('Prediction')
        writer.writerow(header_row)
        # for each row in test data
        for row in test:
            # Copy data to write
            result_row = []
            for r in row:
                result_row.append(r)

            predict_leaf = predict(classify(row, tree))  # Predict the data

            # Write the results
            result_row.append(predict_leaf)
            writer.writerow(result_row)

            if row[revenue_pos] == predict_leaf:
                correct += 1

    accuracy = correct / size * 100

    return accuracy


def _get_av_accuracy(dataset, train_ratio, n):
    """
    Split the data n times and build a tree  to find out the
    average accuracy and the average time to build the tree.
    """
    av_accuracy = 0
    for i in range(n):
        train, test = split_dataset(dataset, train_ratio)

        tree = _build_tree(train)
        accuracy = _get_accuracy(tree, test)
        print('Test #{0}, accuracy = {1}'.format(i, accuracy))

        # Get accuracy
        av_accuracy += accuracy

    av_accuracy /= n

    print('Average over {0} trials: {1}%'.format(n, av_accuracy))


def run_cart(filename, n):
    # Open file and get the data as list
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        dataset = list(reader)

    global header
    header = dataset[0]  # get column names

    global revenue_pos
    revenue_pos = header.index('revenue')  # get position of class label

    dataset = dataset[1:]  # exclude column names from dataset

    print('\nBuilding decision tree using CART algorithm....\n')

    _get_av_accuracy(dataset, 0.5, n)
