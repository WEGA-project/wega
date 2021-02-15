
set terminal png size 1200,2400
set output "s.png"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
//set multiplot layout 7, 1
set multiplot layout 6,1

set lmargin 10
set rmargin 10
set y2label
set xrange ["2021-01-15 00:00:00" : "2021-02-15 23:59:59"]


############## plot2 temp ######################


set title "Освещенность"
set ylabel "Киллолюксы"

plot    \
	"s.csv" using 1:17 w l title "Датчик освещенности", \

unset ylabel
unset title

set title "Влажность"
set ylabel "%"

plot    \
	"s.csv" using 1:3 w l title "Датчик влажности", \

unset ylabel
unset title




set ylabel "градусы"
set title "Температура"
plot    \
	"s.csv" using 1:4 w l title "Корни", \
	"s.csv" using 1:10 w l title "Бак", \
	"s.csv" using 1:2 w l title "Воздух", \


unset ylabel
unset title


set title "Электропроводность"
set ylabel "mS/cm"

plot    \
	"s.csv" using 1:14 w l title "EC", \
	"s.csv" using 1:15 w l title "ECt", \

unset ylabel
unset title


set title "Уровень в питательном баке"
set ylabel "литры"


plot    \
	"s.csv" using 1:16 w l title "Объем в баке", \

unset ylabel
unset title



set title "Колличество растворенных солей"
set ylabel "граммы"

plot    \
	"s.csv" using 1:18 w l title "Остаток солей", \

unset ylabel
unset title


set title "Кислотно-щелочной баланс"


plot    \
	"s.csv" using 1:19 w l title "pH", \

unset ylabel



