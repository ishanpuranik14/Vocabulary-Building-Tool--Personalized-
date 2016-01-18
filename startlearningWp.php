<?php

ini_set('max_execution_time', 300);

// Database Connection
$conn = mysql_connect("localhost","root" ,"");
if(! $conn )
{
die('Could not connect: ' . mysql_error());
}
//echo 'Connected successfully';
mysql_select_db("cl-master");

$interests = $_POST['interests'];
$selected_radio = $_POST['level'];
if(empty($interests))
{
echo("Interest not choosen");
}
elseif(count($interests) == 1){
$sql = "SELECT distinct(uid), level FROM articlewordmeta WHERE (uid, level) IN (SELECT uid,level FROM articlewordmeta WHERE level=$selected_radio AND iid=".$interests[0].");";
}
else{
$sql = "SELECT distinct(uid), level FROM articlewordmeta WHERE (uid, level) IN (SELECT uid,level FROM articlewordmeta WHERE level=$selected_radio AND ( iid=".$interests[0]." OR";
$N = count($interests)-1;
for ($i=1; $i < $N ; $i++) {
$temp = " iid=".$interests[$i]." OR";
$sql.=$temp;
}
$temp1 = " iid=".$interests[$N]."));";
$sql.=$temp1;
}

$result = mysql_query( $sql, $conn );
if(! $result)
{
die('Could not get data (articlewordmeta): ' . mysql_error());
}
else
{
while ($row = mysql_fetch_array($result, MYSQL_NUM)) {
$sql1 = "SELECT * FROM articlewordstats WHERE ";
$temp = "uid='".$row[0]."' AND level=".$row[1].";";
$sql1.=$temp;
$result1 = mysql_query( $sql1, $conn );
if(! $result1)
{
die('Could not get data( articlewordstats): ' . mysql_error());
}
else{
while($row1 = mysql_fetch_array($result1, MYSQL_NUM)){
$sql2 = "INSERT INTO operatingtable1 VALUES('".$row1[0]."',".$row1[1].",".$row1[2].",".$row1[3].",".$row1[4].",".$row1[5].");";
$result2 = mysql_query( $sql2, $conn );
if(! $result2)
{
die('Could not insert data (1): ' . mysql_error());
}
}
//mysql_free_result($result2);
}
// Done copying articlewordstats

$sql3 = "SELECT * FROM articlesentencemeta WHERE ";
$sql3.=$temp;
$result3 = mysql_query( $sql3, $conn );
if(! $result3)
{
die('Could not get data (articlesentencemeta): ' . mysql_error());
}
else{
while($row2 = mysql_fetch_array($result3, MYSQL_NUM)){
$sql4 = "INSERT INTO operatingtable3 VALUES('".$row2[0]."',".$row2[1].",".$row2[2].",".$row2[3].",".$row2[4].",".$row2[5].");";
$result4 = mysql_query( $sql4, $conn );
if(! $result4)
{
die('Could not insert data (3): ' . mysql_error());
}
}
//mysql_free_result($result4);
}
}
//mysql_free_result($result1);
//mysql_free_result($result3);
//mysql_free_result($result);
}
//Done with copying of desired rows into 2 tables, now to select and display the most appropriate content

// First get the uid, level and no of words left of the article with most no of distinct words of that level and amongst such articles
// the highest scores

$sql = "select uid,level, nowordsleft from operatingtable1 where fscore in (SELECT max(fscore) FROM `operatingtable1` WHERE nowordsleft in (SELECT max(nowordsleft) from operatingtable1)) LIMIT 1";
$result = mysql_query( $sql, $conn );
if(! $result)
{
die('Could not get data from operatingtable1 : ' . mysql_error());
}
else{
while($row = mysql_fetch_array($result, MYSQL_NUM)){
$breakFlag = 0;
$uid = $row[0];
$sql = "UPDATE sidebar SET uid='$uid' WHERE no=1;";
$result1 = mysql_query( $sql, $conn );
if(! $result1)
{
die('Could not update sidebar : ' . mysql_error());
}
$level = $row[1];
$wordsleft = $row[2];
$sql = "select wid,sentence from articlewordmeta where uid='$uid' and level=$level"; // get the words and sentences for that article
$file = file_get_contents("articles/".$uid.".txt");
$myArray = json_decode($file, true);
$sentences = array();
$result1 = mysql_query( $sql, $conn );
if(! $result1)
{
die('Could not get data from articlewordmeta : ' . mysql_error());
}
else{
while ($row1 = mysql_fetch_array($result1, MYSQL_NUM)) {
$wid = $row1[0];
$sentence = $row1[1]-1;
$widArray[$wid] = 0; // for each such word store distinct wids so that meanings can be fetched
if($wordsleft == 0){
echo "No words left to master for current configuration. try changing levels or interests :)";
echo '<a href="http://localhost/wordpress/select/"> : Go for a fresh Selection</a>';
$breakFlag=1;
break;
// redirect or provide a link to the home page and skip the remaining code
}
else{
if (!in_array($myArray[$sentence], $sentences)) {
array_push($sentences, $myArray[$sentence]);
}

}
}
}
if($breakFlag == 1){
break;
}

echo '
<h2 style="text-align: center;">Word : Meaning(s)</h2>
';
foreach ($widArray as $wida => $v){ //Display meanings of words
echo "
";
$sql = "select word from satwordmap where wid=$wida";
$result3 = mysql_query( $sql, $conn );
if(! $result3)
{
die('Could not get data from satwordmap : ' . mysql_error());
}
else{
while ($row3 = mysql_fetch_array($result3, MYSQL_NUM)) {
$word = $row3[0];
echo "$word : ";
}
}
$sql = "select * from wordmeanings where wid=$wida";
$result2 = mysql_query( $sql, $conn );
if(! $result2)
{
die('Could not get data from wordmeanings : ' . mysql_error());
}
else{
while ($row2 = mysql_fetch_array($result2, MYSQL_NUM)) {
$meaning = $row2[2];
echo "$meaning ; ";
}
}
}
echo "
";
echo '
<h2 style="text-align: center;">Sentences</h2>
';
if(count($sentences) == 1){
$mysentence = $myArray[$sentence];
if(($sentence-1)>=0){
$mysentence = $myArray[$sentence-1].".".$mysentence;
//array_unshift($sentences, $myArray[$sentence-1]);
}
if(($sentence+1)<count($myArray)){
$mysentence = $mysentence.".".$myArray[$sentence+1];
//array_push($sentences, $myArray[$sentence+1]);
}
echo '<ol><li>
<br/><strong>"</strong>
... '.html_entity_decode(mb_convert_encoding($mysentence, "HTML-ENTITIES")).' ...
<strong>"</strong></li></ol><br/>
';
}
else{
echo '<ol>';
foreach ($sentences as $value) {
echo '<li>
<br><strong>"</strong>
... '.html_entity_decode(mb_convert_encoding($value, "HTML-ENTITIES")).' ...
<strong>"</strong></li><br/>
';
}
echo '</ol>';
}
} //end while
}

foreach (array_keys($widArray) as $wid) {
$sql = "UPDATE articlewordmeta SET done=1 WHERE wid=$wid";
$result = mysql_query( $sql, $conn );
if(! $result)
{
die('Could not get update in articlewordmeta : ' . mysql_error());
}
}

$sql = "SELECT uid,level,sentence from articlewordmeta where wid=";
$count = 0;
foreach (array_keys($widArray) as $wid) {
$count++;
if($count>1){
$sql.=" OR wid=";
}
$sql.=$wid;
}

$result = mysql_query( $sql, $conn );
if(! $result)
{
die('Could not get fetch from articlewordmeta : ' . mysql_error());
}
else{
while ($row = mysql_fetch_array($result, MYSQL_NUM)) {
$uid=$row[0];
$level=$row[1];
$sentence=$row[2];
$sql="UPDATE operatingtable3 SET nowordsleft=nowordsleft-1 , nowordsshown=nowordsshown+1, score=score-5 WHERE ( uid='$uid' AND sentence=$sentence AND level=$level);";
$result1 = mysql_query( $sql, $conn );
if(! $result1)
{
die('Could not update from operatingtable3 : ' . mysql_error());
}
$sql = "UPDATE operatingtable1 SET nowordsleft=nowordsleft-1 , nowordsshown=nowordsshown+1, score=score-5 WHERE ( uid='$uid' AND level=$level);";
$result1 = mysql_query( $sql, $conn );
if(! $result1)
{
die('Could not update operatingtable1 : ' . mysql_error());
}
$sql = " SELECT score from articlebirdseye where uid='$uid' and level=$level;";
$result1 = mysql_query( $sql, $conn );
if(! $result1)
{
die('Could not fetch from articlebirdseye : ' . mysql_error());
}
else{
while($row1 = mysql_fetch_array($result1, MYSQL_NUM)){
$ofscore = $row1[0];
$sql = "UPDATE operatingtable1 SET fscore=(score+(0.3*$ofscore)) WHERE ( uid='$uid' AND level=$level);";
$result2 = mysql_query( $sql, $conn );
if(! $result2)
{
die('Could not update fscore in operatingtable1 : ' . mysql_error());
}
}
}
}
}

mysql_close($conn);

?>