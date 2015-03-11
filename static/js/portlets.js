$(function() {
	$( ".column" ).sortable({
		connectWith: ".column",
		handle: ".portlet-header",
		cancel: ".portlet-toggle",
		placeholder: "portlet-placeholder ui-corner-all"
	});
 
	$( ".portlet" )
		.addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
		.find( ".portlet-header" )
		.addClass( "ui-widget-header ui-corner-all" )
		.prepend( "<span class='ui-icon ui-icon-triangle-1-n portlet-toggle'></span>");
 
	$( ".portlet-toggle" ).click(function() {
		var icon = $( this );
		icon.toggleClass( "ui-icon-triangle-1-n ui-icon-triangle-1-s" );
		icon.closest( ".portlet" )
			.toggleClass( ".portlet-minimized" )
			.find( ".portlet-content" ).toggle();
	});
});
