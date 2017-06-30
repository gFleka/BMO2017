<?php
if($_GET['action']=='start')
{
$con = mysqli_connect("**server_ip**","**username**","**password**","**database**");

$result = $con->query("SELECT working FROM led WHERE id = 1");
$row = $result->fetch_assoc();
$working = $row['working'];
if($working=='0')
{
	mysqli_query($con, "UPDATE led SET working='1' WHERE id='1'");
	mysqli_close($con);
}
else
{
	mysqli_query($con, "UPDATE led SET working='0' WHERE id='1'");
	mysqli_close($con);
}
}
else
{
	$con = mysqli_connect("**server_ip**","**username**","**password**","**database**");
	$result = $con->query("SELECT working FROM led WHERE id = 1");
	$row = $result->fetch_assoc();
	$working = $row['working'];
	echo $working;
}

?>