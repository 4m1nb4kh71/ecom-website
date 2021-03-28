addbutton = document.getElementById('form-button')
productForm = document.getElementById('product-form')

addbutton.addEventListener('click' , (e)=>{
    submitproduct()
})

submitproduct = ()=> {

    productFormData = {
        'name':null,
        'price':null,
        'img':null,
        'digital':null,
    }

    productFormData.name = productForm.name.value
    productFormData.price = productForm.price.value
    productFormData.img = productForm.img.value
    productFormData.digital = productForm.digital.value

    var url = '/addproduct/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'form':productFormData}),
    }).then((response)=>response.json())
    .then((data)=>{
        console.log('success',data);
        alert('product added');
       
    })
}