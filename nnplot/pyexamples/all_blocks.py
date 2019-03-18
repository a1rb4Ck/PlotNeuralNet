import os

# mandatory
from nnplot.pycore.tikzeng import to_head, to_cor, to_begin, to_end

from nnplot.pycore.tikzeng import to_generate
from nnplot.pycore.tikzeng import to_input
from nnplot.pycore.tikzeng import to_Conv
from nnplot.pycore.tikzeng import to_DeConv
from nnplot.pycore.tikzeng import to_ConvConvRelu
from nnplot.pycore.tikzeng import to_Pool
from nnplot.pycore.tikzeng import to_UnPool
from nnplot.pycore.tikzeng import to_ConvRes
from nnplot.pycore.tikzeng import to_ConvSoftMax
from nnplot.pycore.tikzeng import to_SoftMax
from nnplot.pycore.tikzeng import to_connection
from nnplot.pycore.tikzeng import to_skip
from nnplot.pycore.tikzeng import cage_between
from nnplot.pycore.tikzeng import plus


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
        'deconv': to_DeConv,
        'pool': to_Pool,
        'unpool': to_UnPool,
        'ccr': to_ConvConvRelu,
        'cr': to_ConvRes,
        'plus': plus
        }


def str2block(kind, previous, **kwargs):
    fn = KIND_MAP[kind]
    if previous is not None:
        while isinstance(previous, Architecture):
            previous = previous[-1]
        kwargs['to'] = '({}-east)'.format(previous.name)

    block = Block(fn, kind, **kwargs)

    return block


def connect(block_of, block_to, kind='connect', **kwargs):
    fn = to_connection if kind == 'connect' else to_skip

    while isinstance(block_to, Architecture):
        block_to = block_to[0]
    while isinstance(block_of, Architecture):
        block_of = block_of[-1]

    if hasattr(block_to, 'offset'):
        ckwargs = {
                'of': block_of.name,
                'to': block_to.name,
        }

        if 'pos1' in kwargs:
            ckwargs['pos1'] = kwargs['pos1']
        if 'pos2' in kwargs:
            ckwargs['pos2'] = kwargs['pos2']

        block = Block(fn, kind, **ckwargs)
        return block


def cage(block_of, block_to):
    fn = cage_between

    while isinstance(block_to, Architecture):
        block_to = block_to[0]
    while isinstance(block_of, Architecture):
        block_of = block_of[-1]

    if hasattr(block_to, 'offset'):
        block = Block(fn, 'cage', name_left=block_of.name, name_right=block_to.name)
        return block


class Architecture(object):
    def __init__(self, name='main', intra_offset=0):
        self.name = name
        self.arch = []
        self.connects = []
        self.intra_offset = intra_offset

        self.counter = 0

    def __call__(self, kind, **kwargs):

        name = '{}_{}_{}'.format(self.name, kind, self.counter)
        print('Name', name)
        kwargs['name'] = name
        self.counter += 1

        prev = None
        if len(self) > 0:
            prev = self[-1]
            dy = kwargs.get('dy', 0)
            dz = kwargs.get('dz', 0)
            dx = self.intra_offset if kind != 'plus' else self.intra_offset + 1
            kwargs['offset'] = '({}, {}, {})'.format(dx, dy, dz)

        if isinstance(kind, str):
            new_block = str2block(kind, prev, **kwargs)

        elif isinstance(kind, Architecture):
            new_block = kind
            if len(new_block) > 0 and len(self) > 0:
                new_block.add_initial_offset(self.intra_offset)
                new_block.add_previous(prev)

        self.arch += [new_block]

        if prev is not None:
            if self.intra_offset != 0:
                self.connects += [connect(prev, new_block)]

                if kind == 'deconv':
                    self.connects += [cage(prev, new_block)]

            if kind == 'plus':
                self.connects += [connect(prev, new_block)]
                self.connects += [connect(new_block.other, new_block, 'skip', **kwargs)]

    def __str__(self):
        as_str = ['%%%%%%%%%\n% {}'.format(self.name)]
        as_str += [str(b) for b in self.arch]

        as_str += ['\n%%%%%\n% Connections']
        as_str += [str(c) for c in self.connects if c is not None]

        return '\n'.join(as_str)

    def add_initial_offset(self, offset):
        block = self.arch[0]
        if isinstance(block, Block):
            block.kwargs['offset'] = '({}, 0, 0)'.format(offset)
            setattr(block, 'offset', '({}, 0, 0)'.format(offset))
            self.arch[0] = block

        elif isinstance(block, Architecture):
            block.add_initial_offset(offset)

    def add_previous(self, prev_block):
        while isinstance(prev_block, Architecture):
            prev_block = prev_block[-1]

        current_block = self[0]
        while isinstance(current_block, Architecture):
            current_block = current_block[0]

        current_block.kwargs['to'] = '({}-east)'.format(prev_block.name)

    def __getitem__(self, idx):
        return self.arch[idx]

    def __len__(self):
        return len(self.arch)


class Wrapper(object):
    def __init__(self, proot='..'):
        self.components = [
                to_head(proot),
                to_cor(),
                to_begin()
                ]

    def __call__(self, arch):
        self.components += [arch]

    def save(self, path):
        self.components += [to_end()]

        with open(path, 'w') as le_file:
            as_str = '\n'.join([str(c) for c in self.components])
            le_file.write(as_str)


def main():

    H = 40
    S = 256
    WW = 2
    N = 32

    E = Architecture('Encoder', 2)
    counter = 0
    for i in range(2, 5):
        H = H / 2
        D = WW * i
        N = N * 2
        S = S / 2

        B = Architecture()
        for j in range(i):
            kwargs = {}
            if j == i-1:
                kwargs = {'n_filer': N, 's_filer': S}
            else:
                kwargs = {'n_filer': '', 's_filer': ''}
            B('conv',
              name='conv_{}'.format(counter),
              height=H,
              depth=H,
              width=D,
              **kwargs)

            counter += 1

        B('pool',
          name='pool_{}'.format(i),
          height=H / 2,
          depth=H / 2,
          width=1)

        E(B)

    BB = Architecture('Bottelneck')
    for i in range(2):
        if i == 1:
            kwargs = {'n_filer': N, 's_filer': S}
        else:
            kwargs = {'n_filer': '', 's_filer': ''}
        BB('conv', name='bottle_{}'.format(i), height=H, depth=H, width=D, **kwargs)
    
    DD = Architecture('Decoder', 2)
    for i in list(range(2, 5))[::-1]:
        B = Architecture()
        kwargs = {}
        B('pool',
          name='uppool_{}'.format(i),
          height=H,
          depth=H,
          width=1)
        H = H * 2
        D = WW * i
        N = N / 2
        S = S * 2
        for j in range(i):
            if j == i-1:
                kwargs = {'n_filer': N, 's_filer': S}
            else:
                kwargs = {'n_filer': '', 's_filer': ''}
            B('conv',
              name='deconv_{}'.format(j + i*j),
              height=H,
              depth=H,
              width=D,
              **kwargs)
        DD(B)

    Net = Architecture('AutoEncoder', intra_offset=1.5)
    Net(E)
    Net(BB)
    Net(DD)

    W = Wrapper()
    W(Net)
    W.save()


class PytorchHook(Architecture):
    '''Allows to generate a model graph from the model directly by registering
    an instance of this class as :function:`forward_hook`.

    Hook
     |- A1
     |   |- C1
     |   |- C2
     |
     |- A2
     |  |- C1
     |  |- A3
     |     |- C1
     |     |- C2
     |
     |- C1

    '''

    leafs = ['Conv2d', 'Linear', 'ReLU']
    name_map = {'Conv2d': 'conf', 'Linear': 'fc', 'ReLU': 'relu'}

    def __init__(self):
        super().__init__('MyModel')

        self.nested_stuff = {}
        self.current = None

    def __call__(self, module, inputs, outputs):
        '''If the module is one of the leaf modules append to the last 
        Architecture, else append a new architecture.
        '''

        module_name = module.__class__.__name__
        if module_name in self.leafs:
            kwargs = {}
            super().__call__(name_map[module_name], **kwargs)
        else:
            A = Architecture(module_name)
            self.current = module_name
            super().__call__(A)



if __name__ == '__main__':
    main()
