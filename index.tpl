<!doctype html>
<head>
    <meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1">
    <title>KHCC visitcount</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css"> 
    <script type="text/javascript" language="javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>

	<script type="text/javascript" charset="utf-8">
		function get_selected(path) {
			var selected = $("#date_select").val()
			if( /{{re_created_on}}/.test(selected)==false ) {
				return null
			} else {
				return path+"/"+selected
			}
		}
	
		$(document).ready(function() {
			var url = get_selected("table")
			if( url == null ) {
				$('#datatable').DataTable()
			} else {
				var tbl = $('#datatable').DataTable({ajax:url,"order": [[ 2, "desc" ]],pageLength:100});
			}

			$("#csv_btn").click(function(){
				var url = get_selected("csv")
				window.location = url
			})

			$("#date_select").change(function(){
				var url = get_selected("table")
				if( url != null ) {
					tbl.ajax.url(url)
					tbl.ajax.reload()
				}
			})
		});
	</script>

</head>
<body>
	<div class="container">
		<p>Release: {{heroku_release}}</p>
		Date:&nbsp;<select id="date_select">
			% if len(dates) > 0:
				%for date in dates[:-1]:
				<option value="{{date}}">{{date}}</option>
				%end
				<option value="{{dates[-1]}}" selected="selected">{{dates[-1]}}</option>
			% else:
				<option value="">No data available</option>
			% end
		</select>
		<button type="button" id="csv_btn">Download CSV</button>
		<p/>
		<table id="datatable" class="display" cellspacing="0" width="100%">
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
