$(document).ready(function () {

    var hash = location.hash.replace(/^#/, '');  // ^ means starting, meaning only match the first hash
    if (hash) {
        $('.nav-tabs a[data-hash-target="#' + hash + '"]').tab('show');
    }


    $('.nav-tabs a').on('shown.bs.tab', function (e) {
        window.location.hash = e.target.dataset.hashTarget;

    })

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
                    'gfe', 'gmn', 'gb', 'gzn', 'gcu', 'gmo', 'gco', 'gsi', 'dfe', 'dmn', 'db', 'dzn', 'dcu', 'dmo', 'dco', 'dsi',
                    'taml', 'tbml', 'gml_fe', 'gml_mn', 'gml_b', 'gml_zn', 'gml_cu', 'gml_mo', 'gml_co',
                    'gml_si', 'gml_cano3', 'gml_kno3', 'gml_nh4no3', 'gml_mgno3', 'gml_mgso4', 'gml_k2so4',
                    'gml_kh2po4', 'gml_cacl2', 'gml_cmplx', 'gl_fe', 'gl_mn', 'gl_b', 'gl_zn',
                    'gl_cu', 'gl_mo', 'gl_co', 'gl_si', 'gl_cano3', 'gl_kno3', 'gl_nh4no3', 'gl_mgno3',
                    'gl_mgso4', 'gl_k2so4', 'gl_kh2po4', 'gl_cacl2', 'gl_cmplx', 'ml_cano3', 'gg_cano3',
                    'ml_kno3', 'gg_kno3', 'ml_nh4no3', 'gg_nh4no3', 'ml_mgno3', 'gg_mgno3', 'ml_cacl2',
                    'gg_cacl2', 'ml_mgso4', 'ml_kh2po4', 'ml_k2so4', 'ml_fe', 'ml_mn', 'ml_b', 'ml_zn',
                    'ml_cu', 'ml_mo', 'ml_co', 'ml_si', 'ml_cmplx', 'gg_mgso4', 'gg_kh2po4', 'gg_k2so4',
                    'gg_fe', 'gg_mn', 'gg_b', 'gg_zn', 'gg_cu', 'gg_mo','gg_co', 'gg_si', 'gg_cmplx', 'ec'];

        var i;
        var dicts = {};

        dicts['pushed_element'] = $(element.target).attr('name');

        dicts['calc_mode'] = $("#id_calc_mode").val();
        dicts['micro_calc_mode'] = $("#id_micro_calc_mode").val();
        dicts['litres'] = $("#id_litres").val();
        dicts['id_npk_formula'] = $("#id_npk_formula").val();
        dicts['id_npk_magazine'] = $("#id_npk_magazine").val();
        dicts['nh4_nh3_ratio'] = $("#id_nh4_nh3_ratio").val();



        for (i = 0; i < out_list.length; ++i) {
            let t = $('#' + 'id_' + out_list[i]);

            dicts[out_list[i]] = t.val();
        }
        dicts[$(element.target).attr('name')] = $(element.target).val();
        console.log(dicts[$(element.target).attr('name')]);
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

                $('#mixer-fe').removeClass('d-none');
                $('#mixer-mn').removeClass('d-none');
                $('#mixer-zn').removeClass('d-none');
                $('#mixer-cu').removeClass('d-none');
                $('#mixer-mo').removeClass('d-none');
                $('#mixer-co').removeClass('d-none');
                $('#mixer-si').removeClass('d-none');
                $('#mixer-b').removeClass('d-none');


                $('#conc-fe').removeClass('d-none');
                $('#conc-mn').removeClass('d-none');
                $('#conc-zn').removeClass('d-none');
                $('#conc-cu').removeClass('d-none');
                $('#conc-mo').removeClass('d-none');
                $('#conc-co').removeClass('d-none');
                $('#conc-si').removeClass('d-none');
                $('#conc-b').removeClass('d-none');

                $('#p_fe').removeClass('d-none');
                $('#p_mn').removeClass('d-none');
                $('#p_zn').removeClass('d-none');
                $('#p_cu').removeClass('d-none');
                $('#p_mo').removeClass('d-none');
                $('#p_co').removeClass('d-none');
                $('#p_si').removeClass('d-none');
                $('#p_b').removeClass('d-none');
                $('#p_cmplx').addClass('d-none');

                    $('#mixer-cmplx').addClass('d-none');
                    $('#conc-cmplx').addClass('d-none');
                $('#grams_micro_up').removeClass('d-none');




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

            $('#mixer-fe').addClass('d-none');
            $('#mixer-mn').addClass('d-none');
            $('#mixer-zn').addClass('d-none');
            $('#mixer-cu').addClass('d-none');
            $('#mixer-mo').addClass('d-none');
            $('#mixer-co').addClass('d-none');
            $('#mixer-si').addClass('d-none');
            $('#mixer-b').addClass('d-none');



            $('#p_fe').addClass('d-none');
                $('#p_mn').addClass('d-none');
                $('#p_zn').addClass('d-none');
                $('#p_cu').addClass('d-none');
                $('#p_mo').addClass('d-none');
                $('#p_co').addClass('d-none');
                $('#p_si').addClass('d-none');
                $('#p_b').addClass('d-none');
                $('#p_cmplx').removeClass('d-none');


              $('#conc-fe').addClass('d-none');
                $('#conc-mn').addClass('d-none');
                $('#conc-zn').addClass('d-none');
                $('#conc-cu').addClass('d-none');
                $('#conc-mo').addClass('d-none');
                $('#conc-co').addClass('d-none');
                $('#conc-si').addClass('d-none');
                $('#conc-b').addClass('d-none');


            $('#conc-cmplx').removeClass('d-none');
            $('#mixer-cmplx').removeClass('d-none');
            $('#grams_micro_up').addClass('d-none');
            $('#id_weight_micro').prop("disabled", false);



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
                  $("#id_" + i+ "option[value="+data.pp[i]+"]").prop('selected', true); }

            else
                if (i=='mixer_btn_link'){

                      $("#id_" + i).attr("href",data.pp[i]);
                }
                else
                  {

                      $('[id=id_' + i).each(function () {

                        let t = $(this);
                        t.val( data.pp[i]);
                        t.text( data.pp[i]);
                      });




                    }
        }

        for (i in data.pp.errors) {


             if (data.pp.errors[i]==true){

                 $("#id_"+i).addClass('text-danger');
             } else {
                 $("#id_"+i).removeClass('text-danger');
             }
        }

        $("#id_litres2").text( data.pp.litres);





    };


});