# *****************************************************************************
#  Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of the NVIDIA CORPORATION nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL NVIDIA CORPORATION BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# *****************************************************************************

import argparse


def parse_fastpitch_args(parent, add_help=False):
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser(parents=[parent], add_help=add_help,
                                     allow_abbrev=False)
    io = parser.add_argument_group('io parameters')
    io.add_argument('--n-mel-channels', default=80, type=int,
                    help='Number of bins in mel-spectrograms')

    symbols = parser.add_argument_group('symbols parameters')
    symbols.add_argument('--symbol-type', default='char', type=str,
                         help='Input symbol type')
    symbols.add_argument('--n-symbols', default=148, type=int,
                         help='Number of symbols in dictionary')
    symbols.add_argument('--padding-idx', default=0, type=int,
                         help='Index of padding symbol in dictionary')
    symbols.add_argument('--symbols-embedding-dim', default=384, type=int,
                         help='Input embedding dimension')

    arch = parser.add_argument_group('model-wide architecture parameters')
    arch.add_argument('--use-sepconv', action='store_true',
                      help='Use depthwise separable convolutions')
    arch.add_argument('--use-mas', action='store_true',
                      help='Train with monotonic alignment search')

    in_fft = parser.add_argument_group('input FFT parameters')
    in_fft.add_argument('--in-fft-n-layers', default=6, type=int,
                        help='Number of FFT blocks')
    in_fft.add_argument('--in-fft-n-heads', default=1, type=int,
                        help='Number of attention heads')
    in_fft.add_argument('--in-fft-d-head', default=64, type=int,
                        help='Dim of attention heads')
    in_fft.add_argument('--in-fft-conv1d-kernel-size', default=3, type=int,
                        help='Conv-1D kernel size')
    in_fft.add_argument('--in-fft-conv1d-filter-size', default=1536, type=int,
                        help='Conv-1D filter size')
    in_fft.add_argument('--in-fft-sepconv', action='store_true',
                        help='Use depthwise separable convolutions')
    in_fft.add_argument('--in-fft-output-size', default=384, type=int,
                        help='Output dim')
    in_fft.add_argument('--in-fft-post-cond', action='store_true',
                        help='Add conditioning after FFT blocks')
    in_fft.add_argument('--p-in-fft-dropout', default=0.1, type=float,
                        help='Dropout probability')
    in_fft.add_argument('--p-in-fft-dropatt', default=0.1, type=float,
                        help='Multi-head attention dropout')
    in_fft.add_argument('--p-in-fft-dropemb', default=0.0, type=float,
                        help='Dropout added to word+positional embeddings')

    out_fft = parser.add_argument_group('output FFT parameters')
    out_fft.add_argument('--out-fft-n-layers', default=6, type=int,
                         help='Number of FFT blocks')
    out_fft.add_argument('--out-fft-n-heads', default=1, type=int,
                         help='Number of attention heads')
    out_fft.add_argument('--out-fft-d-head', default=64, type=int,
                         help='Dim of attention head')
    out_fft.add_argument('--out-fft-conv1d-kernel-size', default=3, type=int,
                         help='Conv-1D kernel size')
    out_fft.add_argument('--out-fft-conv1d-filter-size', default=1536, type=int,
                         help='Conv-1D filter size')
    out_fft.add_argument('--out-fft-sepconv', action='store_true',
                        help='Use depthwise separable convolutions')
    out_fft.add_argument('--out-fft-output-size', default=384, type=int,
                         help='Output dim')
    out_fft.add_argument('--p-out-fft-dropout', default=0.1, type=float,
                         help='Dropout probability for out_fft')
    out_fft.add_argument('--p-out-fft-dropatt', default=0.1, type=float,
                         help='Multi-head attention dropout')
    out_fft.add_argument('--p-out-fft-dropemb', default=0.0, type=float,
                         help='Dropout added to word+positional embeddings')

    dur_pred = parser.add_argument_group('duration predictor parameters')
    dur_pred.add_argument('--dur-predictor-kernel-size', default=3, type=int,
                          help='Duration predictor conv-1D kernel size')
    dur_pred.add_argument('--dur-predictor-filter-size', default=256, type=int,
                          help='Duration predictor conv-1D filter size')
    dur_pred.add_argument('--dur-predictor-sepconv', action='store_true',
                          help='Use depthwise separable convolutions')
    dur_pred.add_argument('--p-dur-predictor-dropout', default=0.1, type=float,
                          help='Dropout probability for duration predictor')
    dur_pred.add_argument('--dur-predictor-n-layers', default=2, type=int,
                          help='Number of conv-1D layers')

    pitch_pred = parser.add_argument_group('pitch predictor parameters')
    pitch_pred.add_argument('--pitch-predictor-kernel-size', default=3, type=int,
                            help='Pitch predictor conv-1D kernel size')
    pitch_pred.add_argument('--pitch-predictor-filter-size', default=256, type=int,
                            help='Pitch predictor conv-1D filter size')
    pitch_pred.add_argument('--pitch-predictor-sepconv', action='store_true',
                            help='Use depthwise separable convolutions')
    pitch_pred.add_argument('--p-pitch-predictor-dropout', default=0.1, type=float,
                            help='Pitch probability for pitch predictor')
    pitch_pred.add_argument('--pitch-predictor-n-layers', default=2, type=int,
                            help='Number of conv-1D layers')

    cond = parser.add_argument_group('conditioning parameters')
    cond.add_argument('--pitch-embedding-kernel-size', default=3, type=int,
                      help='Pitch embedding conv-1D kernel size')
    cond.add_argument('--pitch-embedding-sepconv', action='store_true',
                      help='Use depthwise separable convolutions')
    cond.add_argument('--speaker-emb-weight', type=float, default=1.0,
                      help='Scale speaker embedding')
    cond.add_argument('--lang-emb-weight', type=float, default=1.0,
                      help='Scale language embedding')

    return parser
