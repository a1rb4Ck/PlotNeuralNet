#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plot a Siamese Neural Network Architecture.

Figure reproduced from 'Figure 1: Siamese Neural Network Architecture', in:
"A Deep Siamese Neural Network Learns the Human-Perceived Similarity
Structure of Facial Expressions Without Explicit Categories"
by Sanjeev Jagannatha Rao, Yufei Wang, Garrison W. Cottrell
in CogSci 2016

Original Siamese ideas in:
"Neural Networks for Fingerprint Recognition"
by Pierre Baldi, Yves Chauvin.
in Neural Computation Volume 5 Issue 3, May 1996

"Signature Verification Using a "Siamese" Time Delay Neural Network"
by Jane Bromley, Isabelle Guyon, Yann LeCun, Eduard Sickinger, Roopak Shah
in NIPS'93
"""

import sys

from pycore.blocks import to_head
from pycore.blocks import to_cor
from pycore.blocks import to_begin
from pycore.blocks import to_end
from pycore.blocks import to_generate

from pycore.blocks import to_input
from pycore.blocks import to_legend
from pycore.blocks import to_ConvRelu
from pycore.blocks import to_Pool
from pycore.blocks import to_FcRelu
from pycore.blocks import block_ConvPool
from pycore.blocks import to_connection
from pycore.blocks import to_SoftMax

sys.path.append('../../')

# Network architecture
arch = [
    to_head('../..'),
    to_cor(),
    to_begin(),

    # A section
    *to_input(pathfile='imgA.jpg', to='(-3,0,0)', width=6.5, height=6.5,
              name='net_in_A'),
    *block_ConvPool(
        name='1_A',
        connect_in=None,
        connect_out='pool_b1_A',
        output_size=96,
        n_filters=11,
        offset='(-1.5,0,0)',
        size=(32, 32, 2),
        opacity=0.5,
        caption='ConvPool1\_A'
    ),
    *block_ConvPool(
        name='b2_A',
        connect_in='pool_b1_A',
        connect_out='pool_b2_A',
        output_size=13,
        n_filters=256,
        offset='(2,0,0)',
        size=(22, 22, 4),
        opacity=0.5,
        caption='ConvPool2\_A'
    ),
    *block_ConvPool(
        name='b3_A',
        connect_in='pool_b2_A',
        connect_out='pool_b3_A',
        output_size=13,
        n_filters=384,
        offset='(1.5,0,0)',
        size=(15, 15, 3.5),
        opacity=0.5,
        caption='ConvPool3\_A'
    ),
    to_FcRelu(
        name='FC1_A',
        output_size=1024,
        offset='(1.5,0,0)',
        to='(pool_b3_A-east)',
        height=2,
        depth=36,
        caption='FC1\_A'
    ),
    to_connection('pool_b3_A', 'FC1_A'),
    to_FcRelu(
        name='FC2_A',
        output_size=256,
        offset='(1.5,0,0)',
        to='(FC1_A-east)',
        height=2,
        depth=18,
        caption='FC2\_A'
    ),
    to_connection('FC1_A', 'FC2_A'),
    to_FcRelu(
        name='FC3_A',
        output_size=2,
        offset='(1.5,0,0)',
        to='(FC2_A-east)',
        height=2,
        depth=8,
        caption='FC3\_A'
    ),
    to_connection('FC2_A', 'FC3_A'),

    # B section
    *to_input(pathfile='imgB.jpg', to='(-3,-10,0)', width=6.5, height=6.5,
              name='net_in_B'),
    *block_ConvPool(
        name='b1_B',
        connect_in=None,
        connect_out='pool_b1_B',
        output_size=96,
        n_filters=11,
        offset='(-1.5,-10,0)',
        size=(32, 32, 2),
        opacity=0.5,
        caption='ConvPool1\_B'
    ),
    *block_ConvPool(
        name='b2_B',
        connect_in='pool_b1_B',
        connect_out='pool_b2_B',
        output_size=13,
        n_filters=256,
        offset='(1.5,0,0)',
        size=(22, 22, 4),
        opacity=0.5,
        caption='ConvPool2\_B'
    ),
    *block_ConvPool(
        name='b3_B',
        connect_in='pool_b2_B',
        connect_out='pool_b3_B',
        output_size=13,
        n_filters=384,
        offset='(2,0,0)',
        size=(15, 15, 3.5),
        opacity=0.5,
        caption='ConvPool3\_B'
    ),
    to_FcRelu(
        name='FC1_B',
        output_size=1024,
        offset='(1.5,0,0)',
        to='(pool_b3_B-east)',
        height=2,
        depth=36,
        caption='FC1\_B'
    ),
    to_connection('pool_b3_B', 'FC1_B'),
    to_FcRelu(
        name='FC2_B',
        output_size=256,
        offset='(1.5,0,0)',
        to='(FC1_B-east)',
        height=2,
        depth=18,
        caption='FC2\_B'
    ),
    to_connection('FC1_B', 'FC2_B'),
    to_FcRelu(
        name='FC3_B',
        output_size=2,
        offset='(1.5,0,0)',
        to='(FC2_B-east)',
        height=2,
        depth=8,
        caption='FC3\_B'
    ),
    to_connection('FC2_B', 'FC3_B'),

    # Constrative Loss
    to_SoftMax(
        name='contr_loss',
        output_size=1,
        offset='(1,-5,0)',
        to='(FC3_A-east)',
        height=6,
        width=6,
        depth=4,
        caption='Contrastive Loss'
    ),
    to_connection('FC3_A', 'contr_loss'),
    to_connection('FC3_B', 'contr_loss'),

    # Legend box
    to_legend(items=[
        to_ConvRelu(
            name='Conv_legend',
            output_size=96,
            n_filters=32, to="(0,0,0)",
            width=2, height=8, depth=8
        ),
        to_Pool(
            name='Pool_legend',
            output_size=48,
            n_filters=32,
            offset="(0,0,0)",
            to="(0,0,0)",
            width=2, height=6, depth=6,
        ),
        to_FcRelu(
            name='FC_legend',
            output_size=100,
            offset='(0,0,0)',
            height=2,
            depth=16
        )
    ], captions=["Conv + ReLu", "Max Pooling", "FC + ReLu"],
       offset='(0,2,0)', column=10, row=-6,),
    to_end()
]

if __name__ == '__main__':
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')
