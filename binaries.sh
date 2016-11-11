AWK=mawk
PERL=/usr/bin/perl
BC=/usr/bin/bc
TCLSH=/usr/bin/tclsh
WC=/usr/bin/wc

bin=`pwd`/bin
X2X=$bin/x2x
FRAME=$bin/frame
WINDOW=$bin/window
MGCEP=$bin/mcep
LPC2LSP=$bin/lpc2lsp
STEP=$bin/step
MERGE=$bin/merge
VSTAT=$bin/vstat
NRAND=$bin/nrand
SOPR=$bin/sopr
VOPR=$bin/vopr
NAN=$bin/nan
MINMAX=$bin/minmax

SAMPFREQ=16000   # Sampling frequency (48kHz)
FRAMELEN=400   # Frame length in point (1200 = 48000 * 0.025)
FRAMESHIFT=80 # Frame shift in point (240 = 48000 * 0.005)
WINDOWTYPE=1 # Window type -> 0: Blackman 1: Hamming 2: Hanning
NORMALIZE=1  # Normalization -> 0: none  1: by power  2: by magnitude
FFTLEN=512     # FFT length in point
FREQWARP=0.42   # frequency warping factor
GAMMA=0      # pole/zero weight for mel-generalized cepstral (MGC) analysis
MGCORDER=34   # order of MGC analysis
STRORDER=5     # order of STR analysis, number of filter banks for mixed excitation
MAGORDER=10    # order of Fourier magnitudes for pulse excitation generation
LNGAIN=1     # use logarithmic gain rather than linear gain
LOWERF0=10    # lower limit for f0 extraction (Hz)
UPPERF0=400    # upper limit for f0 extraction (Hz)
NOISEMASK=50 
