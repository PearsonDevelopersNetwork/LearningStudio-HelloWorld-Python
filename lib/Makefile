CPP=g++
#CPP_OPT=-I./cryptopp -L./cryptopp
LNK_OPT=-lcryptopp
LIB_NAME=pyauthcode

all:
	${CPP} ${CPP_OPT} -c -fPIC ${LIB_NAME}.cpp -o ${LIB_NAME}.o
	${CPP} ${CPP_OPT} -shared -Wl,-soname,lib${LIB_NAME}.so -o lib${LIB_NAME}.so ${LIB_NAME}.o ${LNK_OPT}

clean:
	rm -f *.*o

