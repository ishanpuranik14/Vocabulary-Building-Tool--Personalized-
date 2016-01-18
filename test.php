<html>
<head><title>Test</title></head>
<body>
	<form method = "post" action = "<?php echo $_SERVER['PHP_SELF'];?>">
		<input type = "text" name = "tname" method = "POST"/>
		<input type="submit" name = "submit" value = "Submit"/>
	</form>
	<?php
		if($_SERVER['REQUEST_METHOD'] == 'POST'){
			$name = $_REQUEST['tname'];
			if(empty($name)){
				echo " Enter your name please";
			}
			else{
				echo "Hello $name";
			}
		}

		$conn = mysql_connect("localhost","root" ,"");
		if(! $conn )
		{
		 die('Could not connect: ' . mysql_error());
		}
		echo 'Connected successfully';
		mysql_select_db("cl-master");

		$sql = "SELECT * FROM articlesinterests WHERE iid=1";
		$result = mysql_query( $sql, $conn );
		if(! $result)
		{
		  die('Could not get data: ' . mysql_error());
		}		
		while ($row =  mysql_fetch_array($result, MYSQL_NUM)) {
			echo $row[0]." ".$row[1]." ".$row[2]."<br>"; 
		}
		mysql_free_result($result);
		mysql_close($conn);
		
	?>
</body>
</html>