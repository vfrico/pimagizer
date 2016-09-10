# File: createmo.sh
# Script in bash which compiles .po files into .mo and moves to i18n folder
#
# This file is part of Pimagizer
# Pimagizer Copyright 2013-2014 Víctor Fernández Rico <vfrico@gmail.com>
#
# Pimagizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pimagizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

SRCPATH="$PWD/src"
echo $PWD

rm -rf $SRCPATH/i18n/ 
mkdir $SRCPATH/i18n

# Spanish (ES)
mkdir $SRCPATH/i18n/es
msgfmt $SRCPATH/i18n-template/es.po -o $SRCPATH/i18n/es/pimagizer.mo

# French (FR)
mkdir $SRCPATH/i18n/fr
msgfmt $SRCPATH/i18n-template/fr.po -o $SRCPATH/i18n/fr/pimagizer.mo

# Russian (RU)
mkdir $SRCPATH/i18n/ru
msgfmt $SRCPATH/i18n-template/ru.po -o $SRCPATH/i18n/ru/pimagizer.mo

# Chinese (zh_CN)
mkdir $SRCPATH/i18n/zh_CN
msgfmt $SRCPATH/i18n-template/zh_CN.po -o $SRCPATH/i18n/zh_CN/pimagizer.mo

# Chinese (zh_TW)
mkdir $SRCPATH/i18n/zh_TW
msgfmt $SRCPATH/i18n-template/zh_TW.po -o $SRCPATH/i18n/zh_TW/pimagizer.mo

# Indonesian (ID)
mkdir $SRCPATH/i18n/id
msgfmt $SRCPATH/i18n-template/id.po -o $SRCPATH/i18n/id/pimagizer.mo

# Japanese (JA)
mkdir $SRCPATH/i18n/ja
msgfmt $SRCPATH/i18n-template/ja.po -o $SRCPATH/i18n/ja/pimagizer.mo

# Javanese (JV)
mkdir $SRCPATH/i18n/jv
msgfmt $SRCPATH/i18n-template/jv.po -o $SRCPATH/i18n/jv/pimagizer.mo

# Catalan (CA)
mkdir $SRCPATH/i18n/ca
msgfmt $SRCPATH/i18n-template/ca.po -o $SRCPATH/i18n/ca/pimagizer.mo
