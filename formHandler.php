<html>
<head>
	<title>Learning begins</title>
</head>
<body>
	<?php	
	if(isset($_POST['submit'])){
		$interests = $_POST['interests'];
		echo $interests;
		$selected_radio = $_POST['level'];
		$sql = "";
		if(empty($interests)) 
        {
			echo "<p>You didn't select any interests.</p>";
		}
		elseif(count($interests) == 1){
			$sql = "SELECT uid,level FROM articlewordmeta WHERE level=$selected_radio AND iid=$interests[0];";
		}
		else{
			$sql = "SELECT uid,level FROM articlewordmeta WHERE level=$selected_radio AND ( iid=$interests[0] OR";
			for ($i=1; $i < count($interests)-1 ; $i++) {
				$temp = " iid=".$interests[$i]." OR"; 
				$sql.=$temp;
			}
			$lastIndex = count($interests)-1;
			$temp1 = " iid=".$interests[$lastIndex].");";
			$sql.=$temp1;
		}

		echo $sql;
	}
	?>
</body>
</html>