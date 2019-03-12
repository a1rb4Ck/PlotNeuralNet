import sys
sys.path.append('../')
from pycore.tikzeng import to_head, to_cor, to_begin, to_end  # mandatory
from pycore.tikzeng import to_generate
from pycore.tikzeng import to_input
from pycore.tikzeng import to_Conv
from pycore.tikzeng import to_ConvConvRelu
from pycore.tikzeng import to_Pool
from pycore.tikzeng import to_UnPool
from pycore.tikzeng import to_ConvRes
from pycore.tikzeng import to_ConvSoftMax
from pycore.tikzeng import to_SoftMax
from pycore.tikzeng import to_connection
from pycore.tikzeng import to_skip


class Block(object):
    '''Wraps around the string generating functions to allow access to
    parameters like name etc.'''

    def __init__(self, fn, kind, **kwargs):
        '''Args:
            fn (Callable): One of the string generating functions.
            kwargs (kwargs): Arguments passed to that function.
        '''

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.fn = fn
        self.kwargs = kwargs

        self.kind = kind

    def __str__(self):
        return self.fn(**self.kwargs)


KIND_MAP = {
        'conv': to_Conv,
        'pool': to_Pool,
        'unpool': to_UnPool
        }


def str2block(kind, previous, **kwargs):
    fn = KIND_MAP[kind]
    if previous is not None:
        kwargs['to'] = '({}-east)'.format(previous.name)
    block = Block(fn, kind, **kwargs)

    return block


def connect(block_of, block_to):
    fn = to_connection
    block = Block(fn, 'connect', of=block_of.name, to=block_to.name)

    return block


class Archer(object):
    '''Chains blocks in a predifined manner'''

    def __init__(self, path='..', intra_offset=2, inter_offset=4):
        self.intra_offset = intra_offset
        self.inter_offset = inter_offset
        # Header
        self.arch = [
                to_head(path),
                to_cor(),
                to_begin()
                ]

        self.sub_archs = {}
        self.lanes = {}
        self.sub_connects = {}

    def add_sub_arch(name, lane=(0, 0, 0)):
        '''Add a new entry in the sub_archs dict. Subarchs are linear in 
        nature but live in 3d lanes. They can be connected in the end.
        '''

        self.sub_archs[name] = []
        self.lanes[name] = lane

    def __call__(self, kind, sub_arch='main', lane=None, **kind_kwargs):
        '''Chains a block of type :attr:`kind` to the sub architecture
        :attr:`sub_arch`.
        '''

        if sub_arch in self.sub_archs:
            prev = self.sub_archs[sub_arch][-1]

        else:
            self.sub_archs[sub_arch] = []
            self.sub_connects[sub_arch] = []
            self.lanes[sub_arch] = lane or (0, 0, 0)
            prev = None

        if prev is not None and prev.kind != kind:
            kind_kwargs['offset'] = '({}, 0, 0)'.format(self.intra_offset)
        new_block = str2block(kind, prev, **kind_kwargs)
        self.sub_archs[sub_arch] += [new_block]

        if prev is not None:
            self.sub_connects[sub_arch] += [connect(prev, new_block)]

    def save(self):
        for name, arch in self.sub_archs.items():
            self.arch += ['\n\n% {}\n'.format(name)]
            self.arch += [str(b) for b in arch]

        self.arch += ['\n\n%%%%%%%%\n% Connections']

        for name, connects in self.sub_connects.items():
            self.arch += ['% {}'.format(name)]
            self.arch += [str(c) for c in connects]

        self.arch += [to_end()]

        namefile = str(sys.argv[0]).split('.')[0]

        to_generate(self.arch, namefile + '.tex' )
        

# # defined your arch
# arch = [
#     to_head( '..' ),
#     to_cor(),
#     to_begin(),
#     to_Conv('conv', caption='to Conv'),
#     to_ConvConvRelu('ccr', caption='to ConvConvRelu', to='(conv-east)', offset='(1, 0, 0)'),
#     to_Pool('p', caption='to Pool', to='(ccr-east)', offset='(1, 0, 0)'),
#     to_UnPool('up', caption='to UnPool', to='(p-east)', offset='(1, 0, 0)'),
#     to_ConvRes('cr', caption='to ConvRes', to='(up-east)', offset='(1, 0, 0)'),
#     to_ConvSoftMax('cs', caption='to ConvSoftMax', to='(cr-east)', offset='(1, 0, 0)'),
#     to_SoftMax('sm', caption='to SoftMax', to='(cs-east)', offset='(1, 0, 0)'),
#     to_connection('p', 'up'),
#     to_skip('conv', 'cr'),
#     to_end()
#     ]

# def main():
#     namefile = str(sys.argv[0]).split('.')[0]
#     to_generate(arch, namefile + '.tex' )


def main():
    A = Archer()
    A('conv', name='conv_1', caption='C1', height=40, depth=40, width=1, n_filer=32, s_filer=256)
    A('conv', name='conv_2', caption='C2', height=40, depth=40, width=1, n_filer=32, s_filer=256)
    A('pool', name='pool_1', caption='D')
    A('conv', name='conv_3', caption='C3', height=20, depth=20, width=2, n_filer=64, s_filer=128)
    A('conv', name='conv_4', caption='C4', height=20, depth=20, width=2, n_filer=64, s_filer=128)
    A('pool', name='pool_2', caption='D')
    A('conv', name='conv_5', caption='C5', height=10, depth=10, width=4, n_filer=128, s_filer=64)
    A('conv', name='conv_6', caption='C6', height=10, depth=10, width=4, n_filer=128, s_filer=64)

    A('unpool', name='unpool_1', caption='UP')
    A('conv', name='conv_7', caption='C7', height=20, depth=20, width=2, n_filer=64, s_filer=128)
    A('conv', name='conv_8', caption='C8', height=20, depth=20, width=2, n_filer=64, s_filer=128)
    A('unpool', name='unpool_2', caption='UP')
    A('conv', name='conv_9', caption='C9',  height=40, depth=40, width=1, n_filer=32, s_filer=256)
    A('conv', name='conv_10', caption='C10', height=40, depth=40, width=1, n_filer=3, s_filer=256)

    A.save()

if __name__ == '__main__':
    main()
