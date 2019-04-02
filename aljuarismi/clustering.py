import click
import khiva as kv


def kmean(tt, parameters):
    """

    :param parameters:
    :param tt:
    :return:
    """
    tts = kv.Array(tt)
    k = parameters["number"]
    if not k:
        print('How many clusters?')
        while not k:
            k = click.prompt('', type=int)
    data = kv.k_means(tts, int(k))
    return data[0].to_pandas()


def kshape(tt, parameters):
    """

    :param parameters:
    :param tt:
    :return:
    """
    tts = kv.Array(tt)
    k = parameters["number"]
    if not k:
        print('How many clusters?')
        while not k:
            k = click.prompt('', type=int)
    data = kv.k_shape(tts, int(k))
    return data[0].to_pandas()
