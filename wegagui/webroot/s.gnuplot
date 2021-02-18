
set terminal png size 1900,1500
set output "s.png"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 5,2
set lmargin 10
set rmargin 10
set y2label
set xrange ["2021-02-11 00:00:00" : "2021-02-18 23:59:59"]



plot    \
	"s.csv" using 1:2 w l title "RAW(-)", \


plot    \
	"s.csv" using 1:3 w l title "RAW(+)", \

plot    \
	"s.csv" using 1:5 w l title "R2(-)", \


plot    \
	"s.csv" using 1:6 w l title "R2(+)", \

plot    \
	"s.csv" using 1:5 w l title "R2(+)", \
	"s.csv" using 1:6 w l title "R2(-)", \
	"s.csv" using 1:7 w l title "R2", \

plot    \
	"s.csv" using 1:7 w l title "R2", \

plot    \
	"s.csv" using 1:8 w l title "EC", \

plot    \
	"s.csv" using 1:9 w l title "tR", \

plot    \
	"s.csv" using 1:8 w l title "EC", \
	"s.csv" using 1:10 w l title "ECt", \


