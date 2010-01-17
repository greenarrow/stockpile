
		$(function(){
			$(document).ready(function() {
				$('table#items').dataTable({
					
					//"bJQueryUI": true,
					//"bServerSide": false,
					"sDom": 't<lp>',
					
					
					"sPaginationType": "full_numbers",
					
					"bLengthChange": true,
					"bFilter": false,
					"bSort": true,
					"bInfo": false,
					"bAutoWidth":false,
					
					
					
					//T&lt;"clear"&gt;lfrtip
					/*"sDom": '<f><rt>il<p><"clear">'*/
				});
			});
		});
		
		


