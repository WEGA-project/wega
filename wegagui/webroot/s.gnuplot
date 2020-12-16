
set terminal png size 1400,800
set output "s.png"
set datafile separator ";"
set grid
set xlabel "RAW"
set ylabel "Объем в литрах"
set multiplot layout 2,2

set label "Текущий уровень" at 7.525,8.734482765197754 point pointtype 7

plot    \
	"s.csv" using 1:2 w l title "", \
	"s.csv" using 1:2 w p pt 6 title "", \

set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set xlabel "Дата/Время"
set ylabel "RAW"

plot    \
	"tmp/lev.csv" using 1:2 w l title "", \

set grid ytics mytics
set mytics 2

set ylabel "Объем в литрах"
plot    \
	"tmp/lev.csv" using 1:3 w l title "", \

