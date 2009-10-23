		$(function(){
			$(document).ready(function() {
				$('table#items').dataTable({
					
					"bJQueryUI": true,
					//"bServerSide": false,
					"sDom": 'pt',
					
					
					"sPaginationType": "full_numbers",
					//T&lt;"clear"&gt;lfrtip
					/*"sDom": '<f><rt>il<p><"clear">'*/
				});
			});
			
			function doSomething() {
				//alert("I'm done resizing for the moment");
				$('table#items').dataTable().fnDraw(false);
			};
			
			var resizeTimer = null;
			$(window).bind('resize', function() {
				if (resizeTimer) clearTimeout(resizeTimer);
				resizeTimer = setTimeout(doSomething, 100);
			});
		});

