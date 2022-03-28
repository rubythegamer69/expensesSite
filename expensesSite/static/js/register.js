const usernameField=document.querySelector('#usernamefield');
const userDisplay=document.querySelector('.invalid-feedback')
usernameField.addEventListener('keyup',(e)=>{
    
    const uNameVal = e.target.value
   
    if (uNameVal.length > 0) {
        fetch("/authentication/validate-username",{
            body: JSON.stringify({username: uNameVal}),
            method: "POST",
        }) 
        .then((res)=> res.json())
        .then((data)=> {
            console.log("data",data)
            if (data.username_error) {
                usernamefield.classList.add("is-invalid")
                userDisplay.style.display='block'
                userDisplay.innerHTML=`<p>${data.username_error}</p>`
            }
        })

    }
    
})