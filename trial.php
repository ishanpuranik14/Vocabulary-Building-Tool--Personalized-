<html>
<head>
  <title>Learn</title>
</head>
<body>

 <?php
 // Database Connection
 
  $conn = mysql_connect("localhost","root" ,"");
  if(! $conn )
  {
   die('Could not connect: ' . mysql_error());
  }
  //echo 'Connected successfully';
  mysql_select_db("cl-master");
  $sql = "DELETE FROM operatingtable1;";
  $result = mysql_query( $sql, $conn );
    if(! $result)
      {
        die('Could not delete operatingtable1 : ' . mysql_error());
      }
  $sql = "DELETE FROM operatingtable3;";
  $result = mysql_query( $sql, $conn );
    if(! $result)
      {
        die('Could not delete operatingtable3 : ' . mysql_error());
      }
  $sql = "UPDATE articlewordmeta SET done=0;";
  $result = mysql_query( $sql, $conn );
    if(! $result)
      {
        die('Could not update articlewordmeta : ' . mysql_error());
      } 
  mysql_close($conn);
  
 ?>
  <form action="checkbox-form1.php" method="post">

    <h1>Select your Interests<br /></h1>
    <input type="checkbox" name="interests[]" value="1" />Personal Technology : News and reviews on devices, apps and more<br />
    <input type="checkbox" name="interests[]" value="2" />India Real Time : Unique analysis and insights from The Wall Street Journal and Dow Jones Newswires on the daily news in the world's largest democracy<br />
    <input type="checkbox" name="interests[]" value="3" />Sports : The Journal's all-purpose sports report.<br />
    <input type="checkbox" name="interests[]" value="4" />Law : WSJ on the cases, trends and personalities of interest to the business community.<br />
    <input type="checkbox" name="interests[]" value="5" />Japan Real Time : WSJ's inside track on Japan's politics, economy and culture.<br/>
    <input type="checkbox" name="interests[]" value="6" />Digits : Tech news and buzz<br/>
    <input type="checkbox" name="interests[]" value="7" />Expat : The Expat blog!<br/>

    <h1><br />Select level to study<br /></h1>
    <input type="radio" name="level" value="1" />Level 1<br />
    <input type="radio" name="level" value="2" />Level 2<br />
    <input type="radio" name="level" value="3" />Level 3<br />
    <input type="radio" name="level" value="4" />Level 4<br />
    <input type="radio" name="level" value="5" />Level 5<br />
    <input type="radio" name="level" value="6" />Level 6<br />
    <input type="radio" name="level" value="7" />Level 7<br />
    <input type="radio" name="level" value="8" />Level 8<br />
    <input type="radio" name="level" value="9" />Level 9<br />
    <input type="radio" name="level" value="10" />Level 10<br />
  
    <input type="submit" class = "btn" name="formSubmit" value="Submit" />

  </form>
</body>
</html>