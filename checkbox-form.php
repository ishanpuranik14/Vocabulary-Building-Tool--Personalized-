<html>
<head>
	<title> Test Page </title>
</head>
<body>
	<?php
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