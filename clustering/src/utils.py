import numpy as np

from sklearn.mixture import GaussianMixture


def get_data(conn):
    """
    Fetch the last minute of data from db
    """
    sql = "select * from last_minute"
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return np.array([row[2] for row in data]).reshape(-1, 1)


def get_params(data):
    """
    cluster data and return estimated params
    """
    gmm = GaussianMixture(n_components=3)
    gmm.fit(data)

    return {
        "means": [gmm.means_[i][0] for i in range(3)],
        "vars": [gmm.covariances_[i][0][0] ** 0.5 for i in range(3)],
    }
