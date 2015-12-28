#       File: createmo.sh
#       Script in bash which compiles .po files into .mo and moves to i18n folder
#       
#       This file is part of Pimagizer
#       Pimagizer Copyright 2013-2014 Víctor Fernández Rico <vfrico@gmail.com>
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

mkdir ../src/i18n
# Spanish (ES)
mkdir ../src/i18n/es
msgfmt ../src/i18n-template/es.po -o ../src/i18n/es/pimagizer.mo

# French (FR)
mkdir ../src/i18n/fr
msgfmt ../src/i18n-template/fr.po -o ../src/i18n/fr/pimagizer.mo

# Russian (RU)
mkdir ../src/i18n/ru
msgfmt ../src/i18n-template/ru.po -o ../src/i18n/ru/pimagizer.mo

# Chinese (zh_CN)
mkdir ../src/i18n/zh_CN
msgfmt ../src/i18n-template/zh_CN.po -o ../src/i18n/zh_CN/pimagizer.mo

# Chinese (zh_TW)
mkdir ../src/i18n/zh_TW
msgfmt ../src/i18n-template/zh_TW.po -o ../src/i18n/zh_TW/pimagizer.mo

# Indonesian (ID)
mkdir ../src/i18n/id
msgfmt ../src/i18n-template/id.po -o ../src/i18n/id/pimagizer.mo

# Japanese (JA)
mkdir ../src/i18n/ja
msgfmt ../src/i18n-template/ja.po -o ../src/i18n/ja/pimagizer.mo

# Javanese (JV)
mkdir ../src/i18n/jv
msgfmt ../src/i18n-template/jv.po -o ../src/i18n/jv/pimagizer.mo

# Catalan (CA)
mkdir ../src/i18n/ca
msgfmt ../src/i18n-template/ca.po -o ../src/i18n/ca/pimagizer.mo

