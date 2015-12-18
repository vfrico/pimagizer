#!/bin/bash
#       File: builddeb.sh
#       Script in bash which makes a lot easier the task of 
#       building a deb package. Only works if version is given: A.B.C
#       
#       This file is part of Pimagizer
#       Pimagizer Copyright 2014 Víctor Fernández Rico <vfrico@gmail.com>
#
#       Pimagizer is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       Pimagizer is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.
#This file is intended to be on tools folder
cd ..
python setup.py sdist
a=$(ls dist/ -1)
name=${a:0:9}
v=${a: -12}
version=${v:0:6}
final=$name"_"$version"orig.tar.gz"
mv dist/$a ../$final

dpkg-buildpackage --force-sign
