		$(function(){
			
			var name = $("#name"),
				email = $("#email"),
				password = $("#password"),
				allFields = $([]).add(name).add(email).add(password),
				tips = $("#validateTips");
			
			// Dialog
			$("#field_dialog").dialog({
				bgiframe: true,
				resizable: false,
				autoOpen: false,
				width: 400,
				modal: true,
				position: ['center', 50],
				buttons: {
					'Save': function() {
						var bValid = true;
						allFields.removeClass('ui-state-error');
						
						field = $('#field_dialog').attr("field_id");
						
						alert(field);
						alert( $("#field_dialog > input").attr("id") );
						//alert( $("#field_form > select").attr("value") );
						
						$('#field_dialog').html("done");
						
						
						
						/*
						$.ajax({
							type: "POST",
							url: "/field:" + field,
							data: "",
							dataType: "json",
							success: function(data) {

							    if(data.email_check == "invalid"){
								$("#message_ajax").html("<div class='errorMessage'>Sorry " + data.name + ", " + data.email + " is NOT a valid e-mail address. Try again.</div>");
							    } else {
								$("#message_ajax").html("<div class='successMessage'>" + data.email + " is a valid e-mail address. Thank you, " + data.name + ".</div>");
							    }

							}

						});
						*/
						
						
						//$(this).dialog('close');
						
						/*
						// todo get ajax working once regular post accepting is working
						
						*/
						
					},
				
					'Cancel': function() {
						$(this).dialog('close');
					}
				},
				
				close: function() {
					allFields.val('').removeClass('ui-state-error');
				}
			});
			
			
			
			// Dialog Link
			$("a.edit_field").click(function(){
				field = $(this).attr("field_id");
				$('#field_dialog').attr("field_id", field)
				// clear first so we don't see old data
				$('#field_dialog').html("");
				$('#field_dialog').dialog('option', 'title', 'Edit Field');
				$("#dbg").html( $("#dbg").html() + "<br />" + $('#field_dialog').attr("field_id") );
				$("#field_dialog").load("/field:" + field + "?ajax=1");
				$('#field_dialog').dialog('open');
				
				return false;
			});
			
			// Dialog Link
			$("#new_field").click(function(){
				// clear first so we don't see old data
				$('#field_dialog').html("");
				$('#field_dialog').dialog('option', 'title', 'Create Field');
				$("#field_dialog").load("/field:new?ajax=1");
				$('#field_dialog').dialog('open');
				
				return false;
			});
			
			
			$(document).ready(function() {
				$('#category_fields').dataTable({

				});
			} );
			
			
			
		});
