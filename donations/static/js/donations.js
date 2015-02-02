$(function(){

    // Set mask
    $('#id_expiration_date').mask('00/00/0000');

    var options = {
        types: ['(cities)'],
        componentRestrictions: {country: "br"}
    };

    // Initialize geocomplete
    $("#id_location").geocomplete(options)
    .bind("geocode:result", function(event, result){
        $("#id_position_0").val(result.geometry.location.lat());
        $("#id_position_1").val(result.geometry.location.lng());
    })
    .bind("geocode:error", function(event, status){
        $("#id_location").val("");
        $("#id_position_0").val("");
        $("#id_position_1").val("");
        alert($("#error_message").val());
    });

    // Check if browser support geolocation API
    if(navigator.geolocation) {
        $("#detect_location").show();
    }

    // Detect your location
    $("#detect_location").click(function(){
        if(!!navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var geocoder = new google.maps.Geocoder();
                var latLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                geocoder.geocode({'latLng': latLng}, function(results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        if (results[1]) {
                            $("#id_location").val(results[1].formatted_address);
                            $("#id_position_0").val(position.coords.latitude);
                            $("#id_position_1").val(position.coords.longitude);
                        }
                    }else{
                        alert($("#error_message").val());
                    }
                });
            });
        }
        return false;
    });

});