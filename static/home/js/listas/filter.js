        $(document).ready(function () {
            $("#frmEstado").change(function () {
                $("#frmEstado option:selected").each(function () {
                    idEstado = $(this).val();
                    //Hace el cambio de datos en el dropdown de los municipios
                    $.post("/CancerInfantil/Municipio2", {idEstado: idEstado}, function (data) {
                        $("#frmMunicipio").html(data);
                        $("#frmLocalidad").prop("disabled", true);
                        $("#frmLocalidad").val("TODOS")
                    });
                });
                if ($("#frmEstado").val() == "TODOS") {
                    $("#frmMunicipio").prop("disabled", true);
                    $("#frmLocalidad").prop("disabled", true);
                    $("#frmLocalidad").val("TODOS")
                    $("#frmMunicipio").val("TODOS")
                } else {
                    $("#frmMunicipio").prop("disabled", false);
                }
            });

            $("#frmMunicipio").change(function () {
                $("#frmMunicipio option:selected").each(function () {
                    idMunicipio = $(this).val();
                    //Hace el cambio de datos en el dropdown de las localidades
                    $.post("/CancerInfantil/Localidad2", {idMunicipio: idMunicipio}, function (data) {
                        $("#frmLocalidad").html(data);
                    });
                });
                if ($("#frmMunicipio").val() == "TODOS") {
                    $("#frmLocalidad").prop("disabled", true);
                } else {
                    $("#frmLocalidad").prop("disabled", false);
                }
            });
        });