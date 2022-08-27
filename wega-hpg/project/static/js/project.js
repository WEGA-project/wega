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

    $('#id_show_gramms').click(function () {
        $(this).closest("form").submit();
    });







    function precalc(element) {

        out_list = ['cano3', 'kno3', 'nh4no3', 'mgso4', 'kh2po4', 'k2so4', 'mgno3', 'cacl2',
            'cano3_ca', 'cano3_no3', 'cano3_nh4', 'kno3_k', 'kno3_no3', 'nh4no3_nh4', 'nh4no3_no3', 'mgso4_mg',
            'mgso4_s', 'kh2po4_k', 'kh2po4_p', 'k2so4_k', 'k2so4_s', 'mgno3_mg', 'mgno3_no3', 'cacl2_ca', 'cacl2_cl',
            'n', 'no3', 'nh4', 'p', 'k', 'ca', 'mg', 's', 'cl', 'fe', 'mn', 'b', 'zn', 'cu', 'mo', 'co', 'si',
        'gfe', 'gmn', 'gb', 'gzn', 'gcu', 'gmo', 'gco', 'gsi', 'dfe', 'dmn', 'db', 'dzn', 'dcu', 'dmo', 'dco', 'dsi',  ];

        var i;
        var dicts = {};
        dicts['pushed_element'] = $(element.target).attr('name');
        dicts['calc_mode'] = $("#id_calc_mode").val();
        dicts['micro_calc_mode'] = $("#id_micro_calc_mode").val();
        dicts['litres'] = $("#id_litres").val();
        dicts['id_npk_formula'] = $("#id_npk_formula").val();
        dicts['id_npk_magazine'] = $("#id_npk_magazine").val();
        dicts['nh4_nh3_ratio'] = $("#id_nh4_nh3_ratio").val();
        dicts[$(element.target).attr('name')] = $(element.target).val();

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

        return true};

    $('.precalc').on('change', precalc);

    function recalc(data) {
          console.log('data.pp.micro_calc_mode', data.pp.micro_calc_mode,  );
        if(data.pp.calc_mode =='K'){
            $("#id_kno3").prop("disabled", false);
             $("#id_mgno3").prop("disabled", true);
            } else {
                $("#id_mgno3").prop("disabled", false);
                $("#id_kno3").prop("disabled", true);
            }

            if (data.pp.micro_calc_mode == "u"){
              $('#id_gfe').removeClass('d-none');
            $('#id_gmn').removeClass('d-none');
            $('#id_gzn').removeClass('d-none');
            $('#id_gcu').removeClass('d-none');
            $('#id_gmo').removeClass('d-none');
            $('#id_gco').removeClass('d-none');
            $('#id_gsi').removeClass('d-none');
            $('#id_gb').removeClass('d-none');


            $('#id_fe').prop("disabled", false);
            $('#id_mn').prop("disabled", false);
            $('#id_zn').prop("disabled", false);
            $('#id_cu').prop("disabled", false);
            $('#id_mo').prop("disabled", false);
            $('#id_co').prop("disabled", false);
            $('#id_si').prop("disabled", false);
        }

        if ( data.pp.micro_calc_mode == 'b' ){


            $('#id_gfe').addClass('d-none');
            $('#id_gmn').addClass('d-none');
            $('#id_gzn').addClass('d-none');
            $('#id_gcu').addClass('d-none');
            $('#id_gmo').addClass('d-none');
            $('#id_gco').addClass('d-none');
            $('#id_gsi').addClass('d-none');
            $('#id_gb').addClass('d-none');


            $('#id_fe').prop("disabled", true);
            $('#id_mn').prop("disabled", true);
            $('#id_zn').prop("disabled", true);
            $('#id_cu').prop("disabled", true);
            $('#id_mo').prop("disabled", true);
            $('#id_co').prop("disabled", true);
            $('#id_si').prop("disabled", true);
        }

        for (i in data.pp) {

            if (i == 'calc_mode' || i=='micro_calc_mode'){
                  $("#id_" + i+ "option[value="+data.pp[i]+"]").prop('selected', true);

                }  else {
            $("#id_" + i).attr('value', data.pp[i]);
            $("#id_" + i).val( data.pp[i]);
            $("#id_" + i).text( data.pp[i]);}
        }
        $("#id_litres2").text( data.pp.litres);



    };


});