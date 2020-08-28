
set terminal png size 1900,1000
set output "s.png"
set datafile separator ";"
set xdata time
//set format x "%d.%m %H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
set multiplot layout 4, 2
set lmargin 10
set rmargin 10
set y2label
set xrange ["2020-08-28 00:00:00" : "2020-08-28 23:59:59"]



plot    \
	"s.csv" using 1:2 w l title "AM2302_1_t", \

plot    \
	"s.csv" using 1:3 w l title "AM2302_1_h", \

plot    \
	"s.csv" using 1:4 w l title "18b20_1_t", \

plot    \
	"s.csv" using 1:5 w l title "thermistor_1_raw", \

plot    \
	"s.csv" using 1:6 w l title "1023-phtresist_1_raw", \

plot    \
	"s.csv" using 1:7 w l title "us25_1_dst", \

plot    \
	"s.csv" using 1:8 w l title "ec_1_an", \

plot    \
	"s.csv" using 1:9 w l title "ec_1_ap", \


