<!DOCTYPE html>
<html>
<head>
    <title>cricrate | Best/Worst ODI Fielding Careers</title>		
    <script>
	submitForms = function(){
	    window.document.selectForm.submit();
	}
    </script>
    <link rel="stylesheet" type="text/css" href="style.css" />
</head>    
<header>	
</header>

<body>
<div id="content">
<?php

echo "<div id=\"pageHeader\"><a href=\"#best\">Best</a>/<a href=\"#worst\">Worst</a> ODI Fielding Careers&nbsp;&nbsp;";
echo "<form name=\"selectForm\" method=\"get\" action=\"cricStats.php\">";
echo "<select name=\"span\" onChange=\"submitForms()\">";
if(isset($_GET['span'])) {    
    $span = $_GET['span'];
    echo ($span == "2000-2099") ? "<option selected=\"selected\" value=\"2000-2099\">All-time</option>" : "<option value=\"2000-2099\">All-time</option>";
    echo ($span == "2005-2009") ? "<option selected=\"selected\" value=\"2005-2009\">2005-2009</option>" : "<option value=\"2005-2009\">2005-2009</option>";
    echo ($span == "2010-2019") ? "<option selected=\"selected\" value=\"2010-2014\">2010-2014</option>" : "<option value=\"2010-2014\">2010-2014</option>";
} else {
    $span = "1877-2099";
    echo "<option selected=\"selected\" value=\"2000-2099\">All-time</option>";
    echo "<option value=\"2005-2009\">2000-2005</option>";
    echo "<option value=\"2010-2014\">2010-2014</option>";
}
echo "</select>";
echo "&nbsp;&nbsp;";
echo "<select name=\"team\" onChange=\"submitForms()\">";
if(isset($_GET['team'])) {    
    $team = $_GET['team'];
    echo ($team == "All teams") ? "<option selected=\"selected\" value=\"All teams\">All teams</option>" : "<option value=\"All teams\">All teams</option>";
    echo ($team == "Australia") ? "<option selected=\"selected\" value=\"Australia\">Australia</option>" : "<option value=\"Australia\">Australia</option>";
    echo ($team == "Bangladesh") ? "<option selected=\"selected\" value=\"Bangladesh\">Bangladesh</option>" : "<option value=\"Bangladesh\">Bangladesh</option>";
    echo ($team == "England") ? "<option selected=\"selected\" value=\"England\">England</option>" : "<option value=\"England\">England</option>";
    echo ($team == "India") ? "<option selected=\"selected\" value=\"India\">India</option>" : "<option value=\"India\">India</option>";
    echo ($team == "New Zealand") ? "<option selected=\"selected\" value=\"New Zealand\">New Zealand</option>" : "<option value=\"New Zealand\">New Zealand</option>";
    echo ($team == "Pakistan") ? "<option selected=\"selected\" value=\"Pakistan\">Pakistan</option>" : "<option value=\"Pakistan\">Pakistan</option>";
    echo ($team == "South Africa") ? "<option selected=\"selected\" value=\"South Africa\">South Africa</option>" : "<option value=\"South Africa\">South Africa</option>";
    echo ($team == "Sri Lanka") ? "<option selected=\"selected\" value=\"Sri Lanka\">Sri Lanka</option>" : "<option value=\"Sri Lanka\">Sri Lanka</option>";
    echo ($team == "West Indies") ? "<option selected=\"selected\" value=\"West Indies\">West Indies</option>" : "<option value=\"West Indies\">West Indies</option>";
    echo ($team == "Zimbabwe") ? "<option selected=\"selected\" value=\"Zimbabwe\">Zimbabwe</option>" : "<option value=\"Zimbabwe\">Zimbabwe</option>";
} else {
    $team = "All teams";
    echo "<option selected=\"selected\" value=\"All teams\">All teams</option>";
    echo "<option value=\"Australia\">Australia</option>";
    echo "<option value=\"Bangladesh\">Bangladesh</option>";
    echo "<option value=\"England\">England</option>";
    echo "<option value=\"India\">India</option>";
    echo "<option value=\"New Zealand\">New Zealand</option>";
    echo "<option value=\"Pakistan\">Pakistan</option>";
    echo "<option value=\"South Africa\">South Africa</option>";
    echo "<option value=\"Sri Lanka\">Sri Lanka</option>";
    echo "<option value=\"West Indies\">West Indies</option>";
    echo "<option value=\"Zimbabwe\">Zimbabwe</option>";
}
echo "</select>";
echo "&nbsp;&nbsp;";
echo "<select name=\"role\" onChange=\"submitForms()\">";
if(isset($_GET['role'])) {    
    $role = $_GET['role'];
    echo ($role == "All roles") ? "<option selected=\"selected\" value=\"All roles\">All roles</option>" : "<option value=\"All roles\">All roles</option>";
    echo ($role == "Fielders") ? "<option selected=\"selected\" value=\"Fielders\">Fielders</option>" : "<option value=\"Fielders\">Fielders</option>";
    echo ($role == "Keepers") ? "<option selected=\"selected\" value=\"Keepers\">Keepers</option>" : "<option value=\"Keepers\">Keepers</option>";
} else {
    $role = "All roles";
    echo "<option selected=\"selected\" value=\"All roles\">All roles</option>";
    echo "<option value=\"Fielders\">Fielders</option>";
    echo "<option value=\"Keepers\">Keepers</option>";
}
echo "</select>";
echo "</form>";
echo "</div>";
echo "<a name=\"best\"></a>";
echo "<h4>Best ODI Fielding Careers</h4>";

$spanDates = split("-", $span);
$startSpan = $spanDates[0]."0000";
$endSpan = $spanDates[1]."9999";
$db = new SQLite3('cricStats.db');
if ($team == "All teams") {
    if ($role == "All roles") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.greatFieldings, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating desc limit 50";        
    } elseif ($role == "Fielders") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.greatFieldings, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and a.keeper=0 order by a.rating desc limit 50";
    } else {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.stumpings, a.missedStumpings, a.stumpRate, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and a.keeper=1 order by a.rating desc limit 50";
    }
} else {
    if ($role == "All roles") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.greatFieldings, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating desc limit 50";
    } elseif ($role == "Fielders") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.directHits, a.greatFieldings, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' and a.keeper=0 order by a.rating desc limit 50";
    } else {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.greatCatches, a.stumpings, a.missedStumpings, a.stumpRate, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' and a.keeper=1 order by a.rating desc limit 50";
    }
}
$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
echo "<table class=\"sortable\" id=\"ratingsTable\">";
echo "<thead><tr>";
echo "<th align='right'>Rank</th>";
echo "<th align='left'>Player</th>";
echo "<th align='center'>Country</th>";
echo "<th align='center'>Span</th>";
echo "<th align='right'>Mat</th>";
echo "<th align='right'>Catches</th>";
echo "<th align='right'>Drops</th>";
echo "<th align='center'>Drop %</th>";
echo "<th align='right'>Great Catches</th>";
if ($role == "Keepers") {
    echo "<th align='right'>Stumps</th>";
    echo "<th align='right'>Missed Stump</th>";
    echo "<th align='right'>Stump %</th>";
} else {
    echo "<th align='right'>Direct Hits</th>";
    echo "<th align='right'>Saves</th>";
    echo "<th align='right'>Runs</th>";
}
echo "<th align='right'>Rating</th>"; 
echo "</tr></thead>";

$k = 1;
while($res = $result->fetchArray(SQLITE3_NUM)) {
    $lastPlayedYear = substr($res[3], 0, 4);
    if ($lastPlayedYear == 2015) {
        echo "<tr id=\"currentPlayer\">";
    } else {
        echo "<tr>";   
    }
    echo "<td align='right'>$k</td>";
    for ($j = 1; $j < $result->numColumns(); $j++) {
        if ($j == 1) {
            echo "<td align='left'>".str_replace("Sir ","",$res[$j])."</td>";
	} elseif ($j == 2) { # country
	    echo "<td align='center'><a href=\"../../team.php?team=".$res[$j]."\"><img src=\"../../images/".$res[$j].".png\" alt=\"$res[$j]\" border=1px/></a></td>";
        } elseif ($j == 3) { # span
            echo "<td align='right'>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
            $j++;
	} elseif ($j == 8) { # drop rate
            echo "<td align='right'>".number_format(round($res[$j] * 100, 2), 2)."</td>";
	} elseif ($j == 12 and $role == "Keepers") {
	    echo "<td align='right'>".number_format(round($res[$j] * 100, 2), 2)."</td>";
        } elseif ($j == 13) { # rating
            echo "<td align='right'><b>".round($res[$j], 0)."</b></td>";
        } else {
            echo "<td align='right'>$res[$j]</td>";   
        }        
    }       
    echo "</tr>";
    $k++;
} 
echo "</table>";

echo "<a name=\"worst\"></a>";
echo "<h4>Worst ODI Fielding Careers</h4>";

if ($team == "All teams") {
    if ($role == "All roles") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.directHits, a.misfields, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." order by a.rating asc limit 50";        
    } elseif ($role == "Fielders") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.directHits, a.misfields, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and a.keeper=0 order by a.rating asc limit 50";
    } else {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.stumpings, a.missedStumpings, a.stumpRate, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and a.keeper=1 order by a.rating asc limit 50";
    }
} else {
    if ($role == "All roles") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.directHits, a.misfields, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' order by a.rating asc limit 50";
    } elseif ($role == "Fielders") {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.directHits, a.misfields, a.runsSaved, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' and a.keeper=0 order by a.rating asc limit 50";
    } else {
	$sql = "select a.playerId, a.player, p.country, a.startDate, a.endDate, a.odis, a.catches, a.droppedCatches, a.dropRate, a.stumpings, a.missedStumpings, a.stumpRate, a.rating from fieldingODICareer a, playerInfo p where p.playerId=a.playerId and ((a.startDate+a.endDate)/2)>".$startSpan." and ((a.startDate+a.endDate)/2)<=".$endSpan." and p.country='".$team."' and a.keeper=1 order by a.rating asc limit 50";
    }
}

$result = $db->query($sql);
if (!$result) die("Cannot execute query.");
echo "<table class=\"sortable\" id=\"ratingsTable\">";
echo "<thead><tr>";
echo "<th align='right'>Rank</th>";
echo "<th align='left'>Player</th>";
echo "<th align='center'>Country</th>";
echo "<th align='center'>Span</th>";
echo "<th align='right'>Mat</th>";
echo "<th align='right'>Catches</th>";
echo "<th align='right'>Drops</th>";
echo "<th align='center'>Drop %</th>";
if ($role == "Keepers") {
    echo "<th align='right'>Stumps</th>";
    echo "<th align='right'>Missed Stump</th>";
    echo "<th align='right'>Stump %</th>";
} else {
    echo "<th align='right'>Direct Hits</th>";
    echo "<th align='right'>Misfields</th>";
    echo "<th align='right'>Runs</th>";
}
echo "<th align='right'>Rating</th>"; 
echo "</tr></thead>";

$k = 1;
while($res = $result->fetchArray(SQLITE3_NUM)) {
    $lastPlayedYear = substr($res[3], 0, 4);
    if ($lastPlayedYear == 2015) {
        echo "<tr id=\"currentPlayer\">";
    } else {
        echo "<tr>";   
    }
    echo "<td align='right'>$k</td>";
    for ($j = 1; $j < $result->numColumns(); $j++) {
        if ($j == 1) {
            echo "<td align='left'>".str_replace("Sir ","",$res[$j])."</td>";
	} elseif ($j == 2) { # country
	    echo "<td align='center'><a href=\"../../team.php?team=".$res[$j]."\"><img src=\"../../images/".$res[$j].".png\" alt=\"$res[$j]\" border=1px/></a></td>";
        } elseif ($j == 3) { # span
            echo "<td align='right'>".substr($res[$j], 0, 4)."-".substr($res[$j+1], 0, 4)."</td>";
            $j++;
	} elseif ($j == 8) { # drop rate
            echo "<td align='right'>".number_format(round($res[$j] * 100, 2), 2)."</td>";
	} elseif ($j == 11 and $role == "Keepers") {
	    echo "<td align='right'>".number_format(round($res[$j] * 100, 2), 2)."</td>";
        } elseif ($j == 12) { # rating
            echo "<td align='right'><b>".round($res[$j], 0)."</b></td>";
        } else {
            echo "<td align='right'>$res[$j]</td>";   
        }        
    }       
    echo "</tr>";
    $k++;
} 
echo "</table>";
$db->close();
?>
</div>
<div id="rightmargin"></div>
</body>
</html>