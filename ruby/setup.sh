#!/bin/sh

# ruby
wget http://cache.ruby-lang.org/pub/ruby/2.1/ruby-2.1.0.tar.gz
tar xvzf ./ruby-2.1.0.tar.gz
cd ruby-2.1.0
./configure
make
make install
rm -rf ruby-2.1.0
