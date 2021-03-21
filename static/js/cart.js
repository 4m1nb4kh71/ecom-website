var updateBtns = document.getElementsByClassName('update-cart')
for(i=0;i<updateBtns.length;i++)
{
    
    updateBtns[i].addEventListener('click', (e)=>{
        var productId=e.target.dataset.product
        var action = e.target.dataset.action
        
        console.log('productId:',productId,'action:',action)
        console.log('user:',user)
        if(user === 'AnonymousUser')
        {
           console.log("anonymous user please login") 
        }
        else 
        {
            

            updateUserOrder (productId , action )
           
        }

    })
}

function updateUserOrder (productId , action )
            {
                console.log("user logged in... ")
                var url = '/updateitem/'
                fetch
                (   url,
                    {
                        method:'POST',
                        headers:
                        {
                            'Content-Type':'application/json',
                            'X-CSRFToken':csrftoken
                        },
                        body:JSON.stringify({'productId':productId,'action':action}),
                        
                    },
                    
                ).then((response)=>{
                    return response.json()
                }).then((data)=> {
                   location.reload()
                })

            }