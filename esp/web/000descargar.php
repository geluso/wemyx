<?php include("header.html"); ?>

<TITLE>remezclemos:escribir</TITLE>

<font size=6 color=white>
mandado
<p align=left><font size=4>

<?php

$date = date("YmdHis");
$handle = fopen("mandados/000paz/".$date.".text", "w");
$myContent = $_POST[form];
fwrite($handle, $myContent);
fclose($handle);

?>

<?php include("header.html"); ?>