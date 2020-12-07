#       File: createpot.sh
#       Script in bash which creates pot files for translations (template)
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

intltool-extract --type="gettext/glade" ../src/pimagizer.glade
#mv -v ../about.glade.h about.glade.h
xgettext -kN_ -o ../src/i18n-template/pimagizer.pot ../bin/pimagizer  ../pimagizer/gtkpimagizer.py ../pimagizer/getimage.py ../src/pimagizer.glade.h --from-code=UTF-8 --language=Python --package-name=pimagizer --package-version=0.4.2 --msgid-bugs-address=vfrico@gmail.com
