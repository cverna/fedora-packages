<script type="text/javascript">
function on_change(self) {
	$('#specfile_container').load(moksha.url('/_w/package_sources #specfile'), {
		'package_name': '${w.package_name}',
		'branch': self.value
		});
}
</script>

${w.children[0].display(on_change='on_change', package=w.package_name) | n}

<br/>

<div id="specfile_container">
<div id="specfile">
${w.text | n}
</div>
</div>
