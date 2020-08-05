var _audioData;
var _cur_auidoname = '';
var _audioArray = new Array();


$(document).ready(function(){

    // init UI
    _audioArray.length = 0;

     function sendBlob(blob) {
        var reader = new FileReader();
        reader.onloadend = function() {
            audio_base64 = reader.result;
            // sendBase64(audio_base64);
            _audioArray.push(audio_base64);
        }
        reader.readAsDataURL(blob);
    }

    var audioElem = document.getElementById("Add-Audio");
    var audioSelected = null;
    audioElem.onclick = function(e) {
        audioSelected = this.value;
        this.value = null;
    }

    audioElem.value = null;
    audioElem.onchange = function(e) { // will trigger each time

        if (!this.files) return;

        _audioArray.length = 0;

        var reader = new FileReader();
        _cur_auidoname = this.files[0].name;

        reader.readAsArrayBuffer(this.files[0]);
        reader.onload = function(event) {
            wavbuffer = event.target.result;
            var view = new DataView(wavbuffer);
            var blob = new Blob([view], {type: 'audio/wav'});
            sendBlob(blob);
        };
    };

    function handleFileDialog(changed) {
        // boolean parameter if the value has changed (new select) or not (canceled)
    }

    $(".submit-btn").click(function (e) {

        if (_audioArray.length == 0) {
            alert("please select audio file.");
            return;
        }

        _audioData = _audioArray.pop()
        var jsonObj = {
            audio_data: _audioData,
            ext_type: "wav"
        }

        $.ajax({
            url: "/get_tone",
            type: "POST",
            contentType:"application/json; charset=utf-8",
            data: JSON.stringify(jsonObj),
            dataType: "json",
            success: function (response) {

                var html='<ul>';
                ttext = _cur_auidoname + " : " + response['tone'] + "\t\t(confidence:  " + response['score'] + ")";
                html += '<li><a href="javascript:;" style="color: white;" onclick="clickEvent(this)">' + ttext + '</a></li>';

                html += '</ul>';
                $("#click-text").html(html);
                $("#click-text").show();
                // PreviewImg.value = response
            },
            error: function (request, response) {
                alert("Web server Error. Try again later.");
                return ;
            },
            complete: function(response) {
            }
        });
    });

});


function clickEvent(index) {
    var x = document.createElement("AUDIO");
    x.src = _audioData;

    x.play();

}
