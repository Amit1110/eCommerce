$(document).ready(function(){


var stripeFormModule = $(".stripe-payment-form")
	var stripeModuleToken = stripeFormModule.attr("data-token")
	var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
	var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add Card"
	var stripeTemplate = $.templates("#stripeTemplate")
	var stripeTemplateDataContext = {
		publish_key : stripeModuleToken,
		next_url : stripeModuleNextUrl,
		btn_title : stripeModuleBtnTitle
	}

	var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
	stripeFormModule.html(stripeTemplateHtml)

	//https source site


	// Create a Stripe client.

	paymentForm = $('.payment-form')

	if (paymentForm.length > 1){
		alert("Only one Payment form allowed per page")
		paymentForm.css('display','None')
	}	

	else if (paymentForm.length == 1){

	token = paymentForm.attr("data-token")
	nextUrl = paymentForm.attr("data-next-url")

	var stripe = Stripe(token);

	// Create an instance of Elements.
	var elements = stripe.elements();

	// Custom styling can be passed to options when creating an Element.
	// (Note that this demo uses a wider set of styles than the guide below.)
	var style = {
	  base: {
	    color: '#32325d',
	    lineHeight: '18px',
	    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
	    fontSmoothing: 'antialiased',
	    fontSize: '16px',
	    '::placeholder': {
	      color: '#aab7c4'
	    }
	  },
	  invalid: {
	    color: '#fa755a',
	    iconColor: '#fa755a'
	  }
	};

	// Create an instance of the card Element.
	var card = elements.create('card', {style: style});

	// Add an instance of the card Element into the `card-element` <div>.
	card.mount('#card-element');

	// Handle real-time validation errors from the card Element.
	card.addEventListener('change', function(event) {
	  var displayError = document.getElementById('card-errors');
	  if (event.error) {
	    displayError.textContent = event.error.message;
	  } else {
	    displayError.textContent = '';
	  }
	});

	// Handle form submission.
	var form = document.getElementById('payment-form');
	form.addEventListener('submit', function(event) {
	  event.preventDefault();

	  stripe.createToken(card).then(function(result) {
	    if (result.error) {
	      // Inform the user if there was an error.
	      var errorElement = document.getElementById('card-errors');
	      errorElement.textContent = result.error.message;
	    } else {
	      // Send the token to your server.
	      stripeTokenHandler(nextUrl,result.token);
	    }
	  });
	});

function redirectToPath(nextUrl, timeoffset){
	if (nextUrl){
		setTimeout(function(){
				window.location.href = nextUrl
			},timeoffset)
	}
}

function stripeTokenHandler(nextUrl,token){
	console.log(token.id)
	var paymentMethodEndpoint = '/billing/payment-method/create/'
	var data = {
		'token' : token.id
	}
	$.ajax({
		data : data,
		url : paymentMethodEndpoint,
		method : "POST",
		success : function(data){
			var successMsg = data.message || "Success! Your card was added."
			card.clear()
			if (nextUrl){
                successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
            }
			if($.alert){
				$.alert(successMsg)
			} else{
				$.alert(successMsg)
			}
			redirectToPath(nextUrl,1500)
		},
		error : function(error){
			console.log(error)
		}

	})
}
}
})