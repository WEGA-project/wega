
set terminal png size 900,1000
set output "s.png"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 4,1
set lmargin 10
set rmargin 10
set y2label
set xrange ["2021-02-17 00:00:00" : "2021-02-17 23:59:59"]



plot    \
	"s.csv" using 1:2 w l title "ECtempRAW", \

plot    \
	"s.csv" using 1:3 w l title "ECtemp", \

plot    \
	"s.csv" using 1:4 w l title "RootTemp", \

plot    \
	"s.csv" using 1:3 w l title "ECtemp", \
	"s.csv" using 1:4 w l title "RootTemp", \

