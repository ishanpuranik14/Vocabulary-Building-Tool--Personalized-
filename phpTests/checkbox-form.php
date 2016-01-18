<html>
<head>
	<title> Test Page </title>
</head>
<body>
	<?php
	/*
	function google($fname="husband", $mname ){
			echo "<p>mother's name : $mname and father's name : $fname </p>";
			$mname.=$fname;
			return $mname;
		}

		$fatherNames = array('1' => "ajay", '2' => "sanjeev", '3' => "rajeev");
		$motherNames = array('1' => "nandini", '2' => "kumud", '3' => ":)" );

		google("shalabh", "shalabh");

		echo strlen("shalabh");

		for($x=1 ; $x<=3; $x++){
			$father = $fatherNames[$x];
			$mother = $motherNames[$x];
			echo google( $father,$mother);
		}

		$cars["o"] = "merc";
		$cars["p"] = "bmw";
		$cars["q"] = "lambo";
		print_r("<p></p>");
		echo count($cars);
		print_r("<p></p>");
		sort($cars);
		foreach ($cars as $x => $v) {
			echo $x." : ".$v;			
		}

		echo "<br><br><br><p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>";
		$myFile = fopen("articles/WSJDIG101020143.txt", 'r');
		echo fread($myFile, filesize("articles/WSJDIG101020143.txt"));
		fclose($myFile);
	*/
		if (isset($_POST['interest'] && $_POST['interest'] == 1) {
			echo "Selected interest no. 1";
		}
		else{
			echo "Not selected interest no. 1";
		}
	?>
	<form action="<?php echo htmlentities($_SERVER['PHP_SELF']); ?>" method="post">
		<input type="checkbox" name="interest" value="1"/> Personal Technology
		<br>		
		<input type="submit" name="formSubmit" value="Submit"/>	
	</form>
</body>
</html>