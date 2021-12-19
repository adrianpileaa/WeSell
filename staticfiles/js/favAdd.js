			favBtn=document.getElementById('favourite');
			favBtn.addEventListener('click', function(){
				productId = this.dataset.product;
				action = this.dataset.action;
				if(user === 'AnonymousUser'){
					window.location.href = "http://localhost:8000/login/"
				}
				else{
					addFavouriteList(productId, action)
				}
			});

			function addFavouriteList(productId, action){
				var url = '/add_favourite/'
				fetch(
					url,{
					method : 'POST',
					headers : {
						'ContentType' : 'application/json',
						'X-CSRFToken' : csrftoken,
					},
					body : JSON.stringify({'productId' : productId, 'action' : action})
				})

				.then(response => response.json())

				.then((data) => {
					console.log(data)
					location.reload()	
					}
				)
			}