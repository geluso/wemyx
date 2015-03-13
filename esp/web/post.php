<?php

$date = date("YmdHis");
$handle = fopen("publicaciones/000paz/".$date.".html", "w");

$myContent = $_POST['poem'];

fwrite($handle, $myContent);

fclose($handle);

?>