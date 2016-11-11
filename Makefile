all: SPTK-3.9
	cd SPTK-3.9 && \
	./configure --prefix=`pwd`/../sptk && \
	make && \
	make install
	git clone https://github.com/MattShannon/mcd.git
	pip install htk-io

SPTK-3.9:
	wget http://downloads.sourceforge.net/project/sp-tk/SPTK/SPTK-3.9/SPTK-3.9.tar.gz
	tar xf SPTK-3.9.tar.gz

