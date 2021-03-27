var shipping = document.getElementById('shipping-info')
var backtocart = document.getElementById('backtocart')
var storeUrl =backtocart.dataset.storeurl
var shipped = shipping.dataset.shipping
var totprice = shipping.dataset.total
var itemcount = shipping.dataset.itemcount
if ( shipped == 'False' )
{
    document.getElementById('shipping-info').innerHTML = ''
}
if(user != 'AnonymousUser')
{
    document.getElementById('user-info').innerHTML = ''
    
}

if(shipped == 'False' && user != 'AnonymousUser'  )
{
    if(itemcount !='0')
    {
        document.getElementById('form-wrapper').classList.add('hidden')
        document.getElementById('payment-info').classList.remove('hidden')
    }
   else
   {
        document.getElementById('form-wrapper').classList.add('hidden')
        document.getElementById('payment-info').classList.remove('hidden')
        document.getElementById('make-payment').classList.add('hidden')
        document.getElementById('payment-info').innerHTML = '<p>No items in cart</p>'
   }
   
}
var form = document.getElementById('form')
if(form != null){
    form.addEventListener('submit',(e)=>{
        e.preventDefault()
        console.log('form submited ...')
        document.getElementById('form-button').classList.add('hidden')
        document.getElementById('payment-info').classList.remove('hidden')
    })
}
   
if(document.getElementById('make-payment') != null){
    document.getElementById('make-payment').addEventListener('click',(e)=>{
        submitFormData()
    })
    
}

submitFormData = ()=>{
    console.log('data submited')

    var userFormData = {
        'name':null,
        'email':null,
        'total':totprice,
    }
    var shippingInfo = {
        'address':null,
        'city':null,
        'state':null,
        'zipcode':null,
    }
    if(shipped !='False')
    {
        shippingInfo.address = form.address.value
        shippingInfo.city = form.city.value
        shippingInfo.state = form.state.value
        shippingInfo.zipcode = form.zipcode.value
    }
    if(user == 'AnonymousUser')
    {
        userFormData.name = form.name.value
        userFormData.email = form.email.value
    }
  

    var url = '/processorder/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'form':userFormData , 'shipping':shippingInfo}),
    }).then((response)=>response.json())
    .then((data)=>{
        console.log('success',data);
        alert('transaction completed');
        window.location.href = storeUrl
    })
}