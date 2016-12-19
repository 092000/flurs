from abc import ABCMeta, abstractmethod

import numpy as np


class Recommender:

    """Base class for experimentation of the incremental models with positive-only feedback.

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        # number of observed users
        self.n_user = 0

        # store user data
        self.users = {}

        # number of observed items
        self.n_item = 0

        # store item data
        self.items = {}

    @abstractmethod
    def init_model(self):
        """Initialize model parameters.

        """
        pass

    def is_new_user(self, u):
        """Check if user is new.

        Args:
            u (int): User index.

        Returns:
            boolean: whether user is new

        """
        return u not in self.users

    @abstractmethod
    def add_user(self, user):
        """For new users, append their information into the dictionaries.

        Args:
            user (User): User.

        """
        self.users[user.index] = {'observed': set()}
        self.n_user += 1

    def is_new_item(self, i):
        """Check if item is new.

        Args:
            i (int): Item index.

        Returns:
            boolean: whether item is new

        """
        return i not in self.items

    @abstractmethod
    def add_item(self, item):
        """For new items, append their information into the dictionaries.

        Args:
            item (Item): Item.

        """
        self.items[item.index] = {}
        self.n_item += 1

    @abstractmethod
    def update(self, e, is_batch_train):
        """Update model parameters based on d, a sample represented as a dictionary.

        Args:
            e (Event): Observed event.

        """
        pass

    @abstractmethod
    def predict(self, user, candidates):
        """Make prediction for the pairs of given user and item candidates.

        Args:
            user (User): Target user.
            candidates (numpy array; (# candidates, )): Target item' indices.

        Returns:
            numpy float array; (# candidates, ): Predicted values for the given user-candidates pairs.

        """
        pass

    @abstractmethod
    def recommend(self, user, target_i_indices):
        """Recommend items for a user represented as a dictionary d.

        First, scores are computed.
        Next, `self.__scores2recos()` is called to convert the scores into a recommendation list.

        Args:
            user (User): Target user.
            target_i_indices (numpy array; (# target items, )): Target items' indices. Only these items are considered as the recommendation candidates.

        Returns:
            (numpy array, numpy array) : (Sorted list of items, Sorted scores).

        """
        return

    def scores2recos(self, scores, target_i_indices, rev=False):
        """Get recommendation list for a user u_index based on scores.

        Args:
            scores (numpy array; (n_target_items,)):
                Scores for the target items. Smaller score indicates a promising item.
            target_i_indices (numpy array; (# target items, )): Target items' indices. Only these items are considered as the recommendation candidates.
            rev (bool): If true, return items in an descending order. A ascending order (i.e., smaller scores are more promising) is default.

        Returns:
            (numpy array, numpy array) : (Sorted list of items, Sorted scores).

        """
        sorted_indices = np.argsort(scores)

        if rev:
            sorted_indices = sorted_indices[::-1]

        return target_i_indices[sorted_indices], scores[sorted_indices]


class FeatureRecommender(Recommender):

    """Base class for experimentation of the incremental models with positive-only feedback.

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def recommend(self, user, target_i_indices, context):
        """Recommend items for a user represented as a dictionary d.

        First, scores are computed.
        Next, `self.__scores2recos()` is called to convert the scores into a recommendation list.

        Args:
            user (User): Target user.
            target_i_indices (numpy array; (# target items, )): Target items' indices. Only these items are considered as the recommendation candidates.
            context (numpy 1d array): Feature vector representing contextual information.

        Returns:
            (numpy array, numpy array) : (Sorted list of items, Sorted scores).

        """
        return