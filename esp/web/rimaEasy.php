<TITLE>remezclemos:rimas</TITLE>

<?php include("header.html"); ?>

<font size=6 color=white>diccionario de rimas</font><br>

<?php include("../global/web/rhymeSearch.php"); ?>

<?php
set_time_limit(1800);

$pWord = $_POST[key];

$clenR = ceil((strlen($pWord)) / 4);

$vCt = fopen('data/vocsFile.csv', "r+");
$cCt = fopen('data/consFile.csv', "r+");

include("../global/web/V+Cget.php");

/* echo $pWord, $tVocs, $rSyls, $clenR; */

$lang = 'eng';
$printWord = $pWord;
include("../global/web/simpleRhymer.php");

?>
<br>
<form name="input" action="rimaEasy.php" method="POST">
    <p align=center><font color=black>x<font color=white>palabra para rimar: <input type="text" name="key">
        <br><br>
        <input type="submit" value="pedir">
</form>
<br><br>
<a href="http://www.remezclemos.net/rimaFind.php">ir al diccionario avanzado</a>

<?php include("footer.html"); ?>