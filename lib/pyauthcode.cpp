#include <iostream>
using namespace std;

#include "cryptopp/osrng.h"
using CryptoPP::AutoSeededRandomPool;

#include "cryptopp/cryptlib.h"
using CryptoPP::Exception;

#include "cryptopp/cmac.h"
using CryptoPP::CMAC;

#include "cryptopp/aes.h"
using CryptoPP::AES;

#include "cryptopp/hex.h"
using CryptoPP::HexEncoder;
using CryptoPP::HexDecoder;

#include "cryptopp/base64.h"
using CryptoPP::Base64Encoder;

#include "cryptopp/hex.h"
using CryptoPP::HexEncoder;

#include "cryptopp/filters.h"
using CryptoPP::Filter;
using CryptoPP::StringSink;
using CryptoPP::StringSource;
using CryptoPP::HashFilter;
using CryptoPP::HashVerificationFilter;

#include "cryptopp/secblock.h"
using CryptoPP::SecByteBlock;

enum { KEY_LEN = 32 };

extern "C" {

  static char *mk_result(const string& encoded)
  {
    size_t len = encoded.length();
    char *out = new char[len + 1];
    memcpy(out, encoded.c_str(), len);
    out[len] = 0;
    return out;
  }

  static char *authcode_b64(const string& mac)
  {
    string encoded;
    encoded.clear();
    StringSource ss3(mac, true, new Base64Encoder(new StringSink(encoded)));
    return mk_result(encoded);
  }

  static char *authcode_hex(const string& mac)
  {
    string encoded;
    encoded.clear();
    StringSource ss3(mac, true, new HexEncoder(new StringSink(encoded), false));
    return mk_result(encoded);
  }

  char *gen_authcode(const char *keydata, const char *data, int b64)
  {
    SecByteBlock key(KEY_LEN);
    memcpy(key.data(), keydata, key.size());
    StringSink *sshc2 = 0;
    Filter *hc2 = 0;
    string mac;
    mac.clear();
    try
      {
        CMAC<AES> cmac(key.data(), key.size());
        StringSource ss2(data, true, new HashFilter(cmac, new StringSink(mac)));
      }
    catch(const CryptoPP::Exception& e)
      {
        cerr << e.what() << endl;
        return false;
      }
    return b64 ? authcode_b64(mac) : authcode_hex(mac);
  }

  void free_authcode(char *authcode)
  {
    delete authcode;
  }
}

