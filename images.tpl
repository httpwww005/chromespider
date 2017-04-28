<!doctype html>
<head>
    <meta charset="utf-8" />
    <title>KHCC visitcount</title>
	<style>
		img {
			height: 600px;
		}

	</style>
</head>
<body>
	<div id="images">
		% if len(images) > 0:
			% for image in images:
				<a href="http://i.imgur.com/{{image["id"]}}.jpg"> <img border=3 src="http://i.imgur.com/{{image["id"]}}.jpg" /> </a>
			% end
		% end
		% if len(gdimages) > 0:
			% for image in gdimages:
				<a href="http://drive.google.com/uc?export=download&id={{image["drive_id"]}}"> <img border=3 src="http://drive.google.com/uc?export=download&id={{image["drive_id"]}}" /> </a>
			% end
		% end
	</div>
</body>
</html>
