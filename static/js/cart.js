var updateBtns = document.getElementsByClassName('update-cart')

for(i=0;i<updateBtns.length;i++)
{
    
    updateBtns[i].addEventListener('click', (e)=>{
        var productId=e.target.dataset.product
        var action = e.target.dataset.action
        var item = e.target.dataset.item
        
        console.log('productId:',productId,'action:',action,'itemid:',item)
        console.log('user:',user)
        if(user === 'AnonymousUser')
        {
           console.log("anonymous user please login") 
        }
        else 
        {
            

            updateUserOrder (productId , action ,item )
           
        }

    })
}

function updateUserOrder (productId , action,item )
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
                        body:JSON.stringify({'productId':productId,'action':action,'item':item}),
                        
                    },
                    
                ).then((response)=>{
                    return response.json()
                }).then((data)=> {
                   location.reload()
                })

            }

