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
