
set terminal png size 1000,2000
set output "s.png"
set datafile separator ";"
set xdata time
set format x "%d.%m\n%H:%M"
set timefmt "%Y-%m-%d %H:%M:%S"
set grid
//set multiplot layout 7, 1
set multiplot layout 4,1

set lmargin 10
set rmargin 10
set y2label
set xrange ["2021-02-25 00:00:00" : "2021-02-25 23:59:59"]


############## plot2 temp ######################
set title "Погодные условия - облачность"
set ylabel "%"
set yrange[0:100]

plot    \
	"/var/log/sensors/owm.log" using 1:($5) w boxes fs solid 0.01 title "Облачность" lc rgb "grey", \

unset yrange
unset ylabel
unset title



set title "Погодные условия - влажность"
set ylabel "%"

plot    \
	"/var/log/sensors/owm.log" using 1:3 w l title "Относительная влажность", \

unset ylabel
unset title


set title "Погодные условия - Температура"
set ylabel "градусы"
plot    \
	"/var/log/sensors/owm.log" using 1:2 w l title "Улица", \


unset ylabel
unset title


set title "Погодные условия - Атмосферное давление"
set ylabel "мм. ртутного столба"

plot    \
	"/var/log/sensors/owm.log" using 1:($4/1.333333) w l title "Давление", \

unset ylabel
unset title




