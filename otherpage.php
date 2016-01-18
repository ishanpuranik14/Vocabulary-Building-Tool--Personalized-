<html>
<head>
  <title>Learn</title>
</head>
<body>
<?php
  ini_set('max_execution_time', 300);

  function jsonRemoveUnicodeSequences($struct) {
   return preg_replace("/\\\\u([a-f0-9]{4})/e", "iconv('UCS-4LE','UTF-8',pack('V', hexdec('U$1')))", json_encode($struct));
  }

  // Database Connection
  $conn = mysql_connect("localhost","root" ,"");
  if(! $conn )
  {
   die('Could not connect: ' . mysql_error());
  }
  //echo 'Connected successfully';
  mysql_select_db("cl-master");

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
      //echo "uid : $uid <br/>";
      $level = $row[1];
      $wordsleft = $row[2];      
      $sql = "select wid,sentence from articlewordmeta where uid='$uid' and level=$level";        // get the words and sentences for that article
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
          $widArray[$wid] = 0;                                                // for each such word store distinct wids so that meanings can be fetched          
          if($wordsleft == 0){
            echo "No words left to master for current configuration. try changing levels or interests";
            echo "<a href = 'trial.php'>Home</a>";
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
      echo "<h2>Word : Meaning(s)</h2>";
      foreach ($widArray as $wida => $v){                                       //Display meanings of words
        echo "<br />";
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
      echo "<br />";
      echo "<h2>Sentences</h2><br />";
      if(count($sentences) == 1){
        if(($sentence-1)>=0){
          array_unshift($sentences, $myArray[$sentence-1]);
        }
        if(($sentence+1)<count($myArray)){
          array_push($sentences, $myArray[$sentence+1]);
        }
      }
      foreach ($sentences as $value) {
        echo "<p>".html_entity_decode(mb_convert_encoding($value, "HTML-ENTITIES"))."</p>";
        //echo "<p>".jsonRemoveUnicodeSequences($value)."</p>";
      }

    }     //end while
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
<form action="otherpage.php" method="post">
  <input type="submit" name="formSubmit" value="Next Word(s)" />
</form> 
</body>
</html>