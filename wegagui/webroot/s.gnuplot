
set terminal png size 1900,6080
set output "s.png"
set datafile separator ";"
set xdata time
set format x "%d.%m %H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 10, 1
set lmargin 10
set rmargin 10
set y2label
set xrange ["2020-07-23 00:00:00" : "2020-07-23 23:59:59"]


############## plot2 temp ######################


set ylabel "градусы"
set title "Температура"
plot    \
	"s.csv" using 1:4 w l title "Корни", \
	"s.csv" using 1:10 w l title "Бак", \
	"s.csv" using 1:2 w l title "Воздух", \
	"/var/log/sensors/owm.log" using 1:2 w l title "Улица", \


unset ylabel
unset title

set ylabel "%"
set yrange[0:100]

plot    \
	"/var/log/sensors/owm.log" using 1:($5) w l  title "Облачность", \
	"s.csv" using 1:3 w l title "Влажность", \

unset yrange
unset ylabel


set title "Освещенность"
set ylabel "Люксы"

plot    \
	"s.csv" using 1:17 w l title "Lux", \

unset ylabel
unset title



set ylabel "mS/cm"

plot    \
	"s.csv" using 1:14 w l title "EC", \
	"s.csv" using 1:15 w l title "ECt", \

unset ylabel

plot    \
	"s.csv" using 1:16 w l title "Объем в баке", \

plot    \
	"s.csv" using 1:18 w l title "Остаток солей", \
	"s.csv" using 1:19 w l title "k", \




plot    \
	"s.csv" using 1:5 w l title "aTemp", \

plot    \
	"s.csv" using 1:11 w l title "R2p", \
	"s.csv" using 1:12 w l title "R2n", \
	"s.csv" using 1:13 w l title "R2 среднее", \




plot    \
	"s.csv" using 1:8 w l title "An", \

plot    \
	"s.csv" using 1:9 w l title "Ap", \

plot    \
	"s.csv" using 1:19 w l title "pH", \



