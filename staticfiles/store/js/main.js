$('.update_cart').click(function(e){
	e.preventDefault() 
	var product_id = $(this).attr("product_id");
	var baseurl = "https://eyeworld.herokuapp.com/insert_cart/"
	console.log(product_id)
	$.ajax( 
	{ 
	    type:"POST",
		url: baseurl,
	    data:{ 
	      		'product_id' : product_id,
	      		'csrfmiddlewaretoken' : '{{ csrf_token }}',
		},
		dataType : 'json', 
		success: function(response) 
		{ 	console.log(response['total_item_cart'])
			$('#cart-total').text(response['total_item_cart'])
		}	  
	}) 
});


$('.update_cart_quantity').click(function(e){ 
	e.preventDefault()
	var product_id = $(this).attr("product_id");
	var action = $(this).attr("action")
	var baseurl = "https://eyeworld.herokuapp.com/cart/update_item/";
	console.log(product_id)
	$.ajax( 
	{ 
	    type:"POST", 
	    url: baseurl,
	    data:{ 
	      		'product_id' : product_id,
	      		'action' : action,
	      		'csrfmiddlewaretoken' : '{{ csrf_token }}',
		},
		dataType : 'json', 
		success: function(response) 
		{ 	
			window.location.reload();
		}  
	}) 
});

