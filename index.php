<!doctype html>
<html lang="ru">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Мои дубликаты</title>


</head>
<body>

    <div id="error"></div>
    <button id="button_names">Найти дубликаты</button>
    <div id="duplicates"></div>

<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>

<script>

    var d = '<?php echo $_REQUEST['DOMAIN'];?>';
    var a = '<?php echo $_REQUEST['AUTH_ID'];?>';

    $(document).on('click', '#button_names', function(event) {
        doc = document.getElementById("duplicates");
        doc.innerHTML = '';
        event.preventDefault();
        $.post("https://typhoonseryi.pythonanywhere.com/", {'domain': d, 'auth': a}, function(json) {
            json.result.forEach(e => doc.innerHTML += '<p align="center">' + e + '</p><hr/>');
            document.getElementById("error").innerHTML = ''
        })
        .done(function(msg){  })
        .fail(function(xhr, status, error) {
            document.getElementById("error").innerHTML = '<p style="color:red;">' +
                                                        xhr.status + ': ' + xhr.responseJSON.error + '</p>';
        });
    });


</script>

</body>
</html>