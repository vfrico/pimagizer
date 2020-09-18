#!/usr/bin/env bash
# File: createmo.sh
# Script in bash which compiles .po files into .mo and moves to i18n folder
#
# This file is part of Pimagizer
# Pimagizer Copyright 2013-2020 Víctor Fernández Rico <vfrico@gmail.com>
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
LANGS=("ca" "es" "fr" "id" "ja" "jv" "ru" "zh_CN" "zh_TW")

SRCPATH="$PWD/src"
echo $PWD

rm -rf $SRCPATH/i18n/ 
mkdir -p $SRCPATH/i18n

for lang in ${LANGS[*]}; do
    mkdir -p $SRCPATH/i18n/$lang/LC_MESSAGES
    msgfmt $SRCPATH/i18n-template/$lang.po -o $SRCPATH/i18n/$lang/LC_MESSAGES/pimagizer.mo
done
