$(document).ready(function () {


    let time = 0;
    $('#id_hide_macro').click(function () {
        $(this).closest("form").submit();
    });
    $('#id_hide_micro').click(function () {
        $(this).closest("form").submit();
    });

    $('#id_hide_salt').click(function () {
        $(this).closest("form").submit();
    });
 
    $('.precalc').on('keypress change', function () {
        out_list = ['cano3', 'kno3', 'nh4no3', 'mgso4', 'kh2po4', 'k2so4', 'mgno3', 'cacl2',
            'cano3_ca', 'cano3_no3', 'cano3_nh4', 'kno3_k', 'kno3_no3', 'nh4no3_nh4', 'nh4no3_no3', 'mgso4_mg',
            'mgso4_s', 'kh2po4_k', 'kh2po4_p', 'k2so4_k', 'k2so4_s', 'mgno3_mg', 'mgno3_no3', 'cacl2_ca', 'cacl2_cl',
            'n', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', 'fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si',];
        var i;
        var dicts = {};

        dicts['pushed_element'] = $(this).attr('name');
        dicts[$(this).attr('name')] = $(this).val();
        for (i = 0; i < out_list.length; ++i) {
            t = $('#' + 'id_' + out_list[i])
            dicts[out_list[i]] = t.val();
        }


        $.ajax({
            type: "POST",
            url: recalc_url,
            data: JSON.stringify(dicts),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: recalc,
            error: function (errMsg) {
                alert('Ошибка');
            }
        });


    });

    function recalc(data) {

        for (i in data.pp) {

            $("#id_" + i).val(data.pp[i]);
        }


    }


});