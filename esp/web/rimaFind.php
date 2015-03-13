<TITLE>remezclemos:rimas+</TITLE>

<?php include("header.html"); ?>

<?php include("../global/web/rhymeSearch.php"); ?>

<?php

set_time_limit(1800);

$pWord = $_POST[key];
$tVocs = $_POST[totalVs];
$rSyls = $_POST[rSybls];
$clenR = $_POST[cleanR];

if ($clenR == "") {
    $clenR = 2;
}

$vCt = fopen('data/vocsFile.csv', "r+");
$cCt = fopen('data/consFile.csv', "r+");

include("../global/web/V+Cget.php");

if ($rSyls == 0 && $clenR == 0) {
    echo 'sin ni siquiera uno sonido igual, no vas a tener rimas.<br><br>';
    $pWord = "";
}

if ($rSyls > $tVNum) {
    echo "quieres m&aacutes silabas iguales que tiene su palabra. vamos a cambiar este numero para representar el m&aacuteximo<br><br>";
    $rSyls = $tVNum;
    $rSybls = $tVNum;
}

if (($tVocs < 1) || (10 < $tVocs) || ($tVocs == "")) {
    $tVocs = $tVNum;
}

if (($rSyls < 0) || (10 < $rSyls) || ($tVNum < $rSyls) || ($rSyls == "")) {
    $rSyls = $tVNum;
}

if ((in_array($clenR, range(0, 15)) !== TRUE) || ($clenR == "")) {
    $clenR = 3;
}

if (($clenR == 0) & ($rSyls == 0)) {
    $rSyls = $tVNum;
}

if ($rSyls > $tVocs) {
    $rSyls = $tVocs;
}

$printWord = $pWord;
include("../global/web/advancedRhymer.php");

?>


<p align=center><font size=4 color=white>
    <br>
<form name="input" action="rimaFind.php" method="POST">
    <font color=black>xx<font color=white>palabra para rimar:  <input type="text" name="key" size="19">
    <br>
    <font color=black>xxxxxx<font color=white>cantidad total de silabas: <input type="text" name="totalVs" size="1"><font color=black>x<font color=white>
    <br>
    <font color=black>xxxxx<font color=white>silabas iguales al derecho: <input type="text" name="rSybls" size="1"><font color=black>x<font color=white>
    <br>
    <font color=black>x<font color=white>consonantes iguales al derecho: <input type="text" name="cleanR" size="1"><font color=black>x<font color=white>
    <br><br>
    <input type="submit" value="pedir">
</form>
<br><br>
<a href="http://www.remezclemos.net/rimaEasy.php">ir al diccionario m&aacutes facil</a>
<?php include("footer.html"); ?>