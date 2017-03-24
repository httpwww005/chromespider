<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>table</title>
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css">
    <script type="text/javascript" language="javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" charset="utf-8">
		$(document).ready(function() {
			$('#datatable').dataTable({"pageLength":100});
		} );
	</script>

</head>
<body>
	<div class="container">
		<table id="datatable" class="display">
			<thead>
				  <tr>
				  %for col in header:
					<td>{{col}}</td>
				  %end
				  </tr>
			</thead>
			<tfoot>
				  <tr>
				  %for col in header:
					<td>{{col}}</td>
				  %end
				  </tr>
			</tfoot>
			<tbody>
				%for row in rows:
				  <tr>
				  %for col in row:
					<td>{{col}}</td>
				  %end
				  </tr>
				%end
			</tbody>
		</table>
	</div>
</body>
</html>
