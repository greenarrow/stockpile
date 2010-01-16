$(function(){
	
	//hover states on the static widgets
	$('.button, .button_text').hover(
		function() { $(this).addClass('ui-state-hover'); }, 
		function() { $(this).removeClass('ui-state-hover'); }
	);
	
	//hover states on the static widgets
	$('a').hover(
		function() { $(this).addClass('link_hover'); }, 
		function() { $(this).removeClass('link_hover'); }
	);
	
	// Invert the header colors - TODO get this abomination out of here
	$('#header').css( { 'background':$('#header').css('color'), 'color':$('.ui-widget-content').css('background-color') } );
	
	
	$(".show-hide-sidebar-left").click( function(){
		//alert('dd');
		$("div#sidebar_left").toggle(300);
		$("div#show-sidebar-left").toggle(300);
		$("div#main_body").toggleClass('sidebar_visible', 300);
	});
	
	/*
	$("div#show-sidebar-left").click( function(){
		
		$("div#main_body").addClass('sidebar_visible', 300);
		$("div#show-sidebar-left").hide(300);
		
		$("div#show-sidebar-left").queue( function () {
			$("div#sidebar_left").show(300);
		});
	});
	
	$("div#hide-sidebar-left").click( function(){
		$("div#sidebar_left").hide(300);
		
		$("div#sidebar_left").queue( function () {
			$("div#show-sidebar-left").show(100);
			$("div#main_body").removeClass('sidebar_visible', 200);
		});
		
		
		
	});
	*/
	
	$("div.sidebar-module > .sidebar-header").click( function(){
		$(this).parent().find(".sidebar-content").toggle('fold', 500);
	});
	
	$('.sidebar-header').hover(
		function() { $(this).addClass('ui-state-hover'); }, 
		function() { $(this).removeClass('ui-state-hover'); }
		
	);
	
	
	var name = $("#name"),
		email = $("#email"),
		password = $("#password"),
		allFields = $([]).add(name).add(email).add(password),
		tips = $("#validateTips");

	// Dialog
	$("div.dialog").dialog({
		bgiframe: true,
		//resizable: false,
		autoOpen: false,
		width: 400,
		modal: true,
		position: ['center', 50],
		buttons: {
			'Save': function() {
				var bValid = true;
				//allFields.removeClass('ui-state-error');
				
				$(this).dialog('close');
					
			},
			
			'Cancel': function() {
				$(this).dialog('close');
			}
		},
		
		close: function() {
			allFields.val('').removeClass('ui-state-error');
		}
	});
	
	$("a.open-in-dialog").click(function(){
		// clear first so we don't see old data
		$('div.dialog').html("");
		$('div.dialog').dialog( 'option', 'title', $(this).attr("title") );
		url = $(this).attr("href");
		$("div.dialog").load(url + "?ajax=1");
		//alert( url + "?ajax=1" );
		$('div.dialog').dialog('open');
		
		return false;
	});
	
	


	

});


