<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>table</title>
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css">
    <script type="text/javascript" language="javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" charset="utf-8">
	
		$(document).ready(function() {
			var selected_day = $("#date_select").val()
			if( selected_day != null ) {
				var url = "/table/"+selected_day
				$('#datatable').DataTable({ajax:url,pageLength:100});
			} else {
				$('#datatable').DataTable()
			}

			$("#date_select").change(function(){
				var selected_day = $("#date_select").val()
				if( selected_day != null ) {
					var url = "/table/"+$(this).selected_day
					$('#datatable').DataTable().destroy()
					$('#datatable').DataTable({ajax:url,pageLength:100});
				}
			})
		});
	</script>

</head>
<body>
	<div class="container">
		<select id="date_select">
			% if len(dates) > 0:
				%for date in dates[:-1]:
				<option value="{{date}}">{{date}}</option>
				%end
				<option value="{{dates[-1]}}" selected="selected">{{dates[-1]}}</option>
			% end
		</select>
		<p/>
		<br/>
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
			</tbody>
		</table>
	</div>
</body>
</html>
