from nnplot import Architecture, Wrapper


FILTER_NORM = 32
SPATIAL_NORM = 256. / 40.


def up(n, size, arch, show_names=True):
    '''Add a conv-layer with n filters'''

    kwargs = {
            'height': size / SPATIAL_NORM,
            'depth': size / SPATIAL_NORM,
            'width': n / FILTER_NORM,
            'n_filer': n,
            's_filer': size
            }
    arch('deconv', **kwargs) 

    return size


def conv(n, size, arch, show_names=True):
    '''Add a conv-layer with n filters'''

    kwargs = {
            'height': size / SPATIAL_NORM,
            'depth': size / SPATIAL_NORM,
            'width': n / FILTER_NORM,
            'n_filer': n,
            's_filer': size
            }
    arch('conv', **kwargs) 

    return size


res_counter = 0


def plus(other, arch):
    arch('plus', other=other, pos2=6.5)


def res(n, size, arch):
    r'''Input -> ReLU -> Conv -> Plus -> Output
          \______________________/
    '''

    global res_counter

    R = Architecture("Res_{}".format(res_counter))
    res_counter += 1

    kwargs = {
            'height': size / SPATIAL_NORM,
            'depth': size / SPATIAL_NORM,
            'width': 1,
            }

    # R('relu', **kwargs)
    R('conv', **kwargs)

    kwargs.update({
            'n_filer': n,
            's_filer': size
            })

    R('conv', **kwargs)

    kwargs['other'] = arch[-1]
    kwargs['pos1'] = 1.1
    kwargs['pos2'] = 10.1

    R('plus', **kwargs)

    arch(R)

    return size


def construct(in_size=256):
    arch1 = Architecture('Encoder')

    size = in_size
    size = conv(32, size, arch1)
    size = conv(32, size, arch1)
    size = conv(32, size, arch1)

    arch2 = Architecture('Encoder2', intra_offset=2)
    arch2(arch1)
    size = up(16, 2*size, arch2)
    plus(arch1[1], arch2)
    size = conv(16, size, arch2)

    res(16, size, arch2)

    W = Wrapper('..')

    W(arch2)

    W.save('pessers_mod.tex')


if __name__ == '__main__':
    construct()
