<!DOCTYPE HTML
<HTML>
<HEAD>

<TITLE>remezclemos:publicaciones000</TITLE>

<style type="text/css">
<!--
body {
text-align: left;
min-width: 1080px;
}
a:link {
COLOR: #8470ff;
}
a:visited {
COLOR: #8470ff;
}
a:hover {
COLOR: #8470ff;
}
a:active {
COLOR: #8470ff;
}
#wrapper {
            width: 1080px;
            margin: 0 auto;
            text-align: left;
}
--></style>
</head>

<body><div id="wrapper"><body bgcolor="black">
<center><font face="courier new" size="7" color="#00ff66">
remezclemos.net<br>
<font face=courier new size=4 color=grey>
----------------------------------------------------------------------------------------------------
<br><br>
<center><font size=6 color=#82CAFF>
&iquest;como podr&iacuteamos alcanzar la paz mundial?
<p align=left><font size="4" color="white">

<?php
if ($handle = opendir('publicaciones/000paz')) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            $hypertext = "<a href=".'publicaciones/000paz/'.$entry.">";
            echo "$hypertext"."$entry".'</a><br>';
        }
    }
    closedir($handle);
}
?>

manda sus pensamientos <a href="http://www.remezclemos.net/escribir.html">aqui</a>
<p align=center><font color="grey">
----------------------------------------------------------------------------------------------------
<font face="courier new" size="3" color="white">
<br>
<a href="http://www.remezclemos.net/0.html">principia</a> |
<a href="http://www.remezclemos.net/cuentas.html">cuentas</a> | 
<a href="http://www.remezclemos.net/pubs.html">publicaciones</a> | 
<a href="http://www.remezclemos.net/escribir.html">escribir</a> | 
<a href="http://www.remezclemos.net/info.html">informacion</a> | 
<a href="http://www.remezclemos.net/donar.html">donar</a>
<br><br>
<font face="courier new" size="2" color="grey">
&copy2012 topher qastro
</div></BODY>
</HTML>