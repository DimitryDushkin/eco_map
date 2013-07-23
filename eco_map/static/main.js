var map, layer;
var tableId = '105uGNbjdW40N3OFepuDPjsrxkvLFc-6l6v-httY';
var locationColumnName = 'Lng';


$(function(){
	
	function initMap() {
		// Setup Google maps
		var mapOptions = {
	      	center: new google.maps.LatLng(55.74975, 37.623641),  // Moscow
	     	zoom: 11,
	     	mapTypeId: google.maps.MapTypeId.ROADMAP
	    };	
	    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
	    
	    		
		// ============ Try to get current location ====================
		if (navigator.geolocation)
			navigator.geolocation.getCurrentPosition(function (position) {
		        var coords = new google.maps.LatLng(position.coords.latitude,
		        									position.coords.longitude);
				map.setCenter(coords);
				map.setZoom(15);
				// Place home icon on user's position
				var marker = new google.maps.Marker({
					position: coords,
					map: map,
					title: 'Ваше текущее месторасположение',
					icon: '/static/img/icon_home.png'
				});
			});
		// END ============ Try to get current location ====================	
	}
	
	
	function updateMap() {
		// collect data from each checked checkbox
		var selected_waste_types = []
		$('.choose-waste [type="checkbox"]').each(function(){
			if ($(this).attr('checked'))
				selected_waste_types.push($(this).val() + '=1')
		});
		selected_waste_types = selected_waste_types.join(' AND ')
		
	    // Setup Google Fusion Tables layer
	    if (typeof layer === 'undefined') {
	    	layer = new google.maps.FusionTablesLayer({
				query: {
					select: locationColumnName,
					from: tableId,
					where: selected_waste_types
				}
			});
			
			layer.setMap(map);
		}
	    layer.setQuery({
				select: locationColumnName,
				from: tableId,
				where: selected_waste_types
			});
		
	}
	
	
	// ============ On checkboxes click ====================
	// Show only points with checked types
	$('.choose-waste [type="checkbox"]').click(function(){
		updateMap();
	});
	// END ============ On checkboxes click ====================
	
	
	// ====================== Add waste point ==========================
	// On modal open
	$('#addPointModal').on('show', function () {
		// @TODO: add init animation
  		var $formContainer = $('.addPointFormContainer');
		$formContainer.load($formContainer.attr('action'),
				 			function() {addAutoCompleteToInput()});			
	});
	
	// On add point button click
	$('#addPointButton').click(function(){
		var $form = $('.add-point-form');
		
		$.ajax({
			type: 'POST',
			url: $form.attr('action'),
			data: $form.serialize()
		})
		.done(function(data) {
			// if form is correct filled
			if (data == 'ok') { 
				// Close modal
				$('#addPointModal').modal('hide');
				// @todo: add cogratulations on add
				updateMap()
			} else {
				$form.html(data);
				addAutoCompleteToInput();
			}
		});		
	});
	
	// ======= Add auto-complete to add point modal's input field ==================== 
	function addAutoCompleteToInput() {
		var input = document.getElementById('id_adress');
		var options = {
	  	  componentRestrictions: {country: 'ru'}
		};
		
		var autocomplete = new google.maps.places.Autocomplete(input, options);
	}
	// END ======= Add auto-complete to add point modal's input field ====================
	
	$('#addPointModal').on('click', '.show-additional-fields', function(){
		$addFields = $('.additional-fields');
		$addFields.is(":visible") ? $addFields.fadeOut() 
							      : $addFields.fadeIn();
		
	});
		
	// END ====================== Add waste point ===========================================
	
	//===== Set map canvas always to 100% height ========
	var wheight = $(window).height();
	$('#map_canvas').height(wheight);
	$(window).resize(function(){
		var wheight = $(this).height();
		$('#map_canvas').height(wheight);
	});
	// END ===== Set map canvas always to 100% height ========	
	
	
	
	
	// ============================= Initilization =================================
	initMap();
	updateMap();
	$('body [rel="tooltip"]').tooltip();
	// END ============================= Initilization =================================
});