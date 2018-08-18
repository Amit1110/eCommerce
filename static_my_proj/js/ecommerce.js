$(document).ready(function()
	{
		//Contact Form Handler

		var contactForm = $(".contact-form")
		var contactFormMethod = contactForm.attr("method")
		var contactFormEndpoint = contactForm.attr("action") 
		

		function displaySubmitting(submitBtn, defaultText, doSubmit)
		{
			if (doSubmit){
				submitBtn.addClass("disaabled")
				submitBtn.html("<i class='fa fa-spin fa-spinner'></i>Submitting...")	
			}else{
				submitBtn.removeClass("disaabled")
				submitBtn.html(defaultText)	
			}
			
		}

		contactForm.submit(function(event){
			event.preventDefault()
			
			var contactFormSubmitBtn = contactForm.find("[type='submit']")
			var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

			var formData = contactForm.serialize()
			var thisForm = $(this)
			displaySubmitting(contactFormSubmitBtn,"",true)
			$.ajax(
			{
				url: contactFormEndpoint,
				method: contactFormMethod,
				data : formData,
				success : function(data){
					contactForm[0].reset()
					$.alert({
						title   : "Eureka!!",
						content : data.message,
						theme   : "modern"})
					setTimeout(function(){
						displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
						
					},500)
				},
				error : function(error){
					console.log(error.responseJSON)
                    var jsonData = error.responseJSON
                    var msg = ""
                    $.each(jsonData, function(key, value){ // key, value  array index / object
                      msg += key + ": " + value[0].message + "<br/>"
                    })
					$.alert({
						title   : "Sorry!!",
						content : msg,
						theme   : "modern"})
					setTimeout(function(){
						displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
						
					},500)
				}
			})
		})

		// Auto Search

		var searchForm = $(".search-form")
		var searchInput = searchForm.find("[name='q']")
		var searchBtn = searchForm.find("[type='submit']")
		var typingTimer;
		var typingInterval = 500 //1.5 seconds

		searchInput.keyup(function(event){
			clearTimeout(typingTimer)
			typingTimer = setTimeout(performSearch,typingInterval)

		})

		searchInput.keydown(function(event){
			clearTimeout(typingTimer)
		})

		function displaySearching()
		{
			searchBtn.addClass("disaabled")
			searchBtn.html("<i class='fa fa-spin fa-spinner'></i>Searching...")
		}

		function performSearch()
		{
			//console.log(searchInput.val())
			displaySearching()

			query = searchInput.val()

			setTimeout(function()
			{
				window.location.href = '/search/?q=' + query
			},1000)
			
		}

		//Ajax and Form
		var productForm = $(".form-product-ajax")
		productForm.submit(function(event)
		{
			event.preventDefault();
			//console.log("Form is not sent")
			var thisform = $(this)
			//var actionEnd = thisform.attr("action");
			var actionEnd = thisform.attr("data-endpoint");// API EndPoint
			var method = thisform.attr("method");
			var formData = thisform.serialize();

			//console.log(thisform.attr("action"), thisform.attr("method"), thisform.attr("action"))

			$.ajax({
				url: actionEnd,
				method: method,
				data: formData,
				success: function(data){
					// console.log("success")
				 //    console.log(data)
				 //    console.log("Added", data.added)
				 //    console.log("Removed", data.removed)
				    var submitSapn = thisform.find('.submit-span')
				    if (data.added){
				    	submitSapn.html("In cart <button type='submit' class='btn btn-link'>Remove?</button>")
				    }
				    else
				    {
				    	submitSapn.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
				    }
				    var navbar = $(".navbar-cart-count")
				    navbar.text(data.cartItemCount)

				    var currentPath = window.location.href //checks for word in the path
				    if (currentPath.indexOf("cart") != 1)
				    {
				    	refreshCart()
				    }
				},
				error: function(errorData){
					$.alert({
						title : "Sorry!!",
						content:"An error occured",
						theme : "modern"})
					console.log("error")
					console.log(errorData)
				}
			})
		})
		function refreshCart(){
			console.log("in current cart")
			var cartTable = $(".cart-table")
			var cartBody = cartTable.find(".cart-body")
			//cartBody.html("<h1>Changed</h1>")
			var productRows = cartBody.find(".cart-product")

			var currentUrl = window.location.href

			var refreshCartactUrl = '/api/cart/'
			var refreshCartmethod = "GET";
			var data = {};

			$.ajax({
				url: refreshCartactUrl,
				method: refreshCartmethod,
				data: data,
				success: function(data){
					 var hiddenCartItemRemoveForm = $(".cart-item-remove-form")


					if(data.products.length > 0)
					{
						productRows.html(" ");
						i = data.products.length
						$.each(data.products, function(index,value)
						{
							console.log(value)

							var newCartItemRemove = hiddenCartItemRemoveForm.clone()

							newCartItemRemove.css("display","block")
							//newCartItemRemove.removeClass("display","block")
							newCartItemRemove.find(".cart-item-product-id").val(value.id)

							cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")	
							i --
						})

						
						cartBody.find(".cart-subtotal").text(data.subtotal)
						cartBody.find(".cart-total").text(data.total)
					}
					else
					{
						window.location.href = currentUrl
					}
				},
				error: function(errorData){
					console.log("error")
					console.log(errorData)
				}
			})
		}
	})