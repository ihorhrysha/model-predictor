import pickle as pkl


def pickle(obj, filepath):
    with open(filepath, 'wb') as f:
        pkl.dump(obj, f)


def unpickle(filepath):
    with open(filepath, 'rb') as f:
        obj = pkl.load(f)
    return obj


def read_sql_query(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data
